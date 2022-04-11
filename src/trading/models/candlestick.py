from datetime import tzinfo
from .base_model import BaseModel
from .processors.candlestick_processor import CandlestickProcessor
from peewee import DateTimeField, FloatField
import pandas as pd
import yfinance as yf


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
    def save(cls, new: pd.DataFrame):

        def get_candlesticks_to_insert(existing: pd.DataFrame, new: pd.DataFrame) -> list:

            if existing.empty:  # if existing CS's is empty, insert all new CS's
                to_insert_list = list(new.itertuples(name=None))
                return to_insert_list

            # last CS in list, first item of cs no tzinfo
            first_cs_time = cls.get_first_row().datetime
            last_cs_time = cls.get_last_row().datetime

            # find out which CS's have later datetime than already exsting ones # with tz info
            before_first = new.loc[:first_cs_time].iloc[:-1]
            before_first_list = list(before_first.itertuples(name=None))

            after_last = new.loc[last_cs_time:].iloc[1:]
            after_last_list = list(after_last.itertuples(name=None))

            to_insert_list = before_first_list + after_last_list
            return to_insert_list

        to_insert = get_candlesticks_to_insert(cls.load(), new)
        print("Writing to db...")
        print(f"Writing {len(to_insert)} candlesticks.")
        cls.insert_many(to_insert,
                        fields=[
                            cls.datetime,
                            cls.open,
                            cls.high,
                            cls.low,
                            cls.close,
                            cls.adj_close,
                            cls.volume,
                        ]).execute()

        print("Writing complete.")
        print("Loading from db...")

    @classmethod
    def load(cls) -> pd.DataFrame:
        print("Loading data...")
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
        print("Data loaded.")
        return df

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

    @staticmethod
    def download_yahoo_candlestics(tickers, period, interval) -> pd.DataFrame:

        df = yf.download(
            tickers=tickers,
            period=period,
            interval=interval,
            # start="2022-03-07",
            # end="2022-03-14"
        )

        last_cs = df.iloc[-1:]
        if last_cs.index.minute % 5 != 0:  # not 5m interval
            df = df[:-1]  # droping last row
        return df

    @classmethod
    def get_first_row(cls):
        return cls.select().order_by(cls.datetime.asc()).get()

    @classmethod
    def get_last_row(cls):
        return cls.select().order_by(cls.datetime.desc()).get()
