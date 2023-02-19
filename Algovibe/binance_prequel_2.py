#!/usr/bin/env python
# coding: utf-8
import json
import os
import websocket
import ta
#from ta.momentum import rsi
#from ta.trend import sma_indicator
import pandas as pd

# initialize the kill switch
should_stop = False  
# Get the value of an environment variable
API_KEY = os.environ.get('API_KEY')
API_KEY_SK = os.environ.get('API_KEY_SK')
#set variables
data = []
df_list = []

END_POINT = 'wss://stream.binance.us:9443/ws'

our_msg = json.dumps({'method':'SUBSCRIBE', 'params':['btcusdt@ticker'],'id':1})

def createframe(msg):
    df = pd.DataFrame([msg])
    df = df.loc[:,['s', 'E', 'o', 'h', 'l', 'c']]
    df.columns = ['symbol', 'time', 'open', 'high', 'low', 'close']
    df.Price = df.Price.astype(float)
    df.Time = pd.to_datetime(df.Time, unit='ms')
    return df

def on_open(ws):
	'''This is the callback function that will be called when the connection is opened'''
	ws.send(our_msg)

def on_message(ws, message):
    global df
    data = json.loads(message)
    #print(data) 
    new_df = createframe(data)
    df_list.append(new_df)
    df = pd.concat(df_list, ignore_index=True)
    #df['rsi'] = ta.momentum.rsi(df['close'], window=14, fillna=False)
   # df['sma'] = ta.trend.sma_indicator(df['close'], window=12, fillna=False)
    df = df.tail(15)
    print(df)
    
ws = websocket.WebSocketApp(END_POINT, on_message=on_message, on_open=on_open)
ws.run_forever()
