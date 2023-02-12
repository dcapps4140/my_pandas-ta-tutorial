import pandas as pd
import pandas_ta as ta
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

# Download the data for the S&P 500 ^GSPC index for the past year
ticker = '^GSPC'
df = yf.download(ticker, start='2022-02-12', end='2023-02-12')
df = df.drop(columns=['Adj Close'])
df = df.dropna()
print(df.head(5))
# Calculate the average daily range (ADR)
df['ADR'] = (df['High'] - df['Low']) / 7

# Add the RSI, Stochastics, and MACD indicators to the dataframe
df['RSI'] = ta.rsi(df['Close'], timeperiod=7)
df = df.dropna()
print(df.head(10))
stoch_k = ta.stoch(df['High'], df['Low'], df['Close'], fastk_period=14, slowk_period=3, slowd_period=3)[0]
df['STOCH'] = stoch_k
df['MACD'], df['MACD_Signal'], df['MACD_Hist'] = ta.macd(df['Close'], fastperiod=12, slowperiod=26, signalperiod=9)

# Initialize variables for the backtesting
initial_capital = 10000
capital = initial_capital
stop_loss = 0.02 * initial_capital
positions = 0
entry_price = 0
exit_price = 0
entry_date = ''
exit_date = ''
trades = []

# Backtesting loop
for date, row in df.iterrows():
    # Entry logic
    if (row['RSI'] > 50) and (row['STOCH'] > 50) and (row['MACD'] > row['MACD_Signal']):
        # Enter a long position
        entry_price = row['Close']
        entry_date = date
        positions = capital / entry_price
        capital -= positions * entry_price
        exit_price = 0
        exit_date = ''

    # Exit logic
    if (exit_price == 0) and (entry_price != 0) and ((entry_price - row['Close']) > stop_loss or (row['RSI'] < 50) or (row['STOCH'] < 50) or (row['MACD'] < row['MACD_Signal'])):
        # Exit the long position
        exit_price = row['Close']
        exit_date = date
        capital += positions * exit_price
        positions = 0
        trade = {
            'entry_date': entry_date,
            'exit_date': exit_date,
            'entry_price': entry_price,
            'exit_price': exit_price,
            'profit': (exit_price - entry_price) * positions
        }
        trades.append(trade)
        entry_price = 0
        entry_date = ''

#Calculate the strategy returns and add to the dataframe
df['strategy_return'] = 0.0
for trade in trades:
    entry_index = df.index.get_loc(trade['entry_date'])
    exit_index = df.index.get_loc(trade['exit_date'])
    df.loc[df.index[entry_index:exit_index+1], 'strategy_return'] = trade['profit'] / initial_capital

#Calculate the results
total_profit = capital - initial_capital
win_trades = [t for t in trades if t['profit'] > 0]
win_rate = len(win_trades) / len(trades) if len(trades) > 0 else 0
average_win = np.mean([t['profit'] for t in win_trades]) if len(win_trades) > 0 else 0
average_loss = np.mean([t['profit'] for t in trades if t['profit'] < 0]) if len([t for t in trades if t['profit'] < 0]) > 0 else 0

#Calculate the strategy returns
df['strategy_return'] = df['strategy_return'].cumsum()
df['cumulative_return'] = (df['strategy_return'] + 1).cumprod()

#Plot the results
plt.figure(figsize=(15,5))
plt.plot(df.index, df['cumulative_return'])
plt.title("Backtest of Trading Strategy")
plt.xlabel("Year")
plt.ylabel("Cumulative Return")
plt.show()

#Calculate the strategy statistics
cumulative_return = df['cumulative_return'].iloc[-1]
returns = df['strategy_return']
sharpe_ratio = sharpe_ratio(returns)
max_drawdown = max_drawdown(cumulative_return)

print("Cumulative Return: ", cumulative_return)
print("Sharpe Ratio: ", sharpe_ratio)
print("Max Drawdown: ", max_drawdown)