import time
import datetime
from models.candlestick import Candlestick
from trader import Trader
from models.trade import Trade
from connectors.alpaca_connector import AlpacaConnector


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

        self.SLEEP_RATE = 10
        self.TIME_ZONE_OFFSET = datetime.timedelta(hours=2)
        self.ticker = ticker
        self.interval = interval

        API_KEY_ID = "PK0JT3LM0J95OBVUKBM0"
        API_SECRET_KEY = "gZPUTMLTQUG4qKx9hcSgPa3s8RkfmmA5DKhNAuSg"
        API_URL = 'https://paper-api.alpaca.markets'
        self.connector = AlpacaConnector(API_URL, API_KEY_ID, API_SECRET_KEY)
        # x = trader.request("GET", "/v2/account")
        # trader.print_json(x.json())

        print("Initilizing with historical data...")
        Candlestick.update_db_with_new_candlesticks(
            ticker, period=historic_data_period, interval=interval)
        self.main_loop()

    def __sleep(self, duration):
        print(f"Sleeping: {duration}s", end=' ')
        for _ in range(duration):
            print(".", end=' ', flush=True)
            time.sleep(1)
        print("Waking up")

    def __print_last_candlestick(self, last_cs):

        cs_time = last_cs['datetime']
        now = datetime.datetime.now() - self.TIME_ZONE_OFFSET
        print(f"Candlestick time: {cs_time.__str__()}")
        print(f"Now: {now.__str__()}")
        print(f"Delay: {now-cs_time}")
        print(last_cs)

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
            self.data = Candlestick.get_processed_candlesticks()
            last_candlestick = self.data.reset_index().iloc[-1]
            self.__print_last_candlestick(last_candlestick)
            self.take_action(last_candlestick)
            self.print_stats()
