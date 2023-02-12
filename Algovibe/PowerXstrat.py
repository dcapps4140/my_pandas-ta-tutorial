#!/usr/bin/env python
'''The code imports the pandas and pandas_ta libraries, and loads self.da into a pandas self.daFrame called df. 
Then, it defines a function calculate_stoch that takes a self.daFrame df and a window size (defaulting to 7) as inputs, and calculates the 
Stochastic Oscillator using the ta.stoch() function from the pandas_ta library. 
The result is stored as a new column "stoch" in the self.daFrame.'''
import pandas as pd
from backtesting import Backtest
from backtesting import Strategy
from backtesting.lib import crossover
import pandas_ta as ta
import yfinance as yf

RSI_PERIOD = 14
slow_k_period = 3
slow_d_period = 3
FAST_PERIOD = 12
SLOW_PERIOD = 26
SIGNAL_PERIOD = 9
ADR_PERIOD = 7
ticker = '^GSPC'
start_date = '2020-02-12'
end_date = '2023-02-12'
balance = 100000
RISK_PERCENTAGE = .02

class MyStrategy:
    def init(self, df, params):
        self.df = df
        self.strategy = Strategy
        if params is None:
            params = {}
        self.params = params
        self.stoch = self.I(calculate_stoch, df) # functional 
        self.rsi = self.I(calculate_rsi, df) # functional
        self.macd = self.I(calculate_macd,df) # functional
        self.adr = self.I(calculate_adr, df)
        
    def next(self):
        if (df['rsi'] > 50).all() and (df['stoch_k'] > 50).all() and (df['macd'] > df['macd_signal']).all():
            position_size = calculate_position_size(balance, RISK_PERCENTAGE, df['adr'])
            stop_loss = calculate_stop_loss(df['Close'], df['adr'])
            profit_target = calculate_profit_target(df['Close'], df['adr'])
            buy=(position_size, stop_loss, profit_target)
            print(buy)  
        elif (df['rsi'] < 50).all() and (df['stoch_k'] < 50).all() and (df['macd'] < df['macd_signal']).all():
            position_size = calculate_position_size(balance, RISK_PERCENTAGE, df['adr'])
            stop_loss = calculate_stop_loss(df['Close'], df['adr'])
            profit_target = calculate_profit_target(df['Close'], df['adr'])
            sell=(position_size, stop_loss, profit_target)
            print(sell)

                    
# Define functions
#
def calculate_stoch(df):
    # Calculate Stochastic Oscillator using pandas_ta
    result = ta.stoch(df['High'], df['Low'], df['Close']).dropna()
    df['stoch_k'] =  result.STOCHk_14_3_3
    df['stoch_d'] = result.STOCHd_14_3_3
    return df

'''The updated code now includes a new function, calculate_rsi(), which calculates the relative strength index (RSI) of the stock prices in the self.daFrame. 
The function takes in the self.daFrame df and the RSI_PERIOD parameter, and it adds a new column to the self.daFrame df with the calculated RSI values. 
After the calculation is complete, the updated self.daFrame is returned.

In the execution code, the RSI calculation is done by calling calculate_rsi() and passing in the self.daFrame df and the RSI_PERIOD parameter. 
The result of the function is then stored back into the self.daFrame df.'''
def calculate_rsi(df):
    # Calculate RSI using pandas_ta
    df['rsi'] = ta.rsi(df['Close'], RSI_PERIOD)
    return df

'''This code defines a function calculate_macd which takes the self.daFrame, the fast period, slow period, and signal period as input and calculates the MACD using the ta.macd function. 
The calculated MACD, MACD signal and MACD histogram values are then added to the self.daFrame as columns. 
The script also defines custom fast period, slow period and signal period variables and then calls the calculate_macd function to update the self.daFrame.'''
def calculate_macd(df):
    # Calculate MACD using pandas_ta
    result = ta.macd(df['Close'], FAST_PERIOD, SLOW_PERIOD, SIGNAL_PERIOD)
    print(df.tail(10))
    df['macd'] = result.MACD_12_26_9
    df['macd_signal'] = result.MACDs_12_26_9
    df['macd_hist'] = result.MACDh_12_26_9
    return df

def calculate_adr(df):
    # Calculate ADR using pandas_ta
    result  = ta.atr(df['High'], df['Low'], df['Close']).dropna()
    print(result.tail(10))
    df['adr'] = result#.ATRr_14
    print(df.tail(10))
    return df
    
# Define the function to calculate the position size
def calculate_position_size(balance, risk_percentage, adr):
    risk = balance * risk_percentage
    position_size = risk / adr
    return position_size

# Define the function to calculate the stop loss
def calculate_stop_loss(entry_price, adr):
    stop_loss = entry_price - adr
    return stop_loss

# Define the function to calculate the profit target
def calculate_profit_target(entry_price, adr):
    profit_target = entry_price + 2 * adr
    return profit_target

# Define the position size calculation
def calculate_position_size(balance, risk_percentage, adr):
    return (balance * risk_percentage) / adr

# Define the stop loss calculation
def calculate_stop_loss(price, adr):
    return price - adr

# Define the profit target calculation
def calculate_profit_target(price, adr):
    return price + (2 * adr)
        

if __name__ == "__main__":
    # Your code goes here
    # Operation and execution code
    # Download the self.df for the S&P 500 ^GSPC index for the past year
    ticker = '^GSPC'
    df = yf.download(ticker, start=start_date, end=end_date)
    print(df.tail())
    MyStrategy()


#Initialize the backtesting object
#bt = Backtest(df, MyStrategy, cash=100000)
# bt = Backtest(df, my_strategy, cash=10000)
#stats = bt.run()
#print(stats)