'''
This code modifies the existing code to connect to an MS SQL Server database, create a table named StockSymbols to store the qualified stock symbols, 
and insert the qualified stock symbols into the table. The columns in the StockSymbols table include:

Symbol (varchar(10), NOT NULL, PRIMARY KEY) - to store the stock symbol string.
Note: Replace <server_name>, <username>, <password>, and <database_name> in the pymssql.connect() function with the appropriate values
This code uses the IF NOT EXISTS clause in the INSERT statement to only insert a new record if the symbol does not already exist in the table.
'''
#import ta
#import pandas_ta as ta
#import yfinance as yf
import pandas as pd
from yahoo_fin import stock_info as si
#from halo import Halo
import pyodbc

#Define your database connection string parameters
server = 'DESKTOP-7ARJ1N3\SQLEXPRESS'
database = 'stocks'
username = 'vscode'
password = 'development'
table_name = 'StockSymbols'

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

# gather stock symbols from major US exchanges
df1 = pd.DataFrame(si.tickers_sp500())
df2 = pd.DataFrame(si.tickers_nasdaq())
df3 = pd.DataFrame(si.tickers_dow())
df4 = pd.DataFrame(si.tickers_other())

# convert DataFrame to list, then to sets
sym1 = set(symbol for symbol in df1[0].values.tolist())
sym2 = set(symbol for symbol in df2[0].values.tolist())
sym3 = set(symbol for symbol in df3[0].values.tolist())
sym4 = set(symbol for symbol in df4[0].values.tolist())

# join the 4 sets into one. Because it's a set, there will be no duplicate symbols
symbols = set.union(sym1, sym2, sym3, sym4)

# Some stocks are 5 characters. Those stocks with the suffixes listed below are not of interest.
my_list = ['W', 'R', 'P', 'Q']
del_set = set()
sav_set = set()

for symbol in symbols:
    if len(symbol) > 4 and symbol[-1] in my_list:
        del_set.add(symbol)
    else:
        sav_set.add(symbol)

print(f'Removed {len(del_set)} unqualified stock symbols...')
print(f'There are {len(sav_set)} qualified stock symbols...')

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

# Create a table for the stock symbols data
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
table_create_sql = "CREATE TABLE StockSymbols (Symbol varchar(10) NOT NULL PRIMARY KEY)"
if not table_exists(conn, table_name):
    cursor = conn.cursor()
    cursor.execute(table_create_sql)
    cursor.close()

# Insert the qualified stock symbols into the table
for symbol in sav_set:
    insert_sql = f"IF NOT EXISTS (SELECT Symbol FROM StockSymbols WHERE Symbol='{symbol}') " \
                 f"INSERT INTO StockSymbols (Symbol) VALUES ('{symbol}')"
    cursor.execute(insert_sql)
# Commit the changes and close the connection
conn.commit()
conn.close()
