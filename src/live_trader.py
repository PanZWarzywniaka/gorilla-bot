from re import purge
import time
import datetime
from models.candlestick import Candlestick
from trader import Trader
from models.trade import Trade
from util.connectors.alpaca_connector import AlpacaConnector
from util.connectors.ftx_connector import FTXConnector
from util.logger import log_info
from os import environ


class LiveTrader(Trader):
    def __init__(self,
                 dollars,
                 ticker,
                 interval,
                 historic_data_period
                 ) -> None:
        super().__init__(dollars)

        log_info("Initilizing with historical data...")
        Candlestick.update_db_with_new_candlesticks(
            ticker=ticker, period=historic_data_period, interval=interval)

        self.ticker = ticker
        self.ticker_alpaca = ticker+"USD"  # from e.g "XXX" to "XXXUSD"
        INTERVALS_IN_SECONDS = {
            "1m": 60,
            "5m": 300,
            "15m": 900,
        }
        self.interval = interval
        self.interval_seconds = INTERVALS_IN_SECONDS[interval]
        self.SLEEP_RATE = 10  # secs

        self.connector = AlpacaConnector()
        self.ftx_connector = FTXConnector()
        self.start_time = datetime.datetime.utcnow()
        self.main_loop()

    def main_loop(self):
        log_info("Starting main loop")
        log_info(f"Waiting for sync with {self.interval} interval")
        self.time_sync()

        while True:
            log_info("Downloading new price")
            price = self.ftx_connector.get_price()
            log_info(f"Downloaded new price {price}")

            Candlestick.create_from_price(price)
            log_info("Created new CS ")

            self.data = Candlestick.get_processed_candlesticks()
            last_candlestick = self.data.reset_index().iloc[-1]
            self.candlestick = last_candlestick
            self.__print_last_candlestick(last_candlestick)
            self.take_action()
            self.print_stats()

            self.time_sync()

    def time_sync(self):
        seconds_to_sleep = self.interval_seconds - \
            (time.time() % self.interval_seconds)
        log_info(f"Going to sleep {seconds_to_sleep}s")
        time.sleep(seconds_to_sleep)
        log_info("Waking up")

    def buy_all(self) -> bool:
        log_info(f"Buying asset for {self.dollars} USD")
        order_info = self.connector.open_position(
            self.ticker_alpaca, self.dollars)

        if not order_info:
            log_info("Opening position gone wrong. Quiting")
            return False

        log_info("Order filled!")
        log_info(f"Tried to buy for {order_info['notional']} USD")
        log_info(
            f"But bought {order_info['filled_qty']} {order_info['symbol']}")
        log_info(f"For {order_info['filled_avg_price']}")
        spent = float(order_info['filled_qty']) * \
            float(order_info['filled_avg_price'])
        log_info(f"We spent: {spent} USD")

        buy_price = float(order_info['filled_avg_price'])
        self.quantity += float(order_info['filled_qty'])
        # substruct what we paied for the asset
        self.dollars -= spent

        self.current_trade = Trade.create(buy_price=buy_price,
                                          quantity=self.quantity,
                                          buy_datetime=datetime.datetime.utcnow())

        return True

    def sell_all(self) -> bool:
        log_info(f"Selling {self.quantity} of {self.ticker}...")
        order_info = self.connector.close_position(self.ticker_alpaca)
        if not order_info:
            log_info("Closing position gone wrong. Quiting")
            return False

        log_info("Order filled!")
        log_info(
            f"Sold {order_info['filled_qty']} {order_info['symbol']} USD")
        log_info(f"For {order_info['filled_avg_price']}")

        filled_quantity = float(order_info['filled_qty'])
        sell_price = float(order_info['filled_avg_price'])
        earned = filled_quantity * sell_price

        log_info(f"Earned: {earned} USD")

        self.dollars += earned
        self.quantity -= filled_quantity
        self.current_trade.sell_datetime = datetime.datetime.utcnow()
        self.current_trade.sell_price = sell_price
        self.current_trade.save()

        self.reset_variables()
        return True

    def print_stats(self):
        super().print_stats()
        log_info("Live Trader status:")

        run_time = datetime.datetime.utcnow() - self.start_time
        log_info(f"-Running for {run_time}")
        log_info(f"-{self.dollars} USD")
        log_info(f"-{self.quantity} {self.ticker}")
        log_info(f"-Take profit ratio: {environ.get('TAKE_PROFIT_RATIO')}")
        log_info(f"-Stop loss ratio: {environ.get('STOP_LOSS_RATIO')}")
        log_info(f"-RSI triggered: {self.rsi_triggered}")
        log_info(f"Current trade:")
        log_info(self.current_trade)
        if self.current_trade:
            unrealised_return = self.current_trade.get_potential_yield(
                self.candlestick['close'])
            log_info(
                f"Unrealised return: {unrealised_return} %")

    def __print_last_candlestick(self, last_cs):

        cs_time = last_cs['datetime']
        now = datetime.datetime.utcnow()
        log_info(f"Candlestick time: {cs_time.__str__()}")
        log_info(f"Now: {now.__str__()}")
        log_info(f"Delay: {now-cs_time}")
        log_info(last_cs)
