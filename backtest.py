import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

spy = yf.Ticker("SPY")
spy_historical = spy.history(start="2025-09-02", end="2025-09-03", interval="15m")
data = yf.download("SPY", start="2025-09-02", end="2025-09-03", interval="15m")
print(data)
