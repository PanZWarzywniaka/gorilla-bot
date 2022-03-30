from cgitb import reset
from peewee import MySQLDatabase, Model, FloatField, DateTimeField, ForeignKeyField

db = MySQLDatabase('trading', user='root', password='dupadupadupa',
                   host='127.0.0.1', port=3306)


class BaseModel(Model):
    class Meta:
        database = db


class Candlestick(BaseModel):
    datetime = DateTimeField(unique=True, null=False,
                             index=True, primary_key=True)
    open = FloatField(null=False, index=True)
    high = FloatField(null=False, index=True)
    low = FloatField(null=False, index=True)
    close = FloatField(null=False, index=True)
    adj_close = FloatField(null=False, index=True)
    volume = FloatField(null=False, index=True)


class Trade(BaseModel):
    buy_cs = ForeignKeyField(Candlestick, unique=True, null=False)
    sell_cs = ForeignKeyField(Candlestick, unique=True, null=True)

    @staticmethod
    def calculate_profit():
        trades = Trade.select()
        result = 1
        for t in trades:
            sell_price = t.sell_cs.open
            buy_price = t.buy_cs.open
            result *= sell_price/buy_price
        print(result)
