
import pandas_ta as ta
import yfinance as yf
import pandas as pd
from halo import Halo

# Use the Halo library to display a spinning loading animation
spinner = Halo(text='Retrieving stock information...', spinner='dots')
# Define non-default RSI parameters
RSI_PERIOD = 7
RSI_WILDER = False

# Set custom MACD parameters
FAST_PERIOD = 12
SLOW_PERIOD = 26
SIGNAL_PERIOD = 9
#

# Create an empty dataframe to store the stock information
df = pd.DataFrame()
df = yf.download('^GSPC', start='1985-01-01')

stoch = ta.stoch(df['High'], df['Low'], df['Close'], 14, 3, 3)#STOCHk_14_3_3  STOCHd_14_3_3
macd = df.ta.macd(fast=FAST_PERIOD, slow=SLOW_PERIOD, signal=SIGNAL_PERIOD)#MACD_12_26_9  MACDh_12_26_9  MACDs_12_26_9
rsi = df.ta.rsi(RSI_PERIOD)
df = pd.concat([df, stoch, macd, rsi], axis=1)

print(df.tail(10))
# print(df.shape)
# print(df.info())
spinner.stop()
