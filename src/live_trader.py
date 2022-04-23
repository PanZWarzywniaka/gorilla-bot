import time
import datetime
from models.candlestick import Candlestick
from trader import Trader
from models.trade import Trade
from util.connectors.alpaca_connector import AlpacaConnector
from os import environ


class LiveTrader(Trader):
    def __init__(self,
                 dollars=100,
                 starting_quantity=0,
                 rsi_threshold=30,
                 ticker="BTC-USD",
                 interval="5m",
                 historic_data_period="60d"
                 ) -> None:
        super().__init__(
            dollars,
            starting_quantity,
            rsi_threshold,
            ticker,
            historic_data_period,
            interval)

        # transforms e.g "BTC-USD" to "BTCUSD"
        self.symbol = ticker.replace("-", "")
        self.connector = AlpacaConnector()
        self.ticker = ticker
        self.interval = interval
        self.SLEEP_RATE = 10

        self.main_loop()

    def buy_all(self) -> bool:
        print(f"Buying asset for {self.dollars} USD")
        order_info = self.connector.open_position(self.symbol, self.dollars)

        if not order_info:
            print("Opening position gone wrong. Quiting")
            return False

        print("Order filled!")
        print(f"Tried to buy for {order_info['notional']} USD")
        print(f"But bought {order_info['filled_qty']} {order_info['symbol']}")
        print(f"For {order_info['filled_avg_price']}")
        spent = float(order_info['filled_qty']) * \
            float(order_info['filled_avg_price'])
        print(f"We spent: {spent} USD")

        buy_price = float(order_info['filled_avg_price'])
        self.quantity += float(order_info['filled_qty'])
        # substruct what we paied for the asset
        self.dollars -= spent

        self.current_trade = Trade.create(buy_price=buy_price,
                                          quantity=self.quantity,
                                          buy_datetime=datetime.datetime.utcnow())

        return True

    def sell_all(self) -> bool:
        print(f"Selling {self.quantity} of {self.symbol}...")
        order_info = self.connector.close_position(self.symbol)
        if not order_info:
            print("Closing position gone wrong. Quiting")
            return False

        print("Order filled!")
        print(
            f"Sold {order_info['filled_qty']} {order_info['symbol']} USD")
        print(f"For {order_info['filled_avg_price']}")

        filled_quantity = float(order_info['filled_qty'])
        sell_price = float(order_info['filled_avg_price'])
        earned = filled_quantity * sell_price

        print(f"Earned: {earned} USD")

        self.dollars += earned
        self.quantity -= filled_quantity
        self.current_trade.sell_datetime = datetime.datetime.utcnow()
        self.current_trade.sell_price = sell_price
        self.current_trade.save()

        self.reset_variables()
        return True

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
            self.candlestick = last_candlestick
            self.__print_last_candlestick(last_candlestick)
            self.take_action()
            self.print_stats()

    def print_stats(self):
        super().print_stats()
        print("Live Trader status:")
        print(f"-{self.dollars} USD")
        print(f"-{self.quantity} {self.symbol}")
        print(f"-Take profit ratio: {environ('TAKE_PROFIT_RATIO')}")
        print(f"-Stop loss ratio: {environ('STOP_LOSS_RATIO')}")
        print(f"-RSI triggered: {self.rsi_triggered}")
        print(f"Current trade:")
        print(self.current_trade)
        if self.current_trade:
            unrealised_return = self.current_trade.get_potential_yield(
                self.candlestick['close'])
            print(
                f"Unrealised return: {unrealised_return} %")

    def __sleep(self, duration):
        print(f"Sleeping: {duration}s", end=' ')
        for _ in range(duration):
            print(".", end=' ', flush=True)
            time.sleep(1)
        print("Waking up")

    def __print_last_candlestick(self, last_cs):

        cs_time = last_cs['datetime']
        now = datetime.datetime.utcnow()
        print(f"Candlestick time: {cs_time.__str__()}")
        print(f"Now: {now.__str__()}")
        print(f"Delay: {now-cs_time}")
        print(last_cs)
