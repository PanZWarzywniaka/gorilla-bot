from datetime import datetime
import yfinance as yf
import pandas as pd
import numpy as np
import pandas_ta as ta
from schema import db, Candlestick


class DataHandler():
    def __init__(self,
                 ticker="BTC-USD",
                 period="7d",
                 interval="5m",
                 rsi_length=14
                 ) -> None:

        self.ticker = ticker
        self.period = period
        self.interval = interval
        self.rsi_length = rsi_length

        self.__download_data()
        self.__process_data()
        # self.__start_database()
        # self.__save_data()

    def __download_data(self):
        print("Downloading...")
        self.data = yf.download(
            tickers=self.ticker,
            period=self.period,
            interval=self.interval,
            # start="2022-03-07",
            # end="2022-03-14"
        )

    def __calculate_rsi(self):
        self.data.ta.rsi(close='close', length=self.rsi_length, append=True)
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
                f'MACD_{fast}_{slow}_{signal}': 'macd_fast',
                f'MACDs_{fast}_{slow}_{signal}': 'macd_slow',
                f'MACDh_{fast}_{slow}_{signal}': 'macd_hist',

            }, inplace=True)

        self.data['macd_above'] = self.data['macd_fast'] >= self.data['macd_slow']
        self.data['macd_crossover'] = self.data['macd_above'].diff()

        self.data['action_observed'] = 0

    def __process_data(self):

        self.__calculate_rsi()
        self.__calculate_macd()
        pd.set_option("display.max_columns", None)
        self.data.columns = self.data.columns.str.lower()
        print(self.data.columns)
        print(self.data)
        self.data.index.name = 'datetime'

    def __start_database(self):
        db.connect()
        db.create_tables([Candlestick])

    def __save_data(self):
        candlesticks = list(self.data.itertuples(name=None))

        print("Writing to db:")
        with db.atomic():
            for c in candlesticks:
                Candlestick.create(
                    datetime=c[0],
                    open=c[1],
                    high=c[2],
                    low=c[3],
                    close=c[4],
                    adj_close=c[5],
                    volume=c[6]
                )
