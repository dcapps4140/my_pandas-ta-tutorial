#!/usr/bin/env python
# coding: utf-8
import json
import os
import websocket


# Get the value of an environment variable
API_KEY = os.environ.get('API_KEY')
API_KEY_SK = os.environ.get('API_KEY_SK')
print(API_KEY, API_KEY_SK)

END_POINT = 'wss://stream.binance.us:9443/ws'

our_msg = json.dumps({'method':'SUBSCRIBE', 'params':['btcusdt@ticker'],'id':1})

def on_open(ws):
	'''This is the callback function that will be called when the connection is opened'''
	ws.send(our_msg)

def on_message(ws, message):
	'''This is the callback function that will be called when a message is received'''
	out = json.loads(message)
	print(out)

ws = websocket.WebSocketApp(END_POINT, on_message=on_message, on_open=on_open)
ws.run_forever()
