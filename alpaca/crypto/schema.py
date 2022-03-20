from peewee import SqliteDatabase, Model, IntegerField, FloatField, DateField

db = SqliteDatabase("trading.db")


class BaseModel(Model):
    class Meta:
        database = db


class Candlestick(BaseModel):
    datetime = DateField(null=False, index=True)
    open = IntegerField(null=False, index=True)
    high = IntegerField(null=False, index=True)
    low = IntegerField(null=False, index=True)
    close = IntegerField(null=False, index=True)
    adj_close = IntegerField(null=False, index=True)
    volume = IntegerField(null=False, index=True)
