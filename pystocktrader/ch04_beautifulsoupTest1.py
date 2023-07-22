import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen
url = 'https://finance.naver.com/item/sise_day.nhn?code=068270&page=1'
with urlopen(url) as doc:
    html = BeautifulSoup(doc, 'lxml')       # 1. 뷰티풀 수프 생성자의 첫 번째 인수로 HTML/XML페이지의 파일 경로나 URL을 넘겨주고, 두 번째 인수로 웹페이지를 파싱할 방식을 넘겨준다.
    pgrr = html.find('td', class_='pgRR')   # 2. find함수를 통해서 class속성이 'pgRR'인 td태그를 찾으면, 결과값은 'bs4.element.Tag'타입으로 prgg변수에 반환된다.
                                            #    'pgRR'은 Page Right Right 즉, 맨 마지막(오른쪽) 페이지를 의미한다.
                                            #    find()함수의 인수인 class 속성을 굳이 class_로 적은 이유는 파이썬에 이미 class라는 지시어가 존재하기 때문에,
                                            #    인터프리터가 구분할 수 있도록 하기 위함이다.
    #print(pgrr.a['href'])

###############################################################################
df = pd.DataFrame()                                         # 1. 일별 시세를 저장할 df변수가 데이터프레임형임을 인터프리터에 알려준다.
sise_url = 'https://finance.naver.com/item/sise_day.nhn?code=068270'

for page in range(1, 401):                                  # 2. 1페이지부터 last_page(400페이지)까지 반복한다.
    page_url = '{}&page={}'.format(sise_url, page)          # 3. for문의 page숫자를 이용하여 요청할 URL페이지 수를 변경한다.
    df = df.append(pd.read_html(page_url, header=0)[0])     # 4. read_hteml() 함수로 읽은 한 페이지 분량의 데이터프레임을 df객체에 추가한다.

df = df.dropna()                                            # 5. 값이 빠진 행을 제거한다.

print(df)