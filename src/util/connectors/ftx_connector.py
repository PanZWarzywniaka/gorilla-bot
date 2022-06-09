from email import header
import re
from requests import Request
import requests
import hmac
import time
from util.connectors.base_connector import BaseConnector
from os import environ


class FTXConnector(BaseConnector):
    def __init__(self) -> None:
        super().__init__()
        self.url_base = environ.get('URL_BASE_FTX')
        self.secret = environ.get('FTX_SECRET')
        self.ftx_key = environ.get('FTX_KEY')

    def get_request(self, endpoint):
        method = 'GET'
        ts = int(time.time() * 1000)
        url = f'{self.url_base}{endpoint}'
        signature_payload = f'{ts}{method}{url}'.encode()
        signature = hmac.new(self.secret.encode(),
                             signature_payload, 'sha256').hexdigest()

        headers = {
            'FTX-KEY': self.ftx_key,
            'FTX-SIGN': signature,
            'FTX-TS': str(ts)
        }
        while True:
            try:
                return requests.get(url, headers=headers)
            except Exception as err:
                print(err)
                print("Trying again in one second...")
                time.sleep(1)

    def get_price(self) -> float:
        market_name = "BTC/USD"
        endpoint = f"/markets/{market_name}"
        resp = self.get_request(endpoint)
        result = resp.json()['result']
        ask = float(result['ask'])
        bid = float(result['bid'])
        return (ask+bid)/2  # mid price
