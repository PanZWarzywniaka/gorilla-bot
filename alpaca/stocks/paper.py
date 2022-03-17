import json
import requests
import os
from .config import init

API_KEY = "PKNDAPZLAA7HUZRVMW8L"
API_PRIVATE_KEY = "zjVXeNDSPJKn1NuWfLPJzbv7qhBhzoBOr8FwMs1Z"
# for paper money
# for real moneyhttps://data.alpaca.markets
os.environ["APCA_API_BASE_URL"] = "https://paper-api.alpaca.markets"
os.environ["APCA_API_DATA_URL"] = "https://data.alpaca.markets"

# setting constants

HEADERS = {'APCA-API-KEY-ID': API_KEY, 'APCA-API-SECRET-KEY': API_PRIVATE_KEY}


URL_BASE = "https://paper-api.alpaca.markets"
ACCOUNT_URL = "{}/v2/account".format(URL_BASE)
ORDERS_URL = "{}/v2/orders".format(URL_BASE)
ASSETS_URL = "{}/v2/assets".format(URL_BASE)


def get_asset(symbol: str):

    URL = "{}/{}".format(symbol)
    print(URL)


def get_account():
    r = requests.get(ACCOUNT_URL, headers=HEADERS)

    return json.loads(r.content)


def print_account_details(account):
    print("Acount details:")
    print(f"Cash {account['cash']}")
    print(f"Portfolio Value {account['portfolio_value']}")
    print(f"Buying power {account['buying_power']}")
    print(f"Currency {account['currency']}")
    print(f"Status {account['status']}")


def print_orders(orders):
    print("Current Orders: ")
    for count, x in enumerate(orders):
        print(f"Order {count+1}. {x['symbol']} Quantity: {x['qty']}")


def get_orders():
    r = requests.get(ORDERS_URL, headers=HEADERS)

    return json.loads(r.content)


def create_order(symbol, qty, side, type, time_in_force):
    data = {
        "symbol": symbol,
        "qty": qty,
        "side": side,
        "type": type,
        "time_in_force": time_in_force
    }
    print(f"Ordering...")
    print(data)
    r = requests.post(ORDERS_URL, json=data, headers=HEADERS)

    return json.loads(r.content)


def main():
    init()
    print_account_details(get_account())
    print_orders(get_orders())
    # response = create_order("AMZN", 2, "buy", "market", "gtc")


if __name__ == '__main__':
    main()
