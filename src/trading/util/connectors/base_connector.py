from abc import abstractmethod
import requests


class BaseConnector():

    def request(self, verb: str, endpoint: str, json=None, params=None):
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

    @abstractmethod
    def place_buy_order(self, symbol: str, notional: int): pass

    @abstractmethod
    def place_sell_order(self, symbol: str, qty: int): pass
