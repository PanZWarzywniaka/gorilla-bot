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

    def request(self, verb: str, url: str, params=None, json=None):
        if json is None:
            json = {}

        if params is None:
            params = {}
        print(self.headers)
        if verb.upper() == "GET":
            return requests.get(self.url_base+url, headers=self.headers)

        # if verb.upper() == "POST":
        #     return requests.post(self.url_base+url, json=json, auth=self.auth)

        return None
