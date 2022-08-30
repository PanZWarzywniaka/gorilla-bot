from abc import abstractmethod
import requests
from os import environ


class BaseConnector():

    @abstractmethod
    def place_buy_order(self, symbol: str, notional: float): pass

    @abstractmethod
    def place_sell_order(self, symbol: str, qty: float): pass

    @abstractmethod
    def list_of_orders(self): pass
