import json
import os
import websocket
import pandas as pd
from binance.client import Client


API_KEY = 'QiUbdlK0KehGdgOJxokt7rO2OwGP8wjAQkHb8mVeGmgkccmgauOFmn5TV3tX8FMS'
API_KEY_SK = 'NgQTQjNNnBbD8WMWR3MTRlb5aEgkk4rRabKCOzFZdJIL16tibgxJEc8c9yrZelKu'

client = Client(API_KEY, API_KEY_SK, tld='us')

END_POINT = 'wss://stream.binance.us:9443/ws'

our_msg = json.dumps({'method':'SUBSCRIBE', 'params':['btcusdt@ticker'],'id':1})

df = pd.DataFrame()
IN_POSITION = False
BUY_ORDERS, SELL_ORDERS = [], []

def on_open(ws):
    '''This is the callback function that will be called when the connection is opened'''
    ws.send(our_msg)

def on_message(ws, message):
    global	df, IN_POSITION, BUY_ORDERS, SELL_ORDERS
    out = json.loads(message)
    out = pd.DataFrame({'price': [float(out['c'])]}, index=[pd.to_datetime(out['E'], units='ms')])
    df = pd.concat([df,out],axis=0)
    print(df)
    df = df.tail(5)
    last_price = df.tail(1).price.values[0]
    sma_5 = df.price.rolling(5).mean().tail(1).values[0]
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
