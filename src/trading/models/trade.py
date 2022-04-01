from peewee import ForeignKeyField
from models.candlestick import Candlestick
from models.base_model import BaseModel


class Trade(BaseModel):
    buy_cs = ForeignKeyField(Candlestick, unique=True, null=False)
    sell_cs = ForeignKeyField(Candlestick, unique=True, null=True)

    def calculate_return(self):
        sell_price = self.sell_cs.open
        buy_price = self.buy_cs.open
        return sell_price/buy_price

    @staticmethod
    def calculate_investment_return():
        trades = Trade.select()
        result = 1
        for t in trades:
            result *= t.calculate_return()
        print(result)
