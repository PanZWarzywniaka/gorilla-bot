# external
from datetime import datetime
import json

# owm
from visualizer import Visualizer
from data_handler import DataHandler
from schema import Trade


class Trader:

    def __init__(self,
                 dollars=100,
                 starting_asset=0,
                 take_profit_ratio=2,
                 stop_loss_ratio=1,
                 rsi_threshold=30,
                 rsi_length=14,
                 ticker="BTC-USD",
                 period="7d",
                 interval="5m") -> None:

        self.dollars = dollars
        self.asset = starting_asset
        self.take_profit_ratio = take_profit_ratio
        self.stop_loss_ratio = stop_loss_ratio
        self.rsi_threshold = rsi_threshold
        self.rsi_length = rsi_length

        self.data = DataHandler(
            ticker=ticker, period=period, interval=interval, rsi_length=rsi_length).data

        self.price_at_entry = None
        self.rsi_signal = False

        self.current_trade = None

    def buy_all(self) -> bool:
        if self.dollars == 0:
            return False

        price_for_asset = self.candlestick["open"]
        self.price_at_entry = price_for_asset
        self.asset = self.dollars/price_for_asset
        self.dollars = 0

        print(f"Bought asset  " +
              f"Time: {self.candlestick['datetime']}")
        return True

    def trade_result(self, exit_price):
        return (exit_price/self.price_at_entry-1)*100

    def sell_all(self) -> bool:
        if self.asset == 0:
            return False

        price_for_asset = self.candlestick["open"]

        print(f"Selling asset " +
              f"Time: {self.candlestick['datetime']}")
        print(
            f"\nProfit on trade: {self.trade_result(price_for_asset)} % \n")

        self.dollars = self.asset*price_for_asset
        self.asset = 0
        self.price_at_entry = None
        self.rsi_signal = False

        self.current_trade.sell_cs = self.candlestick.datetime
        self.current_trade.save()
        self.current_trade = None

        return True

    def check_rsi_signal(self) -> bool:
        c = self.candlestick

        return c['rsi'] < self.rsi_threshold

    def buy_signal(self) -> bool:
        c = self.candlestick
        ret = c['macd_crossover'] and c['macd_above'] and self.rsi_signal
        return ret

    def stop_loss_signal(self) -> bool:
        if self.price_at_entry is None:
            return False
        c = self.candlestick
        return self.trade_result(c['open']) <= -self.stop_loss_ratio

    def take_profit_signal(self) -> bool:
        if self.price_at_entry is None:
            return False

        c = self.candlestick
        return self.trade_result(c['open']) >= self.take_profit_ratio

    def calculate_profit(self):

        df = self.data.reset_index()
        for index, c in df.iterrows():

            self.index = index
            self.candlestick = c

            # rsi signal
            if self.check_rsi_signal():
                self.rsi_signal = True
                self.data.at[c['datetime'], 'action_observed'] = 1
            # buy
            if self.buy_signal():
                self.buy_all()
                self.data.at[c['datetime'], 'action_observed'] = 2
                if self.current_trade is None:
                    self.current_trade = Trade.create(buy_cs=c.datetime)

            # sell
            if self.stop_loss_signal() or self.take_profit_signal():
                self.sell_all()
                self.data.at[c['datetime'], 'action_observed'] = 3

        # end of time
        self.candlestick = df.iloc[-1]  # last candle stick
        self.sell_all()
        print(f"MONEY: {self.dollars} $$$")

    def __set_signal():  # to be implemted
        pass

    def print_json(self, raw_json):
        print(json.dumps(raw_json, indent=4))

    def make_charts(self):
        Visualizer(self.data, self.rsi_threshold)
