from datetime import datetime
from peewee import ForeignKeyField
from models.candlestick import Candlestick
from models.base_model import BaseModel
import pandas as pd


class Trade(BaseModel):
    buy_cs = ForeignKeyField(Candlestick, unique=True, null=False)
    sell_cs = ForeignKeyField(Candlestick, unique=True, null=True)

    @staticmethod
    def load(start: datetime = None, end: datetime = None) -> pd.DataFrame:
        print("Loading trades...")
        query = Trade.select()

        if start is not None:
            query = query.where(Trade.buy_cs >= start)

        if end is not None:
            query = query.where(Trade.buy_cs <= end)

        columns = {
            'buy_cs': [t.buy_cs for t in query],
            'sell_cs': [t.sell_cs for t in query],
        }

        df = pd.DataFrame(columns, index=[t.id for t in query])
        print("Trades loaded.")
        return df

    @staticmethod
    def calculate_investment_return():
        trades = Trade.select()
        result = 1
        for t in trades:
            result *= t.calculate_return()
        print(result)

    def calculate_return(self):
        sell_price = self.sell_cs.open
        buy_price = self.buy_cs.open
        return sell_price/buy_price

    def potential_return(self, sell_price):
        buy_price = self.buy_cs.open
        return 100*(sell_price/buy_price-1)
