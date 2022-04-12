from datetime import datetime
from historical_trader import HistoricalTrader
from live_trader import LiveTrader

API_KEY_ID = "PKWQG5S6ADTMZPWJIS3Y"
API_SECRET_KEY = "hi4MJ13M3i9OUUPv0wLDHvnycfAlP838JEg8qCor"
API_URL = 'https://paper-api.alpaca.markets'


def main():
    # #trader = Connector(API_URL, API_KEY_ID, API_SECRET_KEY)
    # x = trader.request("GET", "/v2/account")
    # trader.print_json(x.json())

    trader = HistoricalTrader(
        clear_db=True,
        update_db=True,  # downloads candle sticks from the internet
        dollars=100,
        starting_asset=0,

        # as percent of entry money
        take_profit_ratio=3,
        stop_loss_ratio=1,

        rsi_threshold=30,
        # start=None,
        # end=None,
        ticker="BTC-USD",
        period="7d",
        interval="5m")

    trader.make_charts(
        # start=datetime(2022, 4, 2),
        # end=datetime(2022, 4, 6),
    )

    trader = LiveTrader(dollars=100, starting_asset=0,
                        take_profit_ratio=3, stop_loss_ratio=1, rsi_threshold=30,
                        ticker="BTC-USD", historic_data_period="60d")


if __name__ == '__main__':
    main()
