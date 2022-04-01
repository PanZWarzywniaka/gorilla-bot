from connector import Connector
from trader import Trader
from historical_trader import HistoricalTrader

API_KEY_ID = "PKWQG5S6ADTMZPWJIS3Y"
API_SECRET_KEY = "hi4MJ13M3i9OUUPv0wLDHvnycfAlP838JEg8qCor"
API_URL = 'https://paper-api.alpaca.markets'


def main():
    # #trader = Connector(API_URL, API_KEY_ID, API_SECRET_KEY)
    # x = trader.request("GET", "/v2/account")
    # trader.print_json(x.json())

    trader = HistoricalTrader(
        dollars=100,
        starting_asset=0,

        # as percent of entry money
        take_profit_ratio=3,
        stop_loss_ratio=1,

        rsi_threshold=30,
        ticker="BTC-USD",
        period="7d",
        interval="5m")

    # trader.start_database()
    # trader.save_data()

    # trader.make_charts()


if __name__ == '__main__':
    main()
