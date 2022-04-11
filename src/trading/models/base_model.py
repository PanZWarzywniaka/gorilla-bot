from abc import abstractmethod
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

    @classmethod
    def count(cls) -> int:
        return cls.select().count()

    @classmethod
    def print_stats(cls) -> None:
        print(f"\n\nPrinting {cls.__name__}'s stats: \n")
        print(f"There are {cls.count()} {cls.__name__.lower()}s \n")

    @classmethod
    @abstractmethod
    def get_first_row(cls): pass

    @classmethod
    @abstractmethod
    def get_last_row(cls): pass
