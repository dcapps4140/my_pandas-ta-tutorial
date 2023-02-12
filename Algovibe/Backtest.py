import yfinance as yf
import pandas as pd
import pandas_ta as ta
from backtesting import Backtest
from backtesting import Strategy
from backtesting.lib import crossover

# Define non-default RSI parameters
RSI_PERIOD = 7
RSI_WILDER = False

# Set custom MACD parameters
FAST_PERIOD = 12
SLOW_PERIOD = 26
SIGNAL_PERIOD = 9

class MA_strat(Strategy):

    def init(self):
        stoch = ta.stoch(self.data.High, self.data.Low, self.data.Close, 14, 3, 3)
        self.stochasticK = self.I(stoch[0], self.data, 14)
        
        macd = ta.macd(self.data.Close, fast=FAST_PERIOD, slow=SLOW_PERIOD, signal=SIGNAL_PERIOD)
        self.fast_ema = macd[0]
        self.slow_ema = macd[1]
        self.macd_line = macd[2]
        self.signal_line = macd[3]
        
        rsi = ta.rsi(self.data.Close, RSI_PERIOD)
        self.rsi = self.I(rsi, self.data, RSI_PERIOD)


    def next(self):
        if crossover (self.macd_line[-1], self.signal_line[-1]) and self.stochasticK[-1] > 50 and self.rsi[-1] > 50:
            self.buy()
        elif self.macd_line[-1] < self.signal_line[-1] or self.stochasticK[-1] < 50 or self.rsi[-1] < 50:
            self.position.close()


# Create an empty dataframe to store the stock information
df = pd.DataFrame()
# Download data from Yahoo Finance
df = yf.download('^GSPC', start='1985-01-01')
stoch = ta.stoch(df['High'], df['Low'], df['Close'], 14, 3, 3)
print(stoch)

bt = Backtest(df, MA_strat, cash=10000)
stats = bt.run()
print(stats)



annualized_volatility = (df.Close.pct_change() * 100).std() * 252**(1/2)
print("Annualized Volatilty S&P 500 ", annualized_volatility)
