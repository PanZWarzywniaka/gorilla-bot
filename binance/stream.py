#!/usr/bin/env python

import datetime
import math
import time
import logging
from binance.lib.utils import config_logging
from binance.websocket.spot.websocket_client import SpotWebsocketClient as Client
from include import print_json

config_logging(logging, logging.DEBUG)


def message_handler(message):

    if 'k' not in message.keys():
        return

    print(f"Got message.")
    now = time.time()
    print(f"Machine time: {now}")
    ts = int(message['k']['T'])/1000
    print(f"Server time: {ts}")

    diff = abs(now-ts)
    print(f"Time diff: {diff} ms.")
    diff /= 1000
    print(f"Time diff: {diff} s.")
    diff /= 60
    print(f"Time diff: {diff} min.")
# print(
#     f"Server time: {datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')}")


my_client = Client()
my_client.start()

print("Starting stream")
my_client.kline(symbol="btcusdt", id=1, interval="1m",
                callback=message_handler)
