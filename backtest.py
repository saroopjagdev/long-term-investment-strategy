import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

ticker = "SPY"
data = yf.download(ticker, start="2000-01-01", end=datetime.today().strftime('%Y-%m-%d'), interval="1wk")
cumulative_returns = ((data['Close'] / data['Close'].iloc[0])*100) - 100
print(cumulative_returns)

plt.figure(figsize=(10, 6))
plt.plot(cumulative_returns.index, cumulative_returns, label='Cumulative Returns', color = 'green', linewidth=2)
plt.xlabel('Date')
plt.ylabel('Cumulative Returns (%)')
plt.grid(True, linestyle='--', alpha=0.5)
plt.title('Cumulative Returns of SPY (Buy and Hold Strategy)')
plt.tight_layout()
plt.show()