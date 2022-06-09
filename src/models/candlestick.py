import datetime
import pytz
from .base_model import BaseModel
from util.processors.candlestick_processor import CandlestickProcessor
from peewee import DateTimeField, FloatField
import pandas as pd
import yfinance as yf
import time


class Candlestick(BaseModel):
    datetime = DateTimeField(unique=True, null=False,
                             index=True, primary_key=True)
    open = FloatField(null=False, index=True)
    high = FloatField(null=False, index=True)
    low = FloatField(null=False, index=True)
    close = FloatField(null=False, index=True)
    adj_close = FloatField(null=False, index=True)
    volume = FloatField(null=False, index=True)

    @classmethod
    def save_multiple(cls, new: pd.DataFrame):

        def get_candlesticks_to_insert(existing: pd.DataFrame, new: pd.DataFrame) -> list:

            if existing.empty:  # if existing CS's is empty, insert all new CS's
                to_insert_list = list(new.itertuples(name=None))
                return to_insert_list

            # cetting first and last datetimes, localizing to avoid errors
            first_cs_time = cls.get_first().datetime.replace(tzinfo=pytz.UTC)
            last_cs_time = cls.get_last().datetime.replace(tzinfo=pytz.UTC)

            # find out which CS's have later datetime than already exsting ones # with tz info
            before_first = new.loc[:first_cs_time].iloc[:-1]
            before_first_list = list(before_first.itertuples(name=None))

            after_last = new.loc[last_cs_time:].iloc[1:]
            after_last_list = list(after_last.itertuples(name=None))

            to_insert_list = before_first_list + after_last_list
            return to_insert_list

        to_insert = get_candlesticks_to_insert(cls.load(), new)
        return cls.insert_many(to_insert,
                               fields=[
                                   cls.datetime,
                                   cls.open,
                                   cls.high,
                                   cls.low,
                                   cls.close,
                                   cls.adj_close,
                                   cls.volume,
                               ]).execute()

    @classmethod
    def load(cls) -> pd.DataFrame:
        # print("Loading data...")
        query = cls.select()

        columns = {
            'Open': [c.open for c in query],
            'High': [c.high for c in query],
            'Low': [c.low for c in query],
            'Close': [c.close for c in query],
            'Adj close': [c.adj_close for c in query],
            'Volume': [c.volume for c in query],
        }

        df = pd.DataFrame(columns, index=[c.datetime for c in query])
        # print("Data loaded.")
        return df

    @classmethod
    def create_from_price(cls, price: float):
        print(f"Creating new cs from price {price}")
        return cls.create(
            datetime=datetime.datetime.now(),
            open=price,
            high=price,
            low=price,
            close=price,
            adj_close=price,
            volume=0,
        )

    @staticmethod
    def process_candlesticks(df) -> pd.DataFrame:
        return CandlestickProcessor(df, rsi_length=14,
                                    macd_fast=12,
                                    macd_slow=26,
                                    macd_signal=9
                                    ).processed_data

    @classmethod
    def get_processed_candlesticks(cls) -> pd.DataFrame:
        df = cls.load()
        return cls.process_candlesticks(df)

    @classmethod
    def update_db_with_new_candlesticks(cls, ticker, period, interval, start=None, end=None):
        # print("Updating database...")
        df = cls.download_yahoo_candlestics(
            ticker, period, interval, start, end)

        return cls.save_multiple(df)

    @staticmethod
    def download_yahoo_candlestics(ticker, period, interval, start=None, end=None, timeout=10) -> pd.DataFrame:
        ticker += "-USD"  # from "XXX" ticker symbol to "XXX-USD" required by yahoo
        for _ in range(timeout):
            try:
                df = yf.download(
                    tickers=ticker,
                    period=period,
                    interval=interval,
                    start=start,
                    end=end
                )
                # needs to be refactored doesnt support diffrent intervals than 5m
                last_cs = df.iloc[-1:]
                if last_cs.index.minute % 5 != 0:  # not 5m interval
                    df = df[:-1]  # droping last row
                return df
            except Exception:  # what ever gone wrong just try to download again
                time.sleep(10)

    @classmethod
    def get_first(cls):
        return cls.select().order_by(cls.datetime.asc()).get()

    @classmethod
    def get_last(cls):
        return cls.select().order_by(cls.datetime.desc()).get()

    def __str__(self):
        ret = "CANDLESTICK: \n"
        ret += f"Time: {self.datetime.__str__()}\n"
        ret += f"Open: {self.open}\n"
        ret += f"High: {self.high}\n"
        ret += f"Low: {self.low}\n"
        ret += f"Close: {self.close}\n"
        ret += f"Adj_close: {self.adj_close}\n"
        ret += f"Volume: {self.volume}\n"
        return ret

    @ classmethod
    def print_stats(cls) -> None:
        super().print_stats()

        first_cs_datetime = cls.get_first().datetime
        last_cs_datetime = cls.get_last().datetime

        print(f"First at: {first_cs_datetime}")
        print(f"Last at: {last_cs_datetime}\n")
        print(f"Covering: {last_cs_datetime-first_cs_datetime}\n")
