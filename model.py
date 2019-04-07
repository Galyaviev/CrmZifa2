from peewee import *
from datetime import datetime
from flask_login import UserMixin

db = SqliteDatabase('CRM.db')


class Autorization(UserMixin, Model):
    login = TextField(unique=True)
    password = TextField()
    time = DateTimeField(default=datetime.today().replace(microsecond=0))
    full_name = TextField()

    class Meta:
        database = db


class Balance(Model):
    owner = ForeignKeyField(Autorization, related_name='balances')
    balance = FloatField(default=0)
    time = DateTimeField(default=datetime.today().replace(microsecond=0))

    class Meta:
        database = db


class Thing(Model):
    owner = ForeignKeyField(Autorization, related_name='things')
    name_thing = TextField()
    size = TextField()
    price = FloatField()
    currently = FloatField()
    time = DateTimeField(default=datetime.today().replace(microsecond=0))
    shop = TextField()
    weght = FloatField(default=0)
    price_delivery = FloatField(default=0)
    time_delivery = DateTimeField(default=0)

    class Meta:
        database = db


#
# Thing.create(
#     owner=Autorization.select().where(Autorization.login == '1@1.ru').get(),
#     name_thing = 'штаны',
#     size = '12',
#     price = 14,
#     currently = 70,
#     shop = 'NExt')



# db.create_tables([Thing])
# db.drop_tables([Thing])







# Autorization.create(login = 'user@user.ru', password = 'user1', full_name = 'Иван иванов иванович')
# Balance.delete().where(Balance.id == 6).execute()
# #
# db.connect()
# db.create_tables([Autorization])
# db.create_tables([Balance])
# Создание Юсеров
# Autorization.create(login = 'user@user.ru', password = 'user1', full_name = 'Иван иванов иванович')
# Autorization.create(login = 'user2@user.ru', password = 'user2', full_name = 'Иван иванова иванович')
# Autorization.create(login = 'admin@admin.ru', password = '1234', full_name = 'Админов Админ Админович')
# Сощдание балансов
# Balance.create(owner=Autorization.select().where(Autorization.login == 'admin@admin.ru').get())
# Balance.create(owner=Autorization.select().where(Autorization.login == 'admin@admin.ru').get(), balance=-350.23)
# Balance.create(owner=Autorization.select().where(Autorization.login == 'asasa@sdsdsd.ru').get(), balance=-325.45)

# user  = Autorization.select().where(Autorization.id == 3).get()
# print(user)

#
# balance_user = Balance.select().where(Balance.owner == Autorization.select().where(Autorization.login == 'misha@yandex.ru').get())
# for i in balance_user:
#     i.time = str(i.time).split()
#     print(i.time[0])


#
# balance_user = Balance.select().where(Balance.owner == Autorization.select().where(Autorization.login == user.login).get())
# for i in balance_user:
#     print(i.balance, i.time)



# balances_user = Balance.select().where(Balance.owner == user.id)
# list = []
# for balance in balances_user:
#     list.append(balance.balance)
#
# print(balance)

#
# data = Autorization.select().order_by(Autorization.time.desc())
#
# auto = []
# a = 0
# for i in data:
#     for b in i.balances:
#         a = a + b.balance
#     auto.append((i.id, i.login, i.password, str(i.time), i.full_name, a))
#     print(a)
#     a = 0
#
#
#
# print(auto)