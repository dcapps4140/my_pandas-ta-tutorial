import asyncio

#from binance import AsyncClient
from binance import BinanceSocketManager


API_KEY = 'QiUbdlK0KehGdgOJxokt7rO2OwGP8wjAQkHb8mVeGmgkccmgauOFmn5TV3tX8FMS'
API_KEY_SK = 'NgQTQjNNnBbD8WMWR3MTRlb5aEgkk4rRabKCOzFZdJIL16tibgxJEc8c9yrZelKu'

client = Client(API_KEY, API_KEY_SK)

async def order_book(client, symbol):
    order_book = await client.get_order_book(symbol=symbol)
    print(order_book)


async def kline_listener(client):
    bm = BinanceSocketManager(client)
    symbol = 'BNBBTC'
    res_count = 0
    async with bm.kline_socket(symbol=symbol) as stream:
        while True:
            res = await stream.recv()
            res_count += 1
            print(res)
            if res_count == 5:
                res_count = 0
                loop.call_soon(asyncio.create_task, order_book(client, symbol))