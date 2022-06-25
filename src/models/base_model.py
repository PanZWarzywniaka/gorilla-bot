from abc import abstractmethod
from peewee import MySQLDatabase
from peewee import Model
from os import environ
from util.logger import log_info


class BaseModel(Model):
    class Meta:
        database = MySQLDatabase(environ.get('MYSQL_DATABASE'), user='root', password=environ.get('MYSQL_ROOT_PASSWORD'),
                                 host="database", port=3306)
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
        log_info(f"\n\nPrinting {cls.__name__}'s stats: \n")
        log_info(f"There are {cls.count()} {cls.__name__.lower()}s \n")

    @classmethod
    @abstractmethod
    def get_first(cls): pass

    @classmethod
    @abstractmethod
    def get_last(cls): pass
