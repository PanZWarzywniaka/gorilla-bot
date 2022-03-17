from urllib import request
from auth import CoinbaseWalletAuth
import json
import requests
import datetime


class Trader:

    def __init__(self, url_base, api_key, secret_key, pass_phrase):
        self.url_base = url_base
        self.auth = CoinbaseWalletAuth(api_key, secret_key, pass_phrase)

    def print_json(self, raw_json):
        print(json.dumps(raw_json, indent=4))

    def print_delay(self, timestamp):

        now = time.time()
        print(f"Machine time: {now}")

        print(f"Server time: {timestamp}")

        diff = abs(now-timestamp)
        print(f"Time diff: {diff} ms.")
        diff /= 1000
        print(f"Time diff: {diff} s.")
        diff /= 60
        print(f"Time diff: {diff} min.")

    def request(self, verb: str, url: str, params=None, json=None):
        if json is None:
            json = {}

        if params is None:
            params = {}

        if verb.upper() == "GET":
            return requests.get(self.url_base+url, auth=self.auth, params=params)

        # if verb.upper() == "POST":
        #     return requests.post(self.url_base+url, json=json, auth=self.auth)

        return None

    # date in "%d/%m/%Y" format
    def get_data_for_day(self, product_id: str, start_date: datetime.datetime):

        GRANULARITY = 300

        delta = datetime.timedelta(days=1)
        end_date = start_date + delta

        start_ts = start_date.isoformat()
        end_ts = end_date.isoformat()

        payload = {
            'start': start_ts,
            'end': end_ts,
            'granularity': GRANULARITY
        }

        r = self.request(
            "GET", f"products/{product_id}/candles", params=payload)

        print(start_ts)
        print(end_ts)
        result = r.json()
        self.print_json(result)
        print(len(result))
