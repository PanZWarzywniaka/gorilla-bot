from gorilla_bot.live_trader import LiveTrader
from os import environ


def main():
    trader = LiveTrader(
        dollars=100,
        ticker=environ.get('TICKER'),
        interval=environ.get('INTERVAL'),
        historic_data_period=environ.get('PERIOD'),)


if __name__ == '__main__':
    main()
