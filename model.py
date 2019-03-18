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
# Balance.create(owner=Autorization.select().where(Autorization.login == 'admin@admin.ru').get(), balance=-500)
# Balance.create(owner=Autorization.select().where(Autorization.login == 'user2@user.ru').get(), balance=1000)

# user  = Autorization.select().where(Autorization.id == 3).get()
# print(user)


# balance_user = Balance.select().where(Balance.owner == Autorization.select().where(Autorization.login == 'admin@admin.ru').get())
# for i in balance_user:
#     print(i.balance, i.time)

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

