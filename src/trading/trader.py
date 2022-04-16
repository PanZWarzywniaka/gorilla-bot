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
                 clear_db=True,
                 update_db=True,
                 dollars=100,
                 starting_quantity=0,
                 take_profit_ratio=2,
                 stop_loss_ratio=1,
                 rsi_threshold=30,
                 ticker="BTC-USD",
                 period="7d",
                 interval="5m",
                 qty_increment_decimal_points=4
                 ) -> None:

        # initialize variables
        self.dollars = dollars
        self.quantity = starting_quantity
        self.take_profit_ratio = take_profit_ratio
        self.stop_loss_ratio = stop_loss_ratio
        self.rsi_threshold = rsi_threshold
        self.qty_increment_decimal_points = qty_increment_decimal_points

        self.rsi_triggered = False
        self.current_trade = None
        # database work
        if clear_db:
            self.__clear_database()

        if update_db:
            Candlestick.update_db_with_new_candlesticks(
                ticker, period, interval)

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
            self.current_trade.potential_return(
                c['close']) <= -self.stop_loss_ratio

    def take_profit_signal(self) -> bool:
        c = self.candlestick

        return self.__can_sell() and \
            self.current_trade.potential_return(
                c['close']) >= self.take_profit_ratio

    def reset_variables(self):
        self.rsi_triggered = False
        self.current_trade = None

    def __can_buy(self) -> bool:
        return self.current_trade is None  # we can buy, we don't have open position

    def __can_sell(self) -> bool:
        return self.current_trade is not None  # we can sell, if we have open position

        # ensures that the quantity we want to buy (qty) is up to qty_increment_decimal_points
    def round_quantity_down(self, qty: float) -> float:
        factor = 10 ** self.qty_increment_decimal_points
        return math.floor(qty * factor) / factor

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
