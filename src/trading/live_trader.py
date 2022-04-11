import time
import datetime
from models.candlestick import Candlestick
from trader import Trader
from models.trade import Trade


class LiveTrader(Trader):
    def __init__(self,
                 dollars=100,
                 starting_asset=0,
                 take_profit_ratio=2,
                 stop_loss_ratio=1,
                 rsi_threshold=30,
                 ticker="BTC-USD",
                 historic_data_period="60d",
                 interval="5m") -> None:
        super().__init__(
            True,   # clear_db
            True,   # update_db
            dollars,
            starting_asset,
            take_profit_ratio,
            stop_loss_ratio,
            rsi_threshold,
            ticker,
            historic_data_period,
            interval)

        self.ticker = ticker
        self.interval = interval
        self.main_loop()

    def main_loop(self):
        print("Starting main loop")
        while True:
            Candlestick.update_db_with_new_candlesticks(
                self.ticker, "1d", self.interval,
                start=datetime.datetime.now() - datetime.timedelta(minutes=15))
            print("Sleeping")
            time.sleep(10)
