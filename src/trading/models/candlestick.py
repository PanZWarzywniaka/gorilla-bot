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

    @staticmethod
    def save(df: pd.DataFrame):
        candlestick_list = list(df.itertuples(name=None))

        print("Writing to db...")
        # with BaseModel.Meta.database.atomic():
        Candlestick.insert_many(candlestick_list,
                                fields=[
                                    Candlestick.datetime,
                                    Candlestick.open,
                                    Candlestick.high,
                                    Candlestick.low,
                                    Candlestick.close,
                                    Candlestick.adj_close,
                                    Candlestick.volume,
                                ]).execute()

        print("Writing complete.")
        print("Loading from db...")

    @staticmethod
    def load() -> pd.DataFrame:
        query = Candlestick.select()

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
    def process_candlestics(df) -> pd.DataFrame:
        return CandlestickProcessor(df, rsi_length=14,
                                    macd_fast=12,
                                    macd_slow=26,
                                    macd_signal=9
                                    ).processed_data

    @staticmethod
    def download_yahoo_candlestics(tickers, period, interval) -> pd.DataFrame:

        return yf.download(
            tickers=tickers,
            period=period,
            interval=interval,
            # start="2022-03-07",
            # end="2022-03-14"
        )
