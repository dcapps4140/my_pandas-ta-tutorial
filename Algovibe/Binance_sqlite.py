import pandas as pd
import sqlalchemy
from binance.client import Client
from binance import BinanceSocketManager
import os

API_KEY = 'QiUbdlK0KehGdgOJxokt7rO2OwGP8wjAQkHb8mVeGmgkccmgauOFmn5TV3tX8FMS'
API_KEY_SK = 'NgQTQjNNnBbD8WMWR3MTRlb5aEgkk4rRabKCOzFZdJIL16tibgxJEc8c9yrZelKu'

client = Client(API_KEY, API_KEY_SK)

bsm = BinanceSocketManager(client)

socket = bsm.trade_socket('BTCUSDT')
    
async def main():
    await socket.__aenter__()
    msg = await socket.recv()
    print(msg)
    
main()
