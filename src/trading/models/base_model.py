from peewee import MySQLDatabase
from peewee import Model


class BaseModel(Model):
    class Meta:
        database = MySQLDatabase('trading', user='root', password='dupadupadupa',
                                 host='127.0.0.1', port=3306)
        connected = database.connect()

    @classmethod
    def clear_table(cls):
        cls.delete().execute()
        return True
