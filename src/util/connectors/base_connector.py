from abc import abstractmethod
import requests
from os import environ


class BaseConnector():

    def request(self, verb: str, endpoint: str, params=None, json=None):
        if json is None:
            json = {}

        if params is None:
            params = {}

        if verb.upper() == "GET":
            return requests.get(environ.get('URL_BASE')+endpoint, headers=self.headers, params=params)

        if verb.upper() == "POST":
            return requests.post(environ.get('URL_BASE')+endpoint, headers=self.headers, json=json)

        return None

    @abstractmethod
    def place_buy_order(self, symbol: str, notional: float): pass

    @abstractmethod
    def place_sell_order(self, symbol: str, qty: float): pass

    @abstractmethod
    def list_of_orders(self): pass
