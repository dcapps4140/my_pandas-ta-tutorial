#!/usr/bin/env python
# coding: utf-8

import json
import pandas as pd
import websocket_client as websocket

endpoint = 'wss://stream.binance.com:9443/ws'

our_msg = json.dumps({'method':'SUBSCRIBE', 'params':['btcusdt@ticker'],'id':1})


def on_open(ws):
		ws.send(our_msg)

def on_message(ws, message):
			
			out = json.loads(message)
			
			print(df)


ws = websocket.create_connection(endpoint)
ws.send(our_msg)

while True:
    result = ws.recv()
    on_message(ws, result)