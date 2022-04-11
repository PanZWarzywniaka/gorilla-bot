# external
from datetime import datetime
import json

# owm
from util.visualizer import Visualizer
from models.trade import Trade
from models.trade import Candlestick


class Trader:

    def __init__(self,
                 clear_db=True,
                 update_db=True,
                 dollars=100,
                 starting_asset=0,
                 take_profit_ratio=2,
                 stop_loss_ratio=1,
                 rsi_threshold=30,
                 ticker="BTC-USD",
                 period="7d",
                 interval="5m") -> None:

        # initialize variables
        self.dollars = dollars
        self.asset = starting_asset
        self.take_profit_ratio = take_profit_ratio
        self.stop_loss_ratio = stop_loss_ratio
        self.rsi_threshold = rsi_threshold

        self.rsi_triggered = False
        self.current_trade = None

        # database work
        if clear_db:
            self.__clear_database()

        if update_db:
            self.__update_db_with_new_candlesticks(ticker, period, interval)

        self.data = Candlestick.get_processed_candlesticks()

    def __update_db_with_new_candlesticks(self, ticker, period, interval):
        df = Candlestick.download_yahoo_candlestics(
            ticker, period, interval)
        Candlestick.save(df)

    def __clear_database(self):
        print("Clearing db...")
        classes = [Trade, Candlestick, ]
        list(map(lambda x: x.clear_table(x), classes))
        print("Db cleared...")

    def buy_all(self) -> bool:

        self.current_trade = Trade.create(buy_cs=self.candlestick.datetime)

        price_for_asset = self.candlestick["open"]
        self.asset = self.dollars/price_for_asset
        self.dollars = 0

        return True

    def sell_all(self) -> bool:
        if self.current_trade is None:
            return False

        price_for_asset = self.candlestick["open"]
        self.dollars = self.asset*price_for_asset
        self.asset = 0
        self.current_trade.sell_cs = self.candlestick.datetime
        self.current_trade.save()

        self.__reset_variables()
        return True

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
                c['open']) <= -self.stop_loss_ratio

    def take_profit_signal(self) -> bool:
        c = self.candlestick

        return self.__can_sell() and \
            self.current_trade.potential_return(
                c['open']) >= self.take_profit_ratio

    def __reset_variables(self):
        self.price_at_entry = None
        self.rsi_triggered = False
        self.current_trade = None

    def __can_buy(self) -> bool:
        if self.dollars == 0:
            return False

        if self.current_trade is not None:
            return False

        return True

    def __can_sell(self) -> bool:
        if self.asset == 0:
            return False

        return True

    def make_charts(self, start: datetime = None, end: datetime = None):
        Visualizer(self.data, self.rsi_threshold, start, end)
