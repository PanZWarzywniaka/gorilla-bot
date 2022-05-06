# external
from abc import abstractmethod
from datetime import datetime
import math
# owm
from util.visualizer import Visualizer
from models.trade import Trade
from models.candlestick import Candlestick
from os import environ


class Trader:

    def __init__(self,
                 dollars,
                 ) -> None:

        # initialize variables
        self.dollars = dollars
        self.quantity = 0

        self.rsi_triggered = False
        self.current_trade = None
        # database work
        self.__create_tables()

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
        return self.candlestick['rsi'] <= float(environ.get('RSI_THRESHOLD'))

    def buy_signal(self) -> bool:
        c = self.candlestick

        return self.__can_buy() and \
            self.rsi_triggered and \
            c['macd_crossover'] and \
            c['macd_above']

    def stop_loss_signal(self) -> bool:
        c = self.candlestick
        stop_loss_ratio = float(environ.get('STOP_LOSS_RATIO'))

        return self.__can_sell() and \
            self.current_trade.get_potential_yield(
                c['close']) <= -stop_loss_ratio

    def take_profit_signal(self) -> bool:
        c = self.candlestick
        take_profit_ratio = float(environ.get('TAKE_PROFIT_RATIO'))

        return self.__can_sell() and \
            self.current_trade.get_potential_yield(
                c['close']) >= take_profit_ratio

    def reset_variables(self):
        self.rsi_triggered = False
        self.current_trade = None

    def __can_buy(self) -> bool:
        return not self.current_trade  # we can buy, we don't have open position

    def __can_sell(self) -> bool:
        return self.current_trade is not None  # we can sell, if we have open position

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
