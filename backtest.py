import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

spy = yf.Ticker("SPY")
data = yf.download("SPY", start="2020-01-01", end=datetime.today().strftime('%Y-%m-%d'), interval="1wk")
cumulative_returns = ((data['Close'] / data['Close'].iloc[0])*100) - 100
print(cumulative_returns)

plt.figure(figsize=(10, 6))
plt.plot(cumulative_returns.index, cumulative_returns, label='Cumulative Returns')
plt.title('Cumulative Returns of SPY')
plt.show()
