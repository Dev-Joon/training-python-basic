from Investar import Analyzer
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

mk = Analyzer.MarketDB()
stocks = ['삼성전자', 'SK하이닉스', '현대자동차', 'NAVER']
df = pd.DataFrame()

for s in stocks:
    df[s] = mk.get_daily_price(s, '2020-01-01', '2021-09-08')['close']

# print(df)

# 시총 상위 4종목의 수익률을 비교하려면 종가 대신 일간 변동률로 비교를 해야 하기 때문에
# 데이터프레임에서 제공하는 pct_change() 함수를 사용해 4종목의 일간 변동률을 구한다.
daily_ret = df.pct_change()

# 일간 변동률의 평균값에 252를 곱해서 연간 수익률을 구한다. 252는 미국의 1년 평균 개장일로,
# 우리나라 실정에 맞게 다른 숫자로 바꾸어도 무방하다.
annual_ret = daily_ret.mean() * 252

# 일간 리스크는 cov() 함수를 사용해 일간 변동률의 공분산으로 구한다.
daily_cov = daily_ret.cov()

# 연간 공분산은 일간 공분산에 252를 곱해 계산한다.
annual_cov = daily_cov * 252


# 시총 상위 4종목 비중을 다르게 해 포트폴리오 20,000개를 생성한다.
# 포트폴리오 수익률, 리스크, 종목 비중을 저장할 각 리스크를 생성한다.
port_ret = []
port_risk = []
port_weights = []
sharpe_ratio = []

for _ in range(20000):                                      # 포트폴리오 20,000개를 생성하는데 range() 함수와 for in 구문을 사용했다. for in 구문에서 반복횟수를 사용할 일이 없으면 관습적으로 _ 변수에 할당한다.
    weights = np.random.random(len(stocks))                 # 4개의 랜덤 숫자로 구성된 배열을 생성한다.
    weights /= np.sum(weights)                              # 위에서 구한 4개의 랜덤 숫자를 랜덤 숫자의 총합으로 나눠 4종목 비중의 합이 1이 되도록 조정한다.

    returns = np.dot(weights, annual_ret)                           # 랜덤하게 생성한 종목별 비중 배열과 종목별 연간 수익률을 곱해 해당 포트폴리오 전체 수익률(returns)을 구한다.
    risk = np.sqrt(np.dot(weights.T, np.dot(annual_cov, weights)))  # 종목별 연간 공분산과 종목별 비중 배열을 곱한 뒤 이를 다시 종목별 비중의 전치(transpose)로 곱한다. 이렇게 구한 결과값의 제곱근을 sqrt() 함수로 구하면 해당 포트폴리오 전체 리스크(Risk)를 구할 수 있다.

    # 포트폴리오 20,000개 수익률, 리스크, 종목별 비중을 각각 리스트에 추가한다.
    port_ret.append(returns)
    port_risk.append(risk)
    port_weights.append(weights)
    sharpe_ratio.append(returns/risk)   # 포트폴리오의 수익률을 리스크로 나눈 값을 샤프 지수 리스트에 추가한다.

portfolio = {'Returns': port_ret, 'Risk': port_risk, 'Sharpe': sharpe_ratio}

# i값은 0, 1, 2, 3순으로 변한다.
# 이떄 s값은 '삼성전자', 'SK하이닉스', '현대자동차', 'NAVER'순으로 변한다.
for i, s in enumerate(stocks):
    # portfolio 딕셔너리에 '삼성전자', 'SK하이닉스', '현대자동차', 'NAVER'키 순서로 비중값을 추가한다.
    portfolio[s] = [weight[i] for weight in port_weights]

df = pd.DataFrame(portfolio)
# 최종 생성된 df 데이터프레임을 출력하면, 시총 상위 4 종목의 보유 비율에 따라
# 포트폴리오 20,000개가 각기 다른 리스크와 예상 수익률을 가지는 것을 확인 할수 있다.
df = df[['Returns', 'Risk', 'Sharpe'] + [s for s in stocks]]     # 샤프 지수 칼럼을 데이터프레임에 추가한다.

max_sharp = df.loc[df['Sharpe'] == df['Sharpe'].max()]  # 샤프 지수 칼럼에서 샤프 지숫값이 제일 큰 행을 max_sharpe로 정한다.
min_risk = df.loc[df['Risk'] == df['Risk'].min()]   # 리스크 칼럼에서 리스크값이 제일 작은 행을 min_risk로 정한다.

print(df)

# 포트폴리오의 샤프 지수에 따라 컬러맵을 'viridis'로 표시하고 테두리는 검정(k)로 표시한다.
df.plot.scatter(x='Risk', y='Returns', c='Sharpe', cmap='viridis', edgecolors='k', figsize=(10, 7), grid=True)
# 샤프 지수가 가장 큰 포트폴리오를 300 크기의 붉은 별표로 표시한다.
plt.scatter(x=max_sharp['Risk'], y=max_sharp['Returns'], c='r', marker='*', s=300)
# 리스크가 제일 작은 포트폴리오를 200 크기의 붉은 엑스표로 표시한다.
plt.scatter(x=min_risk['Risk'], y=min_risk['Returns'], c='r', marker='X', s=200)
plt.title('Portfolio Optimization')
plt.xlabel('Risk')
plt.ylabel('Expected Returns')
plt.show()

print(max_sharp)
print(min_risk)