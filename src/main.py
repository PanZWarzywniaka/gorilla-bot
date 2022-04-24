from historical_trader import HistoricalTrader
from live_trader import LiveTrader
from util.visualizer import Visualizer
from os import environ


def main():
    ticker = environ.get('TICKER')
    interval = "5m"
    # trader = HistoricalTrader(
    #     clear_db=True,
    #     update_db=True,  # downloads candle sticks from the internet
    #     dollars=100,
    #     starting_quantity=0,

    #     # as percent of entry money
    #     rsi_threshold=30,

    #     ticker=ticker,
    #     period="60d",
    #     interval=interval,
    #     qty_increment_decimal_points=4
    # )
    # Visualizer()

    trader = LiveTrader(
        dollars=100, starting_quantity=0, rsi_threshold=30,
        ticker=ticker, interval=interval, historic_data_period="60d",)


if __name__ == '__main__':
    main()
