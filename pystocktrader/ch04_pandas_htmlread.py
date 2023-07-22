import pandas as pd

krx_list = pd.read_html('C:/Dev/MyStock/study/상장법인목록.xls')
print(type(krx_list))
print('********************')
print(type(krx_list[0]))

df = pd.read_html('https://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13')[0]
df['종목코드'] = df['종목코드'].map('{:06d}'.format)
df = df.sort_values(by='종목코드', ascending=False)
print(df)
