from datetime import datetime
from peewee import FloatField, DateTimeField
from models.candlestick import Candlestick
from models.base_model import BaseModel
import pandas as pd


class Trade(BaseModel):

    quantity = FloatField(null=False, index=True)
    buy_price = FloatField(null=False, index=True)
    buy_datetime = DateTimeField(null=False, unique=True, index=True)

    sell_price = FloatField(null=True, index=True)
    sell_datetime = DateTimeField(null=True, unique=True, index=True)

    @staticmethod
    def load(start: datetime = None, end: datetime = None) -> pd.DataFrame:
        print("Loading trades...")
        query = Trade.select()

        if start:
            query = query.where(Trade.buy_datetime >= start)

        if end:
            query = query.where(Trade.buy_datetime <= end)

        columns = {
            'quantity': [t.quantity for t in query],
            'buy_price': [t.buy_price for t in query],
            'buy_datetime': [t.buy_datetime for t in query],
            'sell_price': [t.sell_price for t in query],
            'sell_datetime': [t.sell_datetime for t in query],
        }

        df = pd.DataFrame(columns, index=[t.id for t in query])
        print("Trades loaded.")
        return df

    def __str__(self):
        info = f"\nBought: {self.quantity}\n"
        info += f"For: {self.buy_price} USD per asset\n"
        info += f"At: {self.buy_datetime}\n"

        if self.sell_price and self.sell_datetime:
            info += f"Sold for: {self.sell_price} USD per asset\n"
            info += f"At: {self.sell_datetime}\n"
            info += f"Trade yield: {self.get_yield()} %"

        return info

    @classmethod
    def print_stats(cls) -> None:
        super().print_stats()
        trades = cls.select()

        result = 1
        for t in trades:
            print(t, end='')
            if t.sell_price:
                t_yield = t.get_yield()
                result *= t_yield

                print(f"This trade yield: {t_yield} %")

        print(f"\nTOTAL Calculated profit: {result}")

    @classmethod
    def get_last(cls):
        cls.select().order_by(cls.id.desc()).get()

    def get_yield(self):
        return 100*(self.sell_price/self.buy_price-1)

    def get_potential_yield(self, sell_price):
        return 100*(sell_price/self.buy_price-1)
