from urllib import parse
from ast import literal_eval

import pandas as pd
import requests

def get_sise(code, start_time, end_time, time_from='day'):
    get_param = {
        'symbol':code,
        'requestType':1,
        'startTime':start_time,
        'endTime':end_time,
        'timeframe':time_from
    }
    get_param = parse.urlencode(get_param)
    url = 'https://api.finance.naver.com/siseJson.naver?%s'%(get_param)
    response = requests.get(url)
    return literal_eval(response.text.strip())

#df = pd.DataFrame()
# df = get_sise('005930', '20210601', '20210605', 'day')
# print(df)
Column = ['시가', '고가', '저가', '종가', '거래량', '외국인소진율']

index = []
rows = []
for list in get_sise('005930', '20210601', '20210605', 'day')[1:]:
    index.append(list[0])
    rows.append([list[1],list[2],list[3],list[4],list[5],list[6]])

df = pd.DataFrame(rows, columns=Column, index=index)
print(df)




#print(get_sise('005930', '20210601', '20210605', 'day'))