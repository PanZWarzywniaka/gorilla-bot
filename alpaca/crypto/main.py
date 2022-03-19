from connector import Connector
from trader import Trader

API_KEY_ID = "PKWQG5S6ADTMZPWJIS3Y"
API_SECRET_KEY = "hi4MJ13M3i9OUUPv0wLDHvnycfAlP838JEg8qCor"
API_URL = 'https://paper-api.alpaca.markets'


def main():
    # #trader = Connector(API_URL, API_KEY_ID, API_SECRET_KEY)
    # x = trader.request("GET", "/v2/account")
    # trader.print_json(x.json())

    trader = Trader()
    df = trader.download_data()
    df = trader.prepare_data(df)
    trader.calculate_profit(df)
    trader.make_charts(df)
    print(f"MONEY: {trader.dollars}")


if __name__ == '__main__':
    main()
