#!/usr/bin/env python
# coding: utf-8
import json
import os
import websocket

# initialize the kill switch
should_stop = False  
# Get the value of an environment variable
API_KEY = os.environ.get('API_KEY')
API_KEY_SK = os.environ.get('API_KEY_SK')
print('keys set')
      #set variables
data = []
df_list = []

END_POINT = 'wss://stream.binance.us:9443/ws'

our_msg = json.dumps({'method':'SUBSCRIBE', 'params':['btcusdt@ticker'],'id':1})


def on_open(ws):
    print(2)
    ws.send(our_msg)

def on_message(ws, message):
    print(3)
    data = json.loads(message)
    print(data)



while not should_stop:
    if should_stop:
        ws.close()
    
    ws = websocket.WebSocketApp(END_POINT, on_message=on_message, on_open=on_open)
    #ws.run_forever()
