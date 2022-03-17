import requests
import json
import time
import datetime
from auth import CoinbaseWalletAuth
from trader import Trader

API_KEY = "0170a70a9dcf8dc5a7faef4e500a73e0"
API_SECRET = "aa4sJFkLkjIy2WacofPh9I/ky+1+66nadNMfz3ChzADgwiQQ8tQ+Dw6k8THSmPTD/9Dc4s0QWJSXHGY8ZrBdmQ=="
API_PASSPHRASE = 'u30dqbh9rp9'
API_URL = 'https://api-public.sandbox.exchange.coinbase.com/'


def main():
    trader = Trader(API_URL, API_KEY, API_SECRET, API_PASSPHRASE)
    # # r = trader.request("GET", "accounts")
    # # trader.print_json(r.json())
    # product_id = "BTC-USD"
    # payload = {'key1': 'value1', 'key2': 'value2'}
    # r = trader.request("GET", f"products/{product_id}/candles", params=payload)
    # # trader.print_json(r.json())
    # last_ts = r.json()[0][0]
    # trader.print_delay(last_ts)
    day = datetime.datetime(year=2021, month=12, day=15)
    trader.get_data_for_day("BTC-USD", day)


if __name__ == '__main__':
    main()
