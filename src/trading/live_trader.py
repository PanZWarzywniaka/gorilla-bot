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

        self.SLEEP_RATE = 15
        self.TIME_ZONE_OFFSET = datetime.timedelta(hours=2)
        self.ticker = ticker
        self.interval = interval

        Candlestick.update_db_with_new_candlesticks(
            ticker, period=historic_data_period, interval=interval)
        self.main_loop()

    def __sleep(self, duration):
        print(f"Sleeping: {duration}s")
        for _ in range(duration):
            print(".", end=' ', flush=True)
            time.sleep(1)
        print("\nWaking up")

    def main_loop(self):
        print("Starting main loop")
        while True:
            self.__sleep(self.SLEEP_RATE)

            updated = Candlestick.update_db_with_new_candlesticks(
                self.ticker, "1d", self.interval,
                start=datetime.datetime.now() - datetime.timedelta(minutes=15))

            if not updated:
                continue

            print("Got new candlestick!")

            last_cs = Candlestick.get_last()
            print(last_cs)

            cs_time = last_cs.datetime
            now = datetime.datetime.now() - self.TIME_ZONE_OFFSET
            print(f"Time {cs_time=}")
            print(f"Time {now=}")
            print(f"Delay: {now-cs_time}")
