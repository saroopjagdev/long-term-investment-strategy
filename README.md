# long-term-investment-strategy

Backtest of a long-term trend-following strategy on SPY using weekly data from `yfinance`.

The strategy holds the index when a lower moving average (default 30 weeks) is above an upper one (default 50 weeks) and otherwise sits in cash earning a fixed annual rate (default 5%). `backtest.py` compares it with buy-and-hold and sweeps MA window pairs, with a 3D plot of results.

## Run
```
pip install yfinance pandas numpy matplotlib
python backtest.py
```
Parameters (`ticker`, `start_date`, `lower_ma`, `upper_ma`, `cash_annual_return`) are at the top of the script. Based on a strategy by Mark Shipman. Backtests are not predictive and this is not financial advice.
