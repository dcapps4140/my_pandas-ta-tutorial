import yfinance
import pandas as pd
import pandas_ta as ta

df = pd.DataFrame() # Emp

## Load data
#df = pd.read_csv("path/t
# OR if you have yfinance
df = df.ta.ticker("aapl")
print(df)
