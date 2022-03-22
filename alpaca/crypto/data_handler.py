import yfinance as yf
import pandas as pd
import numpy as np
import pandas_ta as ta


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

    # def start_database(self):
    #     db.connect()
    #     db.create_tables([Candlestick])

    # def save_data(self):
    #     df = self.data.reset_index()
    #     print("Creating list to insert")
    #     json = df.to_json(orient="records")
    #     # self.print_json(json)
    #     print("Writing to db")
    #     # for index, candlestick in df.iterrows():
    #     #     # obj =
    #     #     print(f"Writing to database: {index}")
    #     #     c = candlestick
    #     #     d = datetime.strftime(c['datetime'], "%Y-%m-%d %H:%M:%S+%z")
    #     #     Candlestick.create(
    #     #         datetime=d,
    #     #         open=float(c['open']),
    #     #         high=float(c['High']),
    #     #         low=float(c['Low']),
    #     #         close=float(c['Close']),
    #     #         adj_close=float(c['Adj Close']),
    #     #         volume=float(c['Volume'])
    #     #     ).save()
