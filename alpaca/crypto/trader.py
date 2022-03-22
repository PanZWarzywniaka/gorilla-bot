# external
from datetime import datetime
import yfinance as yf
import pandas as pd
import numpy as np
import pandas_ta as ta
import json

# owm
from schema import db, Candlestick
from visualizer import Visualizer


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
        self.ticker = ticker
        self.period = period
        self.interval = interval

        self.data = None
        self.price_at_entry = None
        self.rsi_signal = False

    def buy_all(self) -> bool:
        if self.dollars == 0:
            return False

        price_for_asset = self.candlestick["Open"]
        self.price_at_entry = price_for_asset
        self.asset = self.dollars/price_for_asset
        self.dollars = 0

        print(f"Bought asset  " +
              f"Time: {self.candlestick['Datetime']}")
        return True

    def trade_result(self, exit_price):
        return (exit_price/self.price_at_entry-1)*100

    def sell_all(self) -> bool:
        if self.asset == 0:
            return False

        price_for_asset = self.candlestick["Open"]

        print(f"Selling asset " +
              f"Time: {self.candlestick['Datetime']}")
        print(
            f"\nProfit on trade: {self.trade_result(price_for_asset)} % \n")

        self.dollars = self.asset*price_for_asset
        self.asset = 0
        self.price_at_entry = None
        self.rsi_signal = False

        return True

    def check_rsi_signal(self) -> bool:
        c = self.candlestick

        return c['RSI'] < self.rsi_threshold

    def buy_signal(self) -> bool:
        c = self.candlestick
        ret = c['MACD_crossover'] and c['MACD_above'] and self.rsi_signal
        return ret

    def stop_loss_signal(self) -> bool:
        if self.price_at_entry is None:
            return False
        c = self.candlestick
        return self.trade_result(c['Open']) <= -self.stop_loss_ratio

    def take_profit_signal(self) -> bool:
        if self.price_at_entry is None:
            return False

        c = self.candlestick
        return self.trade_result(c['Open']) >= self.take_profit_ratio

    def calculate_profit(self):

        df = self.data.reset_index()
        for index, c in df.iterrows():

            self.index = index
            self.candlestick = c

            # rsi signal
            if self.check_rsi_signal():
                self.rsi_signal = True
                self.data.at[c['Datetime'], 'action_observed'] = 1
            # buy
            if self.buy_signal():
                self.buy_all()
                self.data.at[c['Datetime'], 'action_observed'] = 2

            # sell
            if self.stop_loss_signal() or self.take_profit_signal():
                self.sell_all()
                self.data.at[c['Datetime'], 'action_observed'] = 3

        # end of time
        self.candlestick = df.iloc[-1]  # last candle stick
        self.sell_all()

    def __set_signal():
        pass

    def print_json(self, raw_json):
        print(json.dumps(raw_json, indent=4))

    def start_database(self):
        db.connect()
        db.create_tables([Candlestick])

    def save_data(self):
        df = self.data.reset_index()
        print("Creating list to insert")
        json = df.to_json(orient="records")
        # self.print_json(json)
        print("Writing to db")
        # for index, candlestick in df.iterrows():
        #     # obj =
        #     print(f"Writing to database: {index}")
        #     c = candlestick
        #     d = datetime.strftime(c['Datetime'], "%Y-%m-%d %H:%M:%S+%z")
        #     Candlestick.create(
        #         datetime=d,
        #         open=float(c['Open']),
        #         high=float(c['High']),
        #         low=float(c['Low']),
        #         close=float(c['Close']),
        #         adj_close=float(c['Adj Close']),
        #         volume=float(c['Volume'])
        #     ).save()

    def download_data(self):
        print("Downloading...")
        self.data = yf.download(
            tickers=self.ticker,
            period=self.period,
            interval=self.interval,
            # start="2022-01-13",
            # end="2022-03-13"
        )

    def __calculate_rsi(self):
        self.data.ta.rsi(close='Close', length=self.rsi_length, append=True)
        self.data.rename(
            columns={f'RSI_{self.rsi_length}': 'RSI'}, inplace=True)

    def __calculate_macd(self):
        fast = 12
        slow = 26
        signal = 9

        self.data.ta.macd(close='close', fast=fast,
                          slow=slow, signal=signal, append=True)

        self.data.rename(
            columns={
                f'MACD_{fast}_{slow}_{signal}': 'MACD_fast',
                f'MACDs_{fast}_{slow}_{signal}': 'MACD_slow',
                f'MACDh_{fast}_{slow}_{signal}': 'MACD_hist',

            }, inplace=True)

        self.data['MACD_above'] = self.data['MACD_fast'] >= self.data['MACD_slow']
        self.data['MACD_crossover'] = self.data['MACD_above'].diff()

        self.data['action_observed'] = 0

    def process_data(self):

        self.__calculate_rsi()
        self.__calculate_macd()
        pd.set_option("display.max_columns", None)
        print(self.data.columns)
        print(self.data)

    def make_charts(self):
        Visualizer(self.data, self.rsi_threshold)
