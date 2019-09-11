from peewee import *
from flask_login import UserMixin
import datetime

DATABASE = SqliteDatabase('stocks.sqlite')


class User(UserMixin, Model):
    username = CharField(unique=True)
    email = CharField()
    password = CharField()

    class Meta:
        database = DATABASE



class Stock(Model):
    name = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)
    owned_by: ForeignKeyField("User", backref="stocks")

    class Meta:
        database = DATABASE


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Stock], safe=True)
    print("TABLES CREATED")
    DATABASE.close()