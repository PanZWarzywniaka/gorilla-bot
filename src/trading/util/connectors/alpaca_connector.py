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
        data = {
            "symbol": symbol,
            "notional": str(notional),
            "side": "buy"
        }
        return self.__place_order(data)

    def place_sell_order(self, symbol: str, qty: int):
        data = {
            "symbol": symbol,
            "qty": str(qty),
            "side": "sell"
        }
        return self.__place_order(data)

    def __place_order(self, data):
        data.update(self.default_json)
        return self.request("POST", "/v2/orders", json=data)

    def list_of_all_orders(self):
        params = {
            "status": "all",
        }
        return self.request("GET", "/v2/orders", params=params)

    def get_order(self, order_id):
        return self.request("GET", f"/v2/orders/{order_id}")

    def get_open_position(self, symbol):
        return self.request("GET", f"/v2/positions/{symbol}")

    def close_position(self, symbol):
        pos_req = self.get_open_position(symbol)
        if not pos_req.ok:  # check if position request was ok
            return False

        pos_json = pos_req.json()
        qty = pos_json['qty']
        return self.place_sell_order(symbol, qty)
