import pyodbc, sys
import ta, time
import pandas_ta as ta
import yfinance as yf
import pandas as pd
from yahoo_fin import stock_info as si
from halo import Halo
from datetime import datetime

#Define your database connection string parameters
server = 'DESKTOP-7ARJ1N3\SQLEXPRESS'
database = 'stocks'
table_name = 'StockSymbols'
table_name_2 = 'StockData'
column_name = 'Symbol'
username = 'vscode'
password = 'development'

date = datetime.today().strftime('%Y-%m-%d-%H-%M')

# Define non-default RSI parameters
rsi_period = 7
rsi_wilder = False

# Set custom MACD parameters
fast_period = 12
slow_period = 26
signal_period = 9
#
def tuple_to_list(t):
    return [list(x) for x in t]

def flatten(l):
    return [item for sublist in l for item in sublist]

def database_exists(conn, db_name):
    cursor = conn.cursor()
    cursor.execute("SELECT name from sys.databases WHERE name = '{}'".format(db_name))
    result = cursor.fetchall()
    cursor.close()
    return len(result) > 0

def table_exists(conn, table_name):
    cursor = conn.cursor()
    cursor.execute("SELECT name from sys.tables WHERE name = '{}'".format(table_name))
    result = cursor.fetchall()
    cursor.close()
    return len(result) > 0

# # record start time
start = time.time()
# Use the Halo library to display a spinning loading animation
spinner = Halo(text='Retrieving stock information...', spinner='dots')
#spinner.start()

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

# Create a database and table for the stock symbols data
# Create the database if it doesn't exist
if not database_exists(conn, database):
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE {}".format(database))
    cursor.close()
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                          'SERVER=' + server + ';'
                          'DATABASE=' + database + ';'
                          'UID=' + username + ';'
                          'PWD=' + password)

# Create the table if it doesn't exist
table_create_sql = "CREATE TABLE {} (Symbol varchar(10) NOT NULL PRIMARY KEY)".format(table_name)
if not table_exists(conn, table_name):
    cursor = conn.cursor()
    cursor.execute(table_create_sql)
    cursor.close()

table_create_sql = "CREATE TABLE {} (Symbol varchar(10) NOT NULL PRIMARY KEY)".format(table_name_2)
if not table_exists(conn, table_name_2):
    cursor = conn.cursor()
    cursor.execute(table_create_sql)
    cursor.close()

# Create an empty dataframe to store the stock information
df = pd.DataFrame()

# Retrieve all stock ticker data from the NYSE
cursor.execute("SELECT {} FROM {}".format(column_name, table_name))
stocklist = cursor.fetchall()

#data is returned as a list of tuples, convert to list of lists
stocklist = tuple_to_list(stocklist)

#flatten list of lists to just a list
stocklist = flatten(stocklist)

# Process each stock ticker
try:
    # Retrieve stock information for all NYSE stocks
    for stock in stocklist:
        print("Ticker = {}".format(stock))
        try:
            ticker = yf.Ticker(stock)
            df = ticker.history(period="1y")
            # print(df['Close'])
            last_row = df.iloc[-1]
            # if last_row['Close'] >= 5 and last_row['Close'] <= 20:
            #     insert_sql = f"IF NOT EXISTS (SELECT Symbol FROM StockDatas WHERE Symbol='{ticker}') " \
            #      f"INSERT INTO StockSymbols (Symbol) VALUES ('{ticker}')"
            #     cursor.execute(insert_sql)
            #     print('in Close')
            #     adx = ta.adx(df['High'], df['Low'], df['Close'])
            #     adx = df.ta.adx()
            #     stoch = ta.stoch(df['High'], df['Low'], df['Close'], 14, 3, 3)#STOCHk_14_3_3  STOCHd_14_3_3
            #     macd = df.ta.macd(fast=fast_period, slow=slow_period, signal=signal_period)#MACD_12_26_9  MACDh_12_26_9  MACDs_12_26_9
            #     rsi = df.ta.rsi(rsi_period)
            #     df = pd.concat([df, adx, stoch, macd, rsi], axis=1)
            #     print('Post Concat')
            
            # Write to MSSQL Server table
            query = "SELECT TOP 1 * FROM StockData"
            cursor.execute(query)
            first_record = cursor.fetchone()
            print('record found')
            try:
                print(ticker.ticker)
                # Execute the INSERT statement using cursor.execute() method
                cursor.execute("IF NOT EXISTS (SELECT Symbol FROM StockData WHERE Symbol='{}')INSERT INTO dbo.StockData (Symbol) VALUES ('{}')".format(ticker.ticker))
                conn.commit()
                print('Insert Executed')
            except pandas.io.sql.DatabaseError as e:
                print("There was a pandas.io.sql.DatabaseError", e)
            except NameError as e:
                print("There was a NameError", e)
            except:
                print("Exception ", sys.exc_info()[0], "occurred!")
                pass
        except:
            print("Exception ", sys.exc_info()[0], "occurred!")
            pass
except:
    pass
finally:
    spinner.stop()
    print("Processing complete")
    print(date)
    # record end time
    end = time.time()
# Commit the changes and close the connection
conn.commit()
conn.close()

