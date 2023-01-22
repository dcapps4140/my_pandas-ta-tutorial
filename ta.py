import yfinance as yf
import pandas_ta as ta
import pandas as pd

# Define non-default RSI parameters
rsi_period = 7
rsi_wilder = False

# Set custom MACD parameters
fast_period = 12
slow_period = 26
signal_period = 9
#
# Get Data
ticker = yf.Ticker("AAL")
df = ticker.history(period="1y")
# 
#print(df)

adx = ta.adx(df['High'], df['Low'], df['Close'])

adx = df.ta.adx()

stoch = ta.stoch(df['High'], df['Low'], df['Close'], 14, 3, 3)#STOCHk_14_3_3  STOCHd_14_3_3

macd = df.ta.macd(fast=fast_period, slow=slow_period, signal=signal_period)#MACD_12_26_9  MACDh_12_26_9  MACDs_12_26_9

rsi = df.ta.rsi(rsi_period)

df = pd.concat([df, adx, stoch, macd, rsi], axis=1)

df = df[df['RSI_7'] < 30]

print(ticker)
print()
last_row = df.iloc[-1]

if last_row['STOCHk_14_3_3'] >= 50:
    message = f"!Possible Uptrend: The Stoch %k is {last_row['STOCHk_14_3_3']:.2f}"
    print(message)
else:
    message = f"The Stoch %k is {last_row['STOCHk_14_3_3']:.2f}"
    print(message)
    
if last_row['RSI_7'] >= 50:
    message = f"!Possible Uptrend: The RSI_7 is {last_row['RSI_7']:.2f}"
    print(message)
else:
    message = f"The RSI_7 is {last_row['RSI_7']:.2f}"
    print(message)

if last_row['MACD_12_26_9'] > last_row['MACDs_12_26_9']:
    message = f"!Possible Uptrend: The MACD > Sig is {last_row['MACD_12_26_9']:.2f}"
    print(message)
else:
    message = f"The MACD_12_26_9 is {last_row['MACD_12_26_9']:.2f}"
    print(message)
