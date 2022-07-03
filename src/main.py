from gorilla_bot.historical_trader import HistoricalTrader
from gorilla_bot.live_trader import LiveTrader
from gorilla_bot.util.visualizer import Visualizer
from os import environ


def main():
    # trader = HistoricalTrader(
    #     clear_db=True,
    #     update_db=True,  # downloads candle sticks from the internet
    #     dollars=100,

    #     # as percent of entry money
    #

    #     ticker=ticker,
    #     period="60d",
    #     interval=interval,
    #     qty_increment_decimal_points=4
    # )
    # Visualizer()
    trader = LiveTrader(
        dollars=100,
        ticker=environ.get('TICKER'),
        interval=environ.get('INTERVAL'),
        historic_data_period=environ.get('PERIOD'),)


if __name__ == '__main__':
    main()
