#!/usr/bin/env python
# coding: utf-8
Import websocket
import json
import pandas as pd

endpoint = 'wss://stream.binance.com:9443/ws'

our_msg = json.dumps({'method':'SUBSCRIBE', 'params':['btcusdt@ticker'],'id':1})

df = pd.DataFrame()
in_position = False

def on_open(ws):
		ws.send(our_msg)

def on_message(ws, message):
			global df, in_position
			out = json.loads(message)
			out = pd.DataFrame({'price':float(out['c'])}, index=[pd.to_datetime(out['E'],units='ms')})
			df = pd.concat([df,out],axis=0)
			print(df)
			df = df.tail(5)
			last_price = df.tail(1).price.values[0]
			sma_5 = df.price.rolling(5).mean().tail(1).values[0]
			if not in_position and last_price > sma_5:
						print('bought for '+ str(last_price))
						in_position = True
			if in_position and sma_5 > last_price
						print('sold for '+ str(last_price))
						in_position = False

ws = websocket.WebSocketApp(endpoint, on_message=on_message, on_open=on_open)

ws.run_forever()