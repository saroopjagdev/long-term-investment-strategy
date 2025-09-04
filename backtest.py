import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime as dt

ticker = "SPY"
start_date = "2000-01-01"
end_date = dt.today().strftime('%Y-%m-%d')

data = yf.download(ticker, start=start_date, end=end_date, interval="1wk")
cumulative_returns = ((data['Close'] / data['Close'].iloc[0])*100) - 100

data['MA30'] = data['Close'].rolling(window=30).mean()
data['MA50'] = data['Close'].rolling(window=50).mean()

plt.figure(figsize=(10, 6))
plt.plot(cumulative_returns.index, cumulative_returns, label='Cumulative Returns', color = 'green', linewidth=2)
plt.plot(data['MA30'], label='30-Week MA', color='blue', linestyle='--')
plt.plot(data['MA50'], label='50-Week MA', color='red', linestyle='--')
plt.xlabel('Date')
plt.ylabel('Cumulative Returns (%)')
plt.grid(True, linestyle='--', alpha=0.5)
plt.title('Cumulative Returns of SPY with Moving Averages')
plt.tight_layout()
plt.show()



