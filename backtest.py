import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt

ticker = "SPY"
start_date = "2000-01-01"
end_date = dt.datetime.today().strftime('%Y-%m-%d')
#end_date = "2010-01-01"
lower_ma = 30
upper_ma = 50

def get_date_x_weeks_before(date_string, num_weeks_before):
    date_object = dt.datetime.strptime(date_string, "%Y-%m-%d")
    new_date = date_object - dt.timedelta(weeks=num_weeks_before)
    return new_date.strftime("%Y-%m-%d")

data = yf.download(ticker, start=get_date_x_weeks_before(start_date, upper_ma), end=end_date, interval="1wk")
data['MA30'] = data['Close'].rolling(window=lower_ma).mean()
data['MA50'] = data['Close'].rolling(window=upper_ma).mean()
data = data[data.index >= start_date]
data['signal'] = np.where(data['MA30'] > data['MA50'], 1, 0)
data['crossover'] = data['signal'].diff()
cumulative_returns = ((data['Close'] / data['Close'].iloc[0])*100) - 100

plt.figure(figsize=(10, 6))
plt.plot(cumulative_returns.index, cumulative_returns, label='Cumulative Returns', color = 'green', linewidth=2)
plt.plot(data['MA30'], label='30-Week MA', color='blue', linestyle='--')
plt.plot(data['MA50'], label='50-Week MA', color='red', linestyle='--')
plt.xlabel('Date')
plt.ylabel('Cumulative Returns (%)')
plt.grid(True, linestyle='--', alpha=0.5)

plt.scatter(
    data.index[data['crossover'] == 1],
    data['Close'][data['crossover'] == 1],
    marker='^', color='green', s=100, label='Buy Signal'
)

plt.scatter(
    data.index[data['crossover'] == -1],
    data['Close'][data['crossover'] == -1],
    marker='v', color='red', s=100, label='Sell Signal'
)

plt.title('Cumulative Returns of SPY with Moving Averages')
plt.tight_layout()
plt.show()



