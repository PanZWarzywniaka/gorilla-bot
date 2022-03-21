from connector import Connector
from trader import Trader

API_KEY_ID = "PKWQG5S6ADTMZPWJIS3Y"
API_SECRET_KEY = "hi4MJ13M3i9OUUPv0wLDHvnycfAlP838JEg8qCor"
API_URL = 'https://paper-api.alpaca.markets'


def main():
    # #trader = Connector(API_URL, API_KEY_ID, API_SECRET_KEY)
    # x = trader.request("GET", "/v2/account")
    # trader.print_json(x.json())

    trader = Trader(
        dollars=100,
        starting_asset=0,
        stop_loss_ratio=1,  # as percent of entry money
        take_profit_ratio=2,
        rsi_threshold=30,
        rsi_length=14,
        ticker="BTC-USD",
        period="7d",
        interval="5m")

    trader.download_data()
    # trader.start_database()
    # trader.save_data()

    trader.process_data()
    trader.calculate_profit()
    # df = trader.data
    # df = df.loc[df['Action'] != 0]
    # print(df)
    trader.make_charts()
    print(f"MONEY: {trader.dollars} $$$")


if __name__ == '__main__':
    main()
