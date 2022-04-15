import requests
from util.connectors.base_connector import BaseConnector


class AlpacaConnector(BaseConnector):

    def __init__(self, url_base, key_id, secret_key):
        super().__init__()
        self.url_base = url_base
        self.headers = {
            "APCA-API-KEY-ID": key_id,
            "APCA-API-SECRET-KEY": secret_key
        }
        self.default_json = {
            "type": "market",
            "time_in_force": "gtc",
        }

    def place_buy_order(self, symbol: str, notional: int):
        params = {
            "symbol": symbol,
            "notional": str(notional),
            "side": "buy"
        }
        return self.__place_order(params)

    def place_sell_order(self, symbol: str, qty: int):
        params = {
            "symbol": symbol,
            "qty": str(qty),
            "side": "sell"
        }
        return self.__place_order(params)

    def __place_order(self, params):
        params.update(self.default_json)
        return self.request("POST", "/v2/orders", json=params)
