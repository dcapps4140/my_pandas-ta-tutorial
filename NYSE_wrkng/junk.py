import yfinance as yf
import pandas as pd
import pandas_ta as ta

# Define non-default RSI parameters
rsi_period = 7
rsi_wilder = False

# Set custom MACD parameters
fast_period = 12
slow_period = 26
signal_period = 9

stocklist = ['AAPL', 'MSFT', 'IBM', 'GOOG', 'A']
print("{}".format(stocklist))
df = pd.DataFrame()

for stock in stocklist:
    # #
    # n += 1
    # time.sleep(1)

    # if my_debug: 
    # print ("\nAnalyzing {} with iteration number {}".format(stock, n))
    # else:
    # print(n, end = "")

    ticker = yf.Ticker(stock)
    df = ticker.history(period="1y")
    # # 
    # if my_debug:print(df)

    adx = ta.adx(df['High'], df['Low'], df['Close'])

    adx = df.ta.adx()

    stoch = ta.stoch(df['High'], df['Low'], df['Close'], 14, 3, 3)#STOCHk_14_3_3  STOCHd_14_3_3

    macd = df.ta.macd(fast=fast_period, slow=slow_period, signal=signal_period)#MACD_12_26_9  MACDh_12_26_9  MACDs_12_26_9

    rsi = df.ta.rsi(rsi_period)

    df = pd.concat([df, adx, stoch, macd, rsi], axis=1)

    df = df[df['RSI_7'] < 30]

    last_row = df.iloc[-1]

    print("", last_row)