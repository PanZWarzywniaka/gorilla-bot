from urllib import request
from auth import CoinbaseWalletAuth
import json
import requests
import datetime
import time


class Connector:

    def __init__(self, url_base, key_id, secret_key):
        self.url_base = url_base
        self.headers = {
            "APCA-API-KEY-ID": key_id,
            "APCA-API-SECRET-KEY": secret_key
        }
        self.default_json = {
            "type": "market",
            "time_in_force": "gtc",
        }

    def __request(self, verb: str, endpoint: str, json=None, params=None):
        if json is None:
            json = {}

        if params is None:
            params = {}

        if verb.upper() == "GET":
            return requests.get(self.url_base+endpoint, headers=self.headers, json=json)
        print(params)
        if verb.upper() == "POST":
            return requests.post(self.url_base+endpoint, headers=self.headers, json=json)

        return None

    def place_buy_order(self, symbol, notional):
        params = {
            "symbol": symbol,
            "notional": notional,
            "side": "buy"
        }
        return self.__place_order(params)

    def place_sell_order(self, symbol, qty):
        params = {
            "symbol": symbol,
            "qty": qty,
            "side": "sell"
        }
        return self.__place_order(params)

    def __place_order(self, params):
        params.update(self.default_json)
        return self.__request("POST", "/v2/orders", json=params)
