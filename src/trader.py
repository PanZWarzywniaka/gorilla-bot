# external
from abc import abstractmethod
from datetime import datetime
import math
# owm
from util.visualizer import Visualizer
from models.trade import Trade
from models.trade import Candlestick


class Trader:

    def __init__(self,
                 dollars=100,
                 starting_quantity=0,
                 take_profit_ratio=2,
                 stop_loss_ratio=1,
                 rsi_threshold=30,
                 ticker="BTC-USD",
                 period="7d",
                 interval="5m",
                 ) -> None:

        # initialize variables
        self.dollars = dollars
        self.quantity = starting_quantity
        self.take_profit_ratio = take_profit_ratio
        self.stop_loss_ratio = stop_loss_ratio
        self.rsi_threshold = rsi_threshold

        self.rsi_triggered = False
        self.current_trade = None
        # database work
        self.__create_tables()
        print("Initilizing with historical data...")
        Candlestick.update_db_with_new_candlesticks(
            ticker, period=period, interval=interval)

    def take_action(self):
        # rsi signal
        if self.rsi_signal():
            self.rsi_triggered = True

        # buy
        if self.buy_signal():
            self.buy_all()

        # sell
        if self.stop_loss_signal() or self.take_profit_signal():
            self.sell_all()

    @abstractmethod
    def buy_all(self) -> bool: pass

    @abstractmethod
    def sell_all(self) -> bool: pass

    def rsi_signal(self) -> bool:
        return self.candlestick['rsi'] < self.rsi_threshold

    def buy_signal(self) -> bool:
        c = self.candlestick

        return self.__can_buy() and \
            self.rsi_triggered and \
            c['macd_crossover'] and \
            c['macd_above']

    def stop_loss_signal(self) -> bool:
        c = self.candlestick

        return self.__can_sell() and \
            self.current_trade.get_potential_yield(
                c['close']) <= -self.stop_loss_ratio

    def take_profit_signal(self) -> bool:
        c = self.candlestick

        return self.__can_sell() and \
            self.current_trade.get_potential_yield(
                c['close']) >= self.take_profit_ratio

    def reset_variables(self):
        self.rsi_triggered = False
        self.current_trade = None

    def __can_buy(self) -> bool:
        return not self.current_trade  # we can buy, we don't have open position

    def __can_sell(self) -> bool:
        return self.current_trade is not None  # we can sell, if we have open position

    def make_charts(self, start: datetime = None, end: datetime = None):
        Visualizer(self.data, self.rsi_threshold, start, end)

    def print_stats(self) -> None:
        Trade.print_stats()
        Candlestick.print_stats()

    def __clear_database(self):
        print("Clearing db...")

        Trade.clear_table()
        Candlestick.clear_table()

        print("Db cleared...")

    def __create_tables(self):
        print("Creating tables...")
        Trade.create_table()
        Candlestick.create_table()
        print("Tables created.")
