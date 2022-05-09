import requests
from util.connectors.base_connector import BaseConnector
from os import environ


class AlpacaConnector(BaseConnector):

    def __init__(self):
        super().__init__()

        self.headers = {
            "APCA-API-KEY-ID": environ.get('ALPACA_KEY_ID'),
            "APCA-API-SECRET-KEY": environ.get('ALPACA_SECRET_KEY'),
        }
        self.default_json = {
            "type": "market",
            "time_in_force": "gtc",
        }

    def request(self, verb: str, endpoint: str, params=None, json=None):
        if json is None:
            json = {}

        if params is None:
            params = {}

        if verb.upper() == "GET":
            return requests.get(environ.get('URL_BASE_ALPACA')+endpoint, headers=self.headers, params=params)

        if verb.upper() == "POST":
            return requests.post(environ.get('URL_BASE_ALPACA')+endpoint, headers=self.headers, json=json)

        return None

    def place_buy_order(self, symbol: str, notional: float):
        data = {
            "symbol": symbol,
            "notional": str(notional),
            "side": "buy"
        }
        return self.__place_order(data)

    def place_sell_order(self, symbol: str, qty: float):
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

    def get_order(self, order_id: str):
        return self.request("GET", f"/v2/orders/{order_id}")

    def get_open_position(self, symbol: str):
        return self.request("GET", f"/v2/positions/{symbol}")

    def is_filled(self, order_id: str, timeout=100):
        for i in range(timeout):
            print(f"Checking if it got filled for {i+1}. time")
            order_info = self.get_order(order_id).json()
            if order_info['filled_at']:
                return order_info
        return False

    def close_position(self, symbol: str) -> bool:
        position_req = self.get_open_position(symbol)
        if not position_req.ok:  # check if position request was ok
            return False

        position_json = position_req.json()
        qty = position_json['qty']
        sell_req = self.place_sell_order(symbol, qty)
        if not sell_req.ok:
            return False
        print("Placed sell order.")

        order_id = sell_req.json()['id']
        order_info = self.is_filled(order_id)
        return order_info

    def open_position(self, symbol: str, notional: float):  # returns order info
        buy_req = self.place_buy_order(symbol, notional)
        if not buy_req.ok:
            return False
        print("Placed buy order.")

        order_id = buy_req.json()['id']
        order_info = self.is_filled(order_id)
        return order_info
