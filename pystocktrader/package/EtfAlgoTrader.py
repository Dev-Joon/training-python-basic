# ch08_03_EtfAlgoTrader.py
import ctypes
import win32com.client
import requests
from datetime import datetime 
#import AutoConnect

# CREON Plus 공통 Object
cpStatus = win32com.client.Dispatch('CpUtil.CpCybos')       # 시스템 상태 정보
cpTradeUtil = win32com.client.Dispatch('CpTrade.CpTdUtil')  # 주문 관련 도구

# CREON Plus 시스템 점검 함수
def check_creon_system():
    # 관리자 권한으로 프로세스 실행 여부
    if not ctypes.windll.shell32.IsUserAnAdmin():
        print('check_creon_system() : admin user -> FAILED')
        return False
    
    # 연결 여부 체크
    if (cpStatus.IsConnect == 0):
        print('check_creon_system() : connect to server -> FAILED')
        return False
    
    # 주문 관련 초기화
    if (cpTradeUtil.TradeInit(0) != 0):
        print('check_creon_system() : init trade -> FAILED')
        return False
    
    return True

cpStock = win32com.client.Dispatch('DsCbo1.StockMst')   # 주식 종목별 정보
def get_current_price(code):
    cpStock.SetInputValue(0, code)  # 종목코드에 대한 가격 정보
    cpStock.BlockRequest()
    
    item = {}
    item['cur_price'] = cpStock.GetHeaderValue(11)  # 현재가
    item['ask'] = cpStock.GetHeaderValue(16)        # 매수호가
    item['bid'] = cpStock.GetHeaderValue(17)        # 매도호가
    
    return item['cur_price'], item['ask'], item['bid']
    

cpOhlc = win32com.client    


channel = '#stocktrader'
token = 'xoxb-2470620632881-2458007691330-76TFWj1JIDeZ6Q90mpkCHPrA'

def dbgout(message):
    print(datetime.now().strftime('[%m/%d %H:%M:%S]'), message)
    strbuf = datetime.now().strftime('[%m/%d %H:%M:%S] ') + message
    response = requests.post("https://slack.com/api/chat.postMessage",
                                headers={"Authorization": "Bearer " + token},
                                data={"channel": channel, "text": strbuf}
                                )

if __name__ == '__main__':
    # AutoConnect.AutoConnect()
    if check_creon_system() is True:
        print('check_creon_system() : OK')
    
    obj = win32com.client.Dispatch('DsCbo1.StockMst')   # 주식마스터 (StockMst) COM 객체를 생성한다.
    obj.SetInputValue(0, 'A005930')                     # SetInputValue() 함수로 조회할 데이터를 삼성전자(A005930)로 지정한다.
    obj.BlockRequest()                                  # BlockRequest() 함수로 삼성전자에 대한 블록 데이터를 요청한다.
    sec = {}
    sec['현재가'] = obj.GetHeaderValue(11)               # GetHeaderValue() 함수로 현재가 정보(11)를 가져와서 sec 딕셔너리에 넣는다. 
    sec['전일대비'] = obj.GetHeaderValue(12)             # GetHeaderValue() 함수로 전일대비 가격변동 정보(12)를 가져와서 sec 딕셔너리에 넣는다.
    
    print(sec)
    
    print(get_current_price('A305080'))
    
    # dbgout('This is test log.')
    