from datetime import datetime
import pyodbc
import sys
import time
import pandas_ta as ta
import yfinance as yf
import pandas as pd
from halo import Halo
from termcolor import colored
import logging

# set up logging to file - see previous section for more details
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='/tmp/myapp.log',
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
server = 'DESKTOP-7ARJ1N3\SQLEXPRESS'
database = 'stocks'
table_name = 'StockSymbols'
table_name_2 = 'StockData'
table_name_3 = 'StockSymbClean'
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
logging.info('Analysis Started.')
#myapp.area1
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
cursor.execute("SELECT {} FROM {}".format(column_name, table_name_3))
stocklist = cursor.fetchall()
logger1.debug('Stocklist Built')

#data is returned as a list of tuples, convert to list of lists
stocklist = tuple_to_list(stocklist)

#flatten list of lists to just a list
stocklist = flatten(stocklist)
logger1.debug('Stocklist Prep Comp.')

#myapp.area2
# Process each stock ticker
# Retrieve stock information for all NYSE stocks
for stock in stocklist:
    try:
        #print("Ticker = {}".format(stock))
        logger1.info('Ticker = %s', stock)
        ticker = yf.Ticker(stock)
        df = ticker.history(period="1y")
        last_row = df.iloc[-1]
        if last_row['Close'] >= 5 and last_row['Close'] <= 20:
            try:
                adx = ta.adx(df['High'], df['Low'], df['Close'])
                adx = df.ta.adx()
                stoch = ta.stoch(df['High'], df['Low'], df['Close'], 14, 3, 3)#STOCHk_14_3_3  STOCHd_14_3_3
                macd = df.ta.macd(fast=fast_period, slow=slow_period, signal=signal_period)#MACD_12_26_9  MACDh_12_26_9  MACDs_12_26_9
                rsi = df.ta.rsi(rsi_period)
                df = pd.concat([df, adx, stoch, macd, rsi], axis=1)
                df['Symbol'] = stock
            except:
                print(sys.exc_info()[0], colored("Exception occurred!","red"), end='\r')
                logger2.warning(sys.exc_info()[0])
                pass
            
            #Loop through the rows of the DataFrame
            for i, row in df.iterrows():
                # Create an INSERT statement for each row
                try:
                    #insert_stmt = f"INSERT INTO table_name (column1, column2, column3) "f"VALUES ('{row['column1']}', '{row['column2']}', '{row['column3']}')"
                    insert_stmt = (f"INSERT INTO StockData ([Symbol], [Open], [High], [Low], [Close], [Volume], [Dividends], [Stock Splits], [ADX_14], [RSI_7], [DMP_14], [DMN_14], [STOCHk_14_3_3], [STOCHd_14_3_3], [MACD_12_26_9], [MACDh_12_26_9], [MACDs_12_26_9])" \
                            f"VALUES('{row['Symbol']}','{row['Open']}','{row['High']}','{row['Low']}','{row['Close']}','{row['Volume']}','{row['Dividends']}','{row['Stock Splits']}','{row['ADX_14']}','{row['RSI_7']}','{row['DMP_14']}','{row['DMN_14']}','{row['STOCHk_14_3_3']}','{row['STOCHd_14_3_3']}','{row['MACD_12_26_9']}' ,'{row['MACDh_12_26_9']}','{row['MACDs_12_26_9']}')"
                        )
                    # insert_stmt = (f"INSERT INTO StockData ([Symbol],Date, [Open], [High], [Low], [Close])" \
                    #         f"VALUES('{row['Symbol']}','{row['Date']}','{row['Open']}','{row['High']}','{row['Low']}','{row['Close']}')"
                    #     ) 
                    # Execute the INSERT statement
                    cursor.execute(insert_stmt)
                    logger2.debug('Insert complete')
                except:
                    print(sys.exc_info()[0], colored("Exception occurred!","red"), end='\r')
                    logger2.warning('%s', sys.exc_info()[0])
                    pass
                #Commit the changes to the database
                conn.commit()    
    except:
        print(sys.exc_info()[0], colored("Exception occurred!","red"), end='\r')
        logger2.warning(sys.exc_info()[0])
        pass

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