import pandas as pd
from pandas_datareader import data as pdr
import yfinance as yf

yf.pdr_override()

dow = pdr.get_data_yahoo('^DJI', '2000-01-04')      # 1) 2000년 이후의 다우존스 지수(^DJI) 데이터를 야후 파이낸스로부터 다운로드한다.
kospi = pdr.get_data_yahoo('^KS11', '2000-01-04')   # 2) 2000년 이후의 KOSPI(^KS11) 데이터를 야후 파이낸스로부터 다운로드한다.

#d = (dow.Close / dow.Close.loc['2000-01-04']) * 100     # 지수화
#k = (kospi.Close / kospi.Close.loc['2000-01-04']) * 100 # 지수화

df = pd.DataFrame({'DOW': dow['Close'], 'KOSPI': kospi['Close']})   #다우존스 지수의 종가 컬럼과 코스피 지수의 종가 컬럼으로 데이터프레임을 생성
df = df.fillna(method='bfill')  # 모든 NaN을 제거
df = df.fillna(method='ffill')
#print(df)

from scipy import stats
regr = stats.linregress(df['DOW'], df['KOSPI'])
print(regr)

import matplotlib.pyplot as plt
# plt.figure(figsize=(9, 5))
# plt.plot(d.index, d, 'r--', label='Dow Jones Industrial Average') # 3) 다우존스 지수를 붉은 점선으로 출력한다.
# plt.plot(k.index, k, 'b', label='KOSPI')              # 4) KOSPI를 푸른 실선으로 표시한다.
# plt.grid(True)
# plt.legend(loc='best')
# plt.show()
plt.figure(figsize=(7, 7))
plt.scatter(df['DOW'], df['KOSPI'], marker='.')     # 다우존스 지수를 x로, KOSPI 지수를 y로 산점도를 그리되, 점은 작은 원(.) 모양으로 표시한다.
plt.xlabel('Dow Jones Industrial Average')
plt.ylabel('KOSPI')
plt.show()