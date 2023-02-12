import pandas as pd
import pandas_ta as ta
import yfinance as yf

# Define variables and parameters
RSI_PERIOD = 7
slow_k_period = 3
slow_d_period = 3
# Define custom MACD parameters
FAST_PERIOD = 12
SLOW_PERIOD = 26
SIGNAL_PERIOD = 9

# Define functions
#
'''The code imports the pandas and pandas_ta libraries, and loads data into a pandas DataFrame called df. 
Then, it defines a function calculate_stoch that takes a DataFrame df and a window size (defaulting to 7) as inputs, and calculates the 
Stochastic Oscillator using the ta.stoch() function from the pandas_ta library. 
The result is stored as a new column "stoch" in the DataFrame.'''
def calculate_stoch(df, RSI_PERIOD, slow_k_period, slow_d_period):
    # Calculate Stochastic Oscillator using pandas_ta
    result = ta.stoch(df['High'], df['Low'], df['Close'], RSI_PERIOD, slow_k_period, slow_d_period)
    df['stoch_k'] =  result.STOCHk_7_3_3
    df['stoch_d'] = result.STOCHd_7_3_3
    return df
'''The updated code now includes a new function, calculate_rsi(), which calculates the relative strength index (RSI) of the stock prices in the DataFrame. 
The function takes in the DataFrame df and the RSI_PERIOD parameter, and it adds a new column to the DataFrame df with the calculated RSI values. 
After the calculation is complete, the updated DataFrame is returned.

In the execution code, the RSI calculation is done by calling calculate_rsi() and passing in the DataFrame df and the RSI_PERIOD parameter. 
The result of the function is then stored back into the DataFrame df.'''
def calculate_rsi(df, RSI_PERIOD):
    # Calculate RSI using pandas_ta
    df['rsi'] = ta.rsi(df['Close'], RSI_PERIOD)
    return df

'''This code defines a function calculate_macd which takes the DataFrame, the fast period, slow period, and signal period as input and calculates the MACD using the ta.macd function. 
The calculated MACD, MACD signal and MACD histogram values are then added to the DataFrame as columns. 
The script also defines custom fast period, slow period and signal period variables and then calls the calculate_macd function to update the DataFrame.'''
def calculate_macd(df, FAST_PERIOD, SLOW_PERIOD, SIGNAL_PERIOD):
    # Calculate MACD using pandas_ta
    result = ta.macd(df['Close'], FAST_PERIOD, SLOW_PERIOD, SIGNAL_PERIOD)
    df['macd'] = result.MACD_12_26_9
    df['macd_signal'] = result.MACDs_12_26_9
    df['macd_hist'] = result.MACDh_12_26_9
    return df

# Operation and execution code
# Download the data for the S&P 500 ^GSPC index for the past year
ticker = '^GSPC'
df = yf.download(ticker, start='2022-02-12', end='2023-02-12')

# Calculate Stochastic Oscillator and update the DataFrame
df = calculate_stoch(df, RSI_PERIOD, slow_k_period, slow_d_period)
df = calculate_rsi(df, RSI_PERIOD)
# Calculate MACD and update the DataFrame
df = calculate_macd(df, FAST_PERIOD, SLOW_PERIOD, SIGNAL_PERIOD)
# Print the result
print(df.tail(15))
