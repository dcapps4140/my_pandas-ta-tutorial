import ta
import pandas_ta as ta
import yfinance as yf
import pandas as pd
from yahoo_fin import stock_info as si
from halo import Halo
import pyodbc

#Define your database connection string parameters
server = 'DESKTOP-7ARJ1N3\SQLEXPRESS'
database = 'stocks'
table_name = 'StockSymbols'
column_name = 'Symbol'
username = 'vscode'
password = 'development'

# Use the Halo library to display a spinning loading animation
spinner = Halo(text='Retrieving stock information...', spinner='dots')
spinner.start()

# Create an empty dataframe to store the stock information
df = pd.DataFrame()

# Connect to the MS SQL Server database
# Define your database connection string
# Connect to the database
conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                    'SERVER=' + server + ';'
                    'DATABASE=' + database + ';'
                    'UID=' + username + ';'
                    'PWD=' + password)
# Create a cursor
cursor = conn.cursor()

# Retrieve all stock ticker data from the NYSE
cursor.execute("SELECT {} FROM {}".format(column_name, table_name))
symbols = cursor.fetchall()

# Process each stock ticker

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
