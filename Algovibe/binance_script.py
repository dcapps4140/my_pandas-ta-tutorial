import json
import os
import asyncio
import ta
import websockets
import pandas as pd
from binance.client import Client

# Get the value of an environment variable
API_KEY = os.environ.get('API_KEY')
API_KEY_SK = os.environ.get('API_KEY_SK')

df = pd.DataFrame()
df_list = []  # initialize an empty list to store DataFrames
open_position = False

client = Client(API_KEY, API_KEY_SK, tld='us')

stream = websockets.connect('wss://testnet.binance.vision/stream?streams=btcusdt@ticker')

def createframe(msg):
    df = pd.DataFrame([msg])
    df = df.loc[:,['s','E','c']]
    df.columns = ['symbol', 'Time', 'Price']
    df.Price = df.Price.astype(float)
    df.Time = pd.to_datetime(df.Time, unit='ms')
    return df

async def main():
    global df, df_list, open_position, open_position
    async with stream as receiver:
        while not should_stop: # use a global variable to determine when to stop
            data = await receiver.rec()
            data = json.loads(data)['data']
            new_df = createframe(data)
            df_list.append(new_df)
            df = pd.concat(df_list, ignore_index=True)
            if len(df) > 30:
                if not open_position:
                    if ta.momentum.roc(df.Price, 30).iloc[-1] > 0 and ta.momentum.roc(df.Price, 30).iloc[-2]:
                        print('bought for '+ str(last_price))
                        BUY_ORDERS.append(last_price)
                        open_position = True
                # if open_position and sma_5 > last_price:
                #     print('sold for '+ str(last_price))
                #     print('profit: '+ str(last_price - BUY_ORDERS[-1]))
                #     SELL_ORDERS.append(last_price)
                #     open_position = False

# initialize the kill switch
should_stop = False
            
if __name__ == '__main__':
    try:
        asyncio.get_event_loop().run_until_complete(main()) # run the main function until it is complete
    except KeyboardInterrupt:
        should_stop = True # set the kill switch to stop the loop
