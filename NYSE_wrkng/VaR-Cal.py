"""This code is used to read an sql database create and write a
Pandas DataFrame to a SQL database. See improvement suggestions at end of code"""
from datetime import datetime
import time
import sys
import logging
from termcolor import colored
import numpy as np
import pandas_ta as ta
import yfinance as yf
import pandas as pd
from halo import Halo
import pyodbc
import itertools
import os

# set up logging to file - see previous section for more details
script_dir = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(script_dir, 'myapp2.log')
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename=filename,
                    filemode='w')
# define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.INFO)
# set a format which is simpler for console use
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
# tell the handler to use this format
console.setFormatter(formatter)
# add the handler to the root logger
logging.getLogger('').addHandler(console)

# Now, define a couple of other loggers which might represent areas in your
# application:

logger1 = logging.getLogger('myapp.area1')
logger2 = logging.getLogger('myapp.area2')

#Define your database connection string parameters
SERVER = r'DESKTOP-7ARJ1N3\SQLEXPRESS'
DATABASE = 'stocks'
TABLE_NAME_1 = 'StockSymbols'
TABLE_NAME_2 = 'StockData'
TABLE_NAME_3 = 'StockSymbClean'
COLUMN_NAME = 'Symbol'
USERNAME = 'vscode'
PASSWORD = 'development'

date = datetime.today().strftime('%Y-%m-%d-%H-%M')
#weights = [0.25, 0.35, 0.40]
weights = [1]
confidence_level = 0.05

# Define non-default RSI parameters
RSI_PERIOD = 7
RSI_WILDER = False

# Set custom MACD parameters
FAST_PERIOD = 12
SLOW_PERIOD = 26
SIGNAL_PERIOD = 9
#
def tuple_to_list(my_tuples):
    """Convert tuples to list of tuples"""
    return [list(x) for x in my_tuples]

# def flatten(my_list):
#     """Flatten list of tuples"""
#     return [item for sublist in my_list for item in sublist]

def flatten(my_list):
    """Flatten list of tuples"""
    return list(itertools.chain(*my_list))

def database_exists(conn, db_name):
    """Does table exist?"""
    cursor = conn.cursor()
    cursor.execute(f"SELECT name from sys.databases WHERE name = '{db_name}'")
    result = cursor.fetchall()
    cursor.close()
    return len(result) > 0

def table_exists(conn, table_name):
    """Does table exist?"""
    cursor = conn.cursor()
    cursor.execute(f"SELECT name from sys.tables WHERE name = '{TABLE_NAME_1}'")
    result = cursor.fetchall()
    cursor.close()
    return len(result) > 0

# # record start time
start = time.time()
logging.info('Analysis Started.')
#myapp.area1
# Use the Halo library to display a spinning loading animation
spinner = Halo(text='Retrieving stock information...', spinner='dots')
#spinner.start()

# Connect to the MS SQL Server database
# Define your database connection string
# Connect to the database
conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                    'SERVER=' + SERVER + ';'
                    'DATABASE=' + DATABASE + ';'
                    'UID=' + USERNAME + ';'
                    'PWD=' + PASSWORD)

# Create a cursor
cursor = conn.cursor()

# Create a database and table for the stock symbols data
# Create the database if it doesn't exist
if not database_exists(conn, DATABASE):
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE {DATABASE}")
    Sonn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                          'SERVER=' + SERVER + ';'
                          'DATABASE=' + DATABASE + ';'
                          'UID=' + USERNAME + ';'
                          'PWD=' + PASSWORD)

# Create the table if it doesn't exist
table_create_sql = f"CREATE TABLE {TABLE_NAME_1} (Symbol varchar(10) NOT NULL PRIMARY KEY)"
if not table_exists(conn, TABLE_NAME_1):
    cursor = conn.cursor()
    cursor.execute(table_create_sql)
    cursor.close()

table_create_sql = f"CREATE TABLE {TABLE_NAME_2} (Symbol varchar(10) NOT NULL PRIMARY KEY)"
if not table_exists(conn, TABLE_NAME_2):
    cursor = conn.cursor()
    cursor.execute(table_create_sql)
    cursor.close()

# Drop previous data from MSSQL DB
row_drop_sql = "DELETE FROM [dbo].[StockData]"
if table_exists(conn, TABLE_NAME_2):
    cursor = conn.cursor()
    cursor.execute(row_drop_sql)
    cursor.commit()

# Create an empty dataframe to store the stock information
df = pd.DataFrame()

# Retrieve all stock ticker data from the NYSE
cursor.execute(f"SELECT {COLUMN_NAME} FROM {TABLE_NAME_3}")
stocklist = cursor.fetchall()
logger1.info('Stocklist Built')

#data is returned as a list of tuples, convert to list of lists
stocklist = tuple_to_list(stocklist)

#flatten list of lists to just a list
stocklist = flatten(stocklist)
logger1.info('Stocklist Prep Comp.')

# myapp.area2
# Process each stock ticker
# Retrieve stock information for all NYSE stocks
for stock in stocklist:
    # Specify the stock symbol
    try: 
        logger2.info('Ticker = %s', stock)
        ticker = yf.Ticker(stock).history(period="1y")
        # Select the 'Close' column, which represents the closing price of the stock each day
        stock_returns = ticker['Close'].pct_change().dropna()
        # Load the returns data into a Pandas dataframe
        df = pd.DataFrame(stock_returns)
        # Rename the 'Close' column to 'returns'
        df = df.rename(columns={'Close': 'returns'})
        #logger2.info('%s', df.head(5))
        # Calculate the portfolio returns
        portfolio_returns = (df * weights).sum(axis=1) 
        #logger2.info('Portfolio %s', portfolio_returns)
        # Calculate the VaR
        var = np.percentile(portfolio_returns, confidence_level * 100)
        # Output the results
        print("Value-at-Risk: {:.5f}".format(var))
        
        tdf = ticker
        last_row = tdf.iloc[-1]

        if last_row['Close'] >= 5 and last_row['Close'] <= 20:
            try:
                adx = ta.adx(tdf['High'], tdf['Low'], tdf['Close'])
                adx = tdf.ta.adx()
                stoch = ta.stoch(tdf['High'], tdf['Low'], tdf['Close'], 14, 3, 3)#STOCHk_14_3_3  STOCHd_14_3_3
                macd = tdf.ta.macd(fast=FAST_PERIOD, slow=SLOW_PERIOD, signal=SIGNAL_PERIOD)#MACD_12_26_9  MACDh_12_26_9  MACDs_12_26_9
                rsi = tdf.ta.rsi(RSI_PERIOD)
                tdf = pd.concat([tdf, adx, stoch, macd, rsi], axis=1)
                tdf['Symbol'] = stock
                tdf['Returns'] = portfolio_returns
                
                # get the date column
                dates = tdf.index
                # print the dates
                #logger2.debug('%s, %s', dates, portfolio_returns)
                tdf['Date'] = dates
                #logger2.debug('%s', tdf.columns)
                #logger2.debug("The data types of each column are:")
                #logger2.debug('%s', tdf.dtypes)
                #logger2.debug('%s', tdf.tail(5))
            except:
                print(sys.exc_info()[0], colored("Exception occurred!","red"), end='\r')
                logger2.warning(sys.exc_info()[0])

            #Loop through the rows of the DataFrame
            for i, row in tdf.iterrows():
                # Create an INSERT statement for each row
                try:
                    #insert_stmt = f"INSERT INTO TABLE_NAME (column1, column2, column3) "f"VALUES ('{row['column1']}', '{row['column2']}', '{row['column3']}')"
                    insert_stmt = (f"INSERT INTO StockData ([Symbol], [Date], [Open], [High], [Low], [Close], [Volume], [Dividends], [Stock Splits], [ADX_14], [RSI_7], [DMP_14], [DMN_14], [STOCHk_14_3_3], [STOCHd_14_3_3], [MACD_12_26_9], [MACDh_12_26_9], [MACDs_12_26_9], [Returns])" \
                            f"VALUES('{row['Symbol']}','{row['Date']}','{row['Open']}','{row['High']}','{row['Low']}','{row['Close']}','{row['Volume']}','{row['Dividends']}','{row['Stock Splits']}','{row['ADX_14']}','{row['RSI_7']}','{row['DMP_14']}','{row['DMN_14']}','{row['STOCHk_14_3_3']}','{row['STOCHd_14_3_3']}','{row['MACD_12_26_9']}' ,'{row['MACDh_12_26_9']}','{row['MACDs_12_26_9']}','{row['Returns']}')"
                        )
                    cursor.execute(insert_stmt)
                    logger2.debug('Insert complete')
                except:
                    print(sys.exc_info()[0], colored("Exception occurred!","red"), end='\r')
                    logger2.warning('%s', sys.exc_info()[0])

                #Commit the changes to the database
                conn.commit()
    except:
        print('ES')
        print(sys.exc_info()[0], colored("Exception occurred!","red"), end='\r')
        logger2.warning(sys.exc_info()[0])
        print('EE')
print('\n', 'Post Insert')

spinner.stop()
#print("Processing complete")
logger2.info('Processing complete')

#print(date)
# record end time
end = time.time()
# Commit the changes and close the connection
conn.commit()
conn.close()

# record end time
end = time.time()
# print the difference between start
# and end time in milli. secs
print("The time of execution of above program is :",
    (((end-start) * 10**3)/1000)/60, "mins")

# print the difference between start