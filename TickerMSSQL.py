import yfinance as yf
import pymssql

class StockData:
    def __init__(self, ticker):
        self.ticker = ticker
        self.data = yf.Ticker(ticker).info

    def filter_data(self, key, value):
        filtered_data = {}
        for k, v in self.data.items():
            if k == key and v == value:
                filtered_data[k] = v
        return filtered_data

    def sort_data(self, key):
        sorted_data = dict(sorted(self.data.items(), key=lambda item: item[1][key]))
        return sorted_data

def main():
    # Connect to MS SQL Server
    conn = pymssql.connect(server='<server_name>', user='<username>', password='<password>', database='<database_name>')
    cursor = conn.cursor()

    # Retrieve all stock ticker data from the NYSE
    cursor.execute("SELECT ticker FROM stock_tickers WHERE exchange = 'NYSE'")
    tickers = cursor.fetchall()

    # Process each stock ticker
    for ticker in tickers:
        stock_data = StockData(ticker[0])

        # Filter data based on a specific key and value
        filtered_data = stock_data.filter_data('sector', 'Technology')

        # Sort data based on a specific key
        sorted_data = stock_data.sort_data('marketCap')

        # Store the filtered and sorted data in MS SQL Server
        for k, v in sorted_data.items():
            cursor.execute("INSERT INTO filtered_sorted_stock_data (ticker, data) VALUES (%s, %s)", (k, v))
        conn.commit()

    # Close the connection to MS SQL Server
    conn.close()

if __name__ == '__main__':
    main()
