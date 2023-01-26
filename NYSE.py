import ta
import pandas_ta as ta
import yfinance as yf
import pandas as pd
from yahoo_fin import stock_info as si
from halo import Halo

# gather stock symbols from major US exchanges
df1 = pd.DataFrame( si.tickers_sp500() )
df2 = pd.DataFrame( si.tickers_nasdaq() )
df3 = pd.DataFrame( si.tickers_dow() )
df4 = pd.DataFrame( si.tickers_other() )

# convert DataFrame to list, then to sets
sym1 = set( symbol for symbol in df1[0].values.tolist() )
sym2 = set( symbol for symbol in df2[0].values.tolist() )
sym3 = set( symbol for symbol in df3[0].values.tolist() )
sym4 = set( symbol for symbol in df4[0].values.tolist() )

# join the 4 sets into one. Because it's a set, there will be no duplicate symbols
symbols = set.union( sym1, sym2, sym3, sym4 )

# Some stocks are 5 characters. Those stocks with the suffixes listed below are not of interest.
my_list = ['W', 'R', 'P', 'Q']
del_set = set()
sav_set = set()

for symbol in symbols:
    if len( symbol ) > 4 and symbol[-1] in my_list:
        del_set.add( symbol )
    else:
        sav_set.add( symbol )

print( f'Removed {len( del_set )} unqualified stock symbols...' )
print( f'There are {len( sav_set )} qualified stock symbols...' )

# Use the Halo library to display a spinning loading animation
spinner = Halo(text='Retrieving stock information...', spinner='dots')
spinner.start()

# Create an empty dataframe to store the stock information
df = pd.DataFrame()

# Retrieve stock information for all NYSE stocks
for symbol in symbols:
    stock = yf.Ticker(symbol)
    df_temp = stock.history(period="max")
    df_temp = ta.add_all_ta_features(df_temp, "open", "high", "low", "close", "volume", fillna=True)
    df = pd.concat([df, df_temp])

# Stop the spinner
spinner.stop()

# Filter the dataframe for stocks that have a Stochastic %k greater than 50, RSI greater than 50, and MACD above the MACD signal
df_filtered = df[(df['stoch_k'] > 50) & (df['rsi'] > 50) & (df['macd'] > df['macd_signal'])]

# Print the symbol of the filtered stocks
print(df_filtered['symbol'].unique())
