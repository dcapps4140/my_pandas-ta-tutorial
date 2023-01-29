'''
A sorting and filtering algorithm for stock ticker data on the NYSE can be implemented using Python, classes, functions, the yfinance library, and an MS SQL server

In this code, we first establish a connection to an MS SQL server and retrieve all the stock ticker data for the NYSE. 
We then create a class StockData to process each stock ticker. The class has two methods: filter_data and sort_data. 
The filter_data method filters the stock data based on a specific key and value, and the sort_data method sorts the data based on a specific key.

In the main function, we process each stock ticker, filter the data based on the 'sector' key and the value 'Technology', 
sort the data based on the 'marketCap' key, and store the filtered and sorted data in MS SQL Server.

The given code provides a way to sort and filter stock ticker data for the NYSE using Python. 
It does this by using the yfinance library to retrieve the data for each stock ticker and the MS SQL server to store the filtered and sorted data.

The code creates a StockData class that processes each stock ticker. 
The class has two methods: filter_data and sort_data. 
The filter_data method allows you to select only the data that meets a certain criteria, for example, selecting only technology sector stocks. 
The sort_data method arranges the data in a specific order, for example, sorting the stocks by market capitalization.

The main function connects to the MS SQL server, retrieves all the stock ticker data for the NYSE, and processes each stock ticker. 
For each stock ticker, it uses the StockData class to filter and sort the data, and then stores the filtered and sorted data in the MS SQL server.

In layman's terms, the code provides a way to take a large amount of stock ticker data and arrange it in a specific way based on certain criteria, 
and store the organized data in a database.
'''
import yfinance as yf
import pyodbc

#Define your database connection string parameters
server = 'DESKTOP-7ARJ1N3\SQLEXPRESS'
database = 'stocks'
table_name = 'StockSymbols'
column_name = 'Symbol'
username = 'vscode'
password = 'development'

class StockData:
    def __init__(self, ticker):
        self.ticker = ticker
        self.data = yf.Ticker(ticker).info
        print(self.data.values)#{'regularMarketPrice': None, 'preMarketPrice': None, 'logo_url': '', 'trailingPegRatio': 3.0203}

def main():
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
    tickers = cursor.fetchall()

        # Process each stock ticker
    for ticker in tickers:
            print(ticker)


            # # Store the filtered and sorted data in MS SQL Server
            for k, v in sorted_data.items():
                cursor.execute("INSERT INTO filtered_sorted_stock_data (ticker, data) VALUES (%s, %s)", (k, v))
            conn.commit()

    # Close the connection to MS SQL Server
    conn.close()

if __name__ == '__main__':
    main()
