import json
import os
import websocket
import pandas as pd

API_KEY = os.environ.get('API_KEY')
API_KEY_SK = os.environ.get('API_KEY_SK')
print(API_KEY, API_KEY_SK)

END_POINT = 'wss://stream.binance.us:9443/ws'

our_msg = json.dumps({'method':'SUBSCRIBE', 'params':['btcusdt@ticker'],'id':1})

DF = pd.DataFrame()
IN_POSITION = False
BUY_ORDERS, SELL_ORDERS = [], []

def on_open(ws):
    '''This is the callback function that will be called when the connection is opened'''
    ws.send(our_msg)

def on_message(ws, message):
    global	DF, IN_POSITION, BUY_ORDERS, SELL_ORDERS
    out = json.loads(message)
    out = pd.DataFrame({'price': [float(out['c'])]}, index=[pd.to_datetime(out['E'], units='ms')])
    DF = pd.concat([DF,out],axis=0)
    print(DF)
    DF = DF.tail(5)
    last_price = DF.tail(1).price.values[0]
    sma_5 = DF.price.rolling(5).mean().tail(1).values[0]
    if not IN_POSITION and last_price > sma_5:
        print('bought for '+ str(last_price))
        BUY_ORDERS.append(last_price)
        IN_POSITION = True
    if IN_POSITION and sma_5 > last_price:
        print('sold for '+ str(last_price))
        print('profit: '+ str(last_price - BUY_ORDERS[-1]))
        SELL_ORDERS.append(last_price)
        IN_POSITION = False

ws = websocket.WebSocketApp(END_POINT, on_message=on_message, on_open=on_open)
ws.run_forever()
