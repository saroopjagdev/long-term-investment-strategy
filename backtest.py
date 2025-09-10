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
cash_annual_return = 0.05
cash_weekly_return = (1 + cash_annual_return)**(1/52) - 1

def get_date_x_weeks_before(date_string, num_weeks_before):
    date_object = dt.datetime.strptime(date_string, "%Y-%m-%d")
    new_date = date_object - dt.timedelta(weeks=num_weeks_before)
    return new_date.strftime("%Y-%m-%d")

data = yf.download(ticker, start=get_date_x_weeks_before(start_date, upper_ma), end=end_date, interval="1wk")

def plot_ma_strategy(data, lower_ma, upper_ma, start_date, cash_weekly_return, scatter=False, base=False, ax=None, label_strategy=None):
    data = data.copy()
    data['MA_lower'] = data['Close'].rolling(window=lower_ma).mean()
    data['MA_upper'] = data['Close'].rolling(window=upper_ma).mean()
    data = data[data.index >= start_date]
    data['signal'] = np.where(data['MA_lower'] > data['MA_upper'], 1, 0)
    data['crossover'] = data['signal'].diff()
    data['returns'] = data['Close'].pct_change()
    data['strategy_returns'] = np.where(
        data['signal'].shift(1) == 1,
        data['returns'],
        cash_weekly_return
    )
    data['strategy'] = ((1 + data['strategy_returns']).cumprod() - 1) * 100

    if ax is None:
        fig, ax = plt.subplots(figsize=(10,6))

    if base:
        data['buy_and_hold'] = ((1 + data['returns']).cumprod() - 1) * 100
        ax.plot(data.index, data['buy_and_hold'], label='Buy & Hold', color='green')


    label = label_strategy if label_strategy is not None else f"{lower_ma}/{upper_ma}"
    ax.plot(data.index, data['strategy'], label=label, alpha=0.7)


    if scatter:
        ax.scatter(
            data.index[data['crossover'] == 1],
            data['strategy'][data['crossover'] == 1],
            marker='^', color='green', s=100, label='Buy Signal'
        )
        ax.scatter(
            data.index[data['crossover'] == -1],
            data['strategy'][data['crossover'] == -1],
            marker='v', color='red', s=100, label='Sell Signal'
        )

    ax.set_xlabel('Date')
    ax.set_ylabel('Cumulative Returns (%)')
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.set_title('Cumulative Returns of Strategy')

    return ax, data


ax, _ = plot_ma_strategy(data, 4, 38, start_date, cash_weekly_return, scatter=True, base=True)
ax.legend()

ax = plt.subplots(figsize=(12,6))[1]

results = []

for lower_ma in range(1, 25):
    for upper_ma in range(lower_ma+1, 50):
        _, temp_data = plot_ma_strategy(
            data, lower_ma, upper_ma, start_date, cash_weekly_return, scatter=False, base=False, ax=ax)
        final_value = temp_data['strategy'].iloc[-1]
        results.append({
            'lower_ma': lower_ma,
            'upper_ma': upper_ma,
            'final_value': final_value
        })

results_df = pd.DataFrame(results)


ax.legend()
plt.show()

top_20 = results_df.sort_values(by='final_value', ascending=False).head(20)
print("Top 20 performing MA combos:")
print(top_20)


bottom_20 = results_df.sort_values(by='final_value', ascending=True).head(20)
print("\nBottom 20 performing MA combos:")
print(bottom_20)