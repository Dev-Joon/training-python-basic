# KOSPI의 MDD 구하기

# ch03_01_KOSPI_MDD.py
from pandas_datareader import data as pdr
import yfinance as yf
yf.pdr_override()

import matplotlib.pyplot as plt

kospi = pdr.get_data_yahoo('^KS11', '2004-01-04')               # 1) KOSPI 지수 데이터를 다운로드 한다. KOSPI지수의 심볼은 ^KS11이다.

window = 252                                                    # 2) 산정 기간에 해당하는 window값은 1년 동안의 개장일을 252일로 어림잡아 설정했다.
peak = kospi['Adj Close'].rolling(window, min_periods=1).max()  # 3) KOSPI 종가 칼람에서 1년(거래일 기준) 기간 단위로 최고치 peak를 구한다.
drawdown = kospi['Adj Close']/peak - 1.0                        # 4) drawdown은 최고치(peak) 대비 현재 KOSPI 종가가 얼마나 하락했는지를 구한다.
max_dd = drawdown.rolling(window, min_periods=1).min()          # 5) drawdown에서 1년 기간 단위로 최저치 max_dd를 구한다. 마이너스값이기 때문에 최저치가 바로 최대 손실 낙폭이 된다.

max_dd_value = max_dd.min()
print(f'MDD : {max_dd_value}')
print(f'MDD Date : {max_dd[max_dd==max_dd_value]}')

plt.figure(figsize=(9, 7))
plt.subplot(211)    # 2행 1열 중 1행에 그린다.
kospi['Close'].plot(label='KOSPI', title='KOSPI MDD', grid=True, legend=True)

plt.subplot(212)    # 2행 1열 중 2행에 그린다.
drawdown.plot(c='blue', label='KOSPI DD', grid=True, legend=True)
max_dd.plot(c='red', label='KOSPI MDD', grid=True, legend=True)
plt.show()