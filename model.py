from peewee import *
from datetime import datetime
from flask_login import  UserMixin

db = SqliteDatabase('CRM.db')


class Autorization(UserMixin, Model):
    login = TextField(unique=True)
    password = TextField()
    time = DateTimeField(default=datetime.now())
    full_name = TextField()
    balance = FloatField(default=0)
    class Meta:
        database = db

login = 'admin@admin.ru'


# db.connect()
# db.create_tables([Autorization])
# Autorization.create(login = 'user@user.ru', password = 'user1', full_name = 'Иван иванов иванович')
# Autorization.create(login = 'user2@user.ru', password = 'user2', full_name = 'Иван иванова иванович')
# Autorization.create(login = 'admin@admin.ru', password = '1234', full_name = 'Админов Админ Админович')
user = Autorization.select().where(Autorization.login == login).first()

test = Autorization.select().where(Autorization.id == user).first()

