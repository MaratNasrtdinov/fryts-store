from peewee import *
db = SqliteDatabase('db/database.db')

class User(Model):
    id = PrimaryKeyField(unique=True)
    user_id = IntegerField()
    username = CharField()
    name = CharField()

    class Meta:
        database = db
        ordering = 'id'
        db_table = 'users'



class Catalog(Model):
    id = PrimaryKeyField(unique=True)
    name = CharField()
    quantity = IntegerField()
    price = IntegerField()
    description = TextField(null=True)
    class Meta:
        database = db
        ordering = 'id'
        db_table = 'catalog'


class Cart(Model):
    user_id = IntegerField()
    username = CharField()
    product = CharField()
    quantity = IntegerField()
    price = IntegerField()

    class Meta:
        database = db
        ordering = 'user_id'
        db_table = 'cart'


class Order(Model):
    id = PrimaryKeyField(unique=True)
    user_id = CharField()
    class Meta:
        database = db
        db_table = 'order'