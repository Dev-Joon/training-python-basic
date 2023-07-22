# 05_StockPriceAPI\Investar\DBUpdater.py
import pymysql
import pandas as pd
from datetime import datetime
from urllib.request import urlopen

import requests
from bs4 import BeautifulSoup
import urllib, pymysql, calendar, time, json
from threading import Timer
import myslacker

class DBUpdater:
    def __init__(self):                                                             # DBUpdater의 생성자 내부에서 마리아디비에 연결한다.
        """생성자 : MariaDB 연결 및 종목코드 딕셔너리 생성"""
        self.myslack = myslacker.myslacker()
        self.myslack.post_message(
            f"[{time.strftime('%Y-%m-%d %H:%M:%S')}]\n ▶Initializing DBUpdater Object..")

        self.conn = pymysql.connect(host='xxx.xxx.xxx.xxx',
                                    port=3130,
                                   user='**********',
                                   password='***********',
                                   db='Investar',
                                   charset='utf8')
        
        with self.conn.cursor() as curs:
            sql = """
            CREATE TABLE IF NOT EXISTS company_info(
                code VARCHAR(20),
                company VARCHAR(40),
                last_update DATE,
                PRIMARY KEY(code)
                )
            """
            curs.execute(sql)
            sql = """
            CREATE TABLE IF NOT EXISTS daily_price (
                code VARCHAR(20),
                date Date,
                open BIGINT(20),
                high BIGINT(20),
                low BIGINT(20),
                close BIGINT(20),
                diff BIGINT(20),
                volume BIGINT(20),
                PRIMARY KEY (code, date)
                )
            """
            curs.execute(sql)

        self.conn.commit()

        self.codes = dict()
        self.update_comp_info()

    def __del__(self):
        """소멸자 : MariaDB의 연결 해제"""
        self.conn.close()

    def read_krx_code(self):                                                     # KRX로부터 상장법인 목록 파일을 읽어온다.
        """KRX로부터 상장법인목록 파일을 읽어와서 데이터프레임으로 반환"""
        url = 'https://kind.krx.co.kr/corpgeneral/corpList.do?method='\
            'download&searchType=13'
        krx = pd.read_html(url, header=0)[0]                                     # 상장법인목록.xls 파일을 read_html() 함수로 읽는다.
        krx = krx[['종목코드', '회사명']]                                         # 종목코드 칼럼과 회사명만 남긴다. 데이터프레임에 [[]]을 사용하면 특정 컬럼만 뽑아서 원하는 순서대로 재구성할 수 있다.
        krx = krx.rename(columns={'종목코드':'code','회사명':'company'})          # 한글 칼럼명을 영문 칼럼명으로 변경한다.
        krx.code = krx['code'].map('{:06d}'.format)                              # 종목코드 형식을 {:06d} 형식의 문자열로 변경한다.
        self.myslack.post_message(
            f"[{time.strftime('%Y-%m-%d %H:%M:%S')}]\n ▶read_krx_code\n ▶{url}")
        return krx

    def update_comp_info(self):
        """종목코드를 company_info 테이블에 업데이트 한 후 딕셔너리에 저장"""
        sql = "SELECT * FROM company_info"
        df = pd.read_sql(sql, self.conn)                                         # company_info 테이블을 read_sql() 함수로 읽는다.                                                                        
        for idx in range(0, len(df)):
            self.codes[df['code'].values[idx]] = df['company'].values[idx]       # 위에서 읽은 데이터프레임을 이용해서 종목코드와 회사명으로 codes 딕셔너리를 만든다.

        with self.conn.cursor() as curs:
            sql = "SELECT max(last_update) FROM company_info"
            curs.execute(sql)
            rs = curs.fetchone()                                                 # SELECT max() ~ 구문을 이용해서 DB에서 가장 최근 업데이트 날짜를 가져온다.
            today = datetime.today().strftime('%Y-%m-%d')

            if rs[0] == None or rs[0].strftime('%Y-%m-%d') < today:              # 위에서 구한 날짜가 존재하지 않거나 오늘보다 오래된 경우에만 업데이트한다.
                krx = self.read_krx_code()                                       # KRX 상장기업 목록 파일을 읽어서 krx 데이터프레임에 저장한다.
                for idx in range(len(krx)):
                    code = krx['code'].values[idx]
                    company = krx['company'].values[idx]
                    sql = f"REPLACE INTO company_info (code, company, last"\
                        f"_update) VALUES ('{code}', '{company}', '{today}')"
                    curs.execute(sql)                                            # REPLACE INTO 구문을 이용해서 '종목코드, 회사명, 오늘날짜'행을 DB에 저장한다. 

                    self.codes[code] = company                                   # codes 딕셔너리에 '키-값'으로 종목코드와 회사명을 추가한다.
                    timenow = datetime.now().strftime('%Y-%m-%d %H:%M')
                    #print(f"[{timenow}]) {idx:04d} REPLACE INTO company_info VALUES ({code}, {company}, {today})")

                self.myslack.post_message(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}]\n ▶[{len(krx)}ea] Company Info. has been replaced.")
                self.conn.commit()
                #print('')


    #def read_naver(self, code, start):
    def read_naver(self, code, company, pages_to_fetch):
        """네이버 금융에서 주식 시세를 읽어서 데이터프레임으로 반환"""
        try:
            url = f"https://finance.naver.com/item/sise_day.nhn?code={code}"
            # 해당 사이트는 반드시 헤더 정보를 요구하기 때문에 헤더를 넘겨줘야 함
            headers = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)' }
            req = requests.get(url, headers=headers)

            # 첫 페이지를 파싱해서 전체 페이지 수 계산
            html = BeautifulSoup(req.text, 'html.parser')
            try:
                lastpage = int(html.select_one('td.pgRR').a['href'].split('=')[-1])
            except:
                lastpage = 1

            # 네이버 금융에서 일별 시세의 마지막 페이지를 구한다.
            df = pd.DataFrame()
            pages = min(lastpage, pages_to_fetch)                              # 설정 파일에 설정된 페이지 수(pages_to_fetch)와 위의 페이지 수에서 작은 것을 택한다.
            for page in range(1, pages + 1):
                req = requests.get(f'{url}&page={page}', headers = headers)
                # pg_url = '{}&page={}'.format(url, page)
                # df = df.append(pd.read_html(pg_url, header=0)[0])                   # 일별 시세 페이지를 read_html()로 읽어서 데이터프레임에 추가한다.
                df = pd.concat([df, pd.read_html(req.text, encoding='euc-kr')[0]], ignore_index=True)
                tmnow = datetime.now().strftime("%Y-%m-%d %H:%M")
                #print('[{}] {} ({}) : {:04d}/{:04d} pages are downloading...'.format(tmnow, company, code, page, pages), end="\r")
            df = df.rename(columns={'날짜':'date','종가':'close','전일비':'diff'
                ,'시가':'open', '고가':'high', '저가':'low', '거래량':'volume'})     # 네이버 금융의 한글 컬럼명을 영문 컬럼명으로 변경한다.
            df['date'] = df['date'].replace('.', '-')                              # 연.월.일 형식의 일자 데이터를 연-월-일 형식으로 변경한다.
            df = df.dropna()
            df[['close', 'diff', 'open', 'high', 'low', 'volume']] = df[['close',
                'diff', 'open', 'high', 'low', 'volume']].astype(int)              # 마리아디비에서 BIGINT형으로 지정한 컬럼들의 데이터형을 int형으로 변경한다.
            df = df[['date', 'open', 'high', 'low', 'close', 'diff', 'volume']]    # 원하는 순서로 컬럼을 재조합하여 데이터프레임을 만든다.
        except Exception as e:
            self.myslack.post_message(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}]\n ▶Exception occurred : {str(e)}")
            return None

        return df

    def replace_into_db(self, df, num, code, company):
        """네이버 금융에서 읽어온 주식 시세를 DB에 REPLACE"""
        with self.conn.cursor() as curs:
            for r in df.itertuples():                                             # 인수로 넘겨받은 데이터프레임을 튜플로 순회처리한다.
                sql = f"REPLACE INTO daily_price VALUES ('{code}', "\
                    f"'{r.date}', {r.open}, {r.high}, {r.low}, {r.close}, "\
                    f"{r.diff}, {r.volume})"
                curs.execute(sql)                                                 # REPLACE INTO 구문으로 daily_price 테이블을 업데이트한다.
            self.conn.commit()                                                    # commit() 함수를 호출해 마리아디비에 반영한다.
            #print('[{}] #{:04d} {} ({}) : {} rows > REPLACE INTO daily_price [OK]'.format(datetime.now().strftime('%Y-%m-%d %H:%M'), num+1, company, code, len(df)))

    def update_daily_price(self, pages_to_fetch):
        """KRX 상장법인의 주식 시세를 네이버로부터 읽어서 DB에 업데이트"""
        okcount = 0;
        ngcount = 0;
        strNGList = []
        for idx, code in enumerate(self.codes):                                  # self.codes 딕셔너리에 저장된 모든 종목코드에 대해 순회처리한다.
            df = self.read_naver(code, self.codes[code], pages_to_fetch)         # read_naver() 메서드를 이용하여 종목코드에 대한 일별 시세 데이터 프레임을 구한다.
            if df is None:
                ngcount = ngcount + 1
                strNGList.append(self.codes[code])
                continue
            else:
                self.replace_into_db(df, idx, code, self.codes[code])                # 일별 시세 데이터프레임이 구해지면 replace_into_db() 메서드로 DB에 저장한다.
                okcount = okcount + 1
        self.myslack.post_message(
            f"[{time.strftime('%Y-%m-%d %H:%M:%S')}]\n ▶update_daily_price\n ▶TOTAL: {len(self.codes)}\n ▶OK: {okcount}\n ▶NG: [{ngcount}ea] {strNGList}")

    def execute_daily(self):
        """실행 즉시 및 매일 오후 5시에 daily_price 테이블 업데이트"""
        self.update_comp_info()                                                  # update_comp_info() 메서드를 호출하여 상장 법인 목록을 DB에 업데이트한다.
        try:
            with open('config.json', 'r') as in_file:                            # DBUpdater.py가 있는 디렉터리에서 config.json 파일을 읽기 모드로 연다.
                config = json.load(in_file)
                pages_to_fetch = config['pages_to_fetch']                        # 파일이 있다면 pages_to_fetch값을 읽어서 프로그램에서 사용한다.
        except FileNotFoundError:                                                # 위에서 열려고 시도했던 config.json 파일이 존재하지 않는 경우
            with open('config.json', 'w') as out_file:
                pages_to_fetch = 100                                             # 최초 실행 시 프로그램에서 사용할 pages_to_fetch값을 100으로 설정한다 (config.json파일에 page_to_fetch값을 1로 저장해서 이후부터는 1페이지씩 읽음)
                config = {'pages_to_fetch': 1}
                json.dump(config, out_file)
        self.update_daily_price(pages_to_fetch)                                  # pages_to_fetch값으로 update_daily_price() 메서드를 호출한다.

        tmnow = datetime.now()
        lastday = calendar.monthrange(tmnow.year, tmnow.month)[1]                # 이번 달의 마지막 날(lastday)을 구해 다음 날 오후 5시를 계산하는데 사용한다.
        if tmnow.month == 12 and tmnow.day == lastday:
            tmnext = tmnow.replace(year=tmnow.year+1, month=1, day=1, 
                hour=17, minute=0, second=0)
        elif tmnow.day == lastday:
            tmnext = tmnow.replace(month=tmnow.month+1, day=1, hour=17, 
                minute=0, second=0)
        else:
            tmnext = tmnow.replace(day=tmnow.day+1, hour=17, minute=0,
                second=0)
        
        tmdiff = tmnext - tmnow
        secs = tmdiff.seconds

        t = Timer(secs, self.execute_daily)                                     # 다음 날 오후5시에 execute_daily() 메서드를 실행하는 타이머(Timer) 객체를 생성한다.
        self.myslack.post_message(
            f"[{time.strftime('%Y-%m-%d %H:%M:%S')}]\n ▶Waiting for next update ({tmnext.strftime('%Y-%m-%d %H:%M')})...")
        #print("Waiting for next update ({}) ... ".format(tmnext.strftime('%Y-%m-%d %H:%M')))
        t.start()


if __name__ == '__main__':
    dbu = DBUpdater()                                                           # DBUpdater.py가 단독으로 실행되면 DBUpdater 객체를 생성한다.
    #dbu.update_comp_info()                                                      # company_info 테이블에 오늘 업데이트된 내용이 있는지 확인하고, 없으면 'read_krx_code'를 호출하여 company_info 테이블에 업데이트하고 codes 딕셔너리에도 저장한다.
    dbu.execute_daily()
