from flask import Flask, render_template, request, url_for, redirect, flash
from model import *
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.secret_key = 'ubuntu'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return Autorization.select().where(Autorization.id == user_id).first()


@app.route('/thing_edit/<id>', methods=['POST', 'GET'])
@login_required
def thing_edit(id):
    if current_user.login == 'admin@admin.ru':
        if request.method == "POST":
            weght = request.form['weght']
            price_delivery = request.form['price_delivery']
            time_delivery = request.form['time_delivery']
            Thing.update(weght=weght, price_delivery=price_delivery, time_delivery=time_delivery).where(
                Thing.id == id).execute()
            return redirect(url_for('things'))

        data = Thing.select().where(Thing.id == id).get()
        full_name = Autorization.select().where(Autorization.id == data.owner_id).first()
        auto = []
        auto.append(
            (full_name.full_name, data.name_thing, data.weght, data.price_delivery, data.time_delivery, data.id))
        data = auto[0]
        return render_template('thing_edit.html', data=data)
    else:
        return '<h1>Вам сюда нельзя</h1>'


@app.route('/thing_add', methods=['POST', 'GET'])
@login_required
def thing_add():
    if current_user.login == 'admin@admin.ru':
        if request.method == 'POST':
            name = request.form['fullname']
            thing = request.form['thing']
            size = request.form['size']
            price = request.form['price']
            currently = request.form['currently']
            time = request.form['time']
            shop = request.form['shop']
            weght = request.form['weght']
            price_delivery = request.form['price_delivery']
            time_delivery = request.form['time_delivery']
            owner = Autorization.select().where(Autorization.full_name == name).get()
            Thing.create(owner=owner, name_thing=thing, size=size, price=price, currently=currently, time=time,
                         shop=shop, weght=weght, price_delivery=price_delivery, time_delivery=time_delivery)
            return redirect(url_for('things'))
    else:
        return '<h1>Вам сюда нельзя</h1>'

    list = []
    data = Autorization.select()
    for i in data:
        list.append(i.full_name)
    return render_template('thing_add.html', datas=list)


@app.route('/things')
@login_required
def things():
    if current_user.login == 'admin@admin.ru':
        data = Thing.select().order_by(Thing.time.desc())
        auto = []
        for i in data:
            rub = i.price * i.currently
            client = Autorization.select().where(Autorization.id == i.owner_id).get().full_name
            auto.append((i.id, client, i.name_thing, i.size, i.price, i.currently, rub, i.time, i.shop, i.weght,
                         i.price_delivery, i.time_delivery))

        return render_template('things.html', datas=auto)
    return '<h1>Вам сюда нельзя</h1>'


@app.route('/')
def index():
    return render_template('login.html')


@app.route('/logout')
def logout():
    logout_user()
    return render_template('login.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        user = Autorization.select().where(Autorization.login == request.form['login']).first()
        if user:
            if user.password == request.form['password']:
                login_user(user)
                if current_user.login != 'admin@admin.ru':
                    name = current_user.login
                    data = Thing.select().order_by(Thing.time.desc()).where(
                        Thing.owner == Autorization.select().where(Autorization.login == name).get())
                    list = []
                    for i in data:
                        rub = i.price * i.currently
                        list.append((i.name_thing, i.size, i.price, i.currently, rub, i.time, i.shop, i.weght,
                                     i.price_delivery, i.time_delivery))

                    return render_template('client_thing.html', name=name, datas=list)
                return redirect(url_for('client'))
        return '<h1>Введен не правильный логин или пароль</h1>'
    return render_template('login.html')


@app.route('/client')
@login_required
def client():
    if current_user.login == 'admin@admin.ru':
        data = Autorization.select().order_by(Autorization.time.desc())
        sum_balance = 0
        auto = []
        for i in data:
            for b in i.balances:
                sum_balance = sum_balance + b.balance

            auto.append((i.id, i.login, i.password, str(i.time), i.full_name, sum_balance))
            sum_balance = 0

        return render_template('client.html', datas=auto)
    return '<h1>Вам сюда нельзя</h1>'


@app.route('/edit/<id>')
@login_required
def get_edit(id):
    if current_user.login == 'admin@admin.ru':
        data = Autorization.select().where(Autorization.id == id).get()
        auto = []
        auto.append((data.id, data.login, data.password, str(data.time), data.full_name))
        data = auto[0]
        return render_template('edit.html', data=data)
    else:
        return '<h1>Вам сюда нельзя</h1>'


@app.route('/balance/<id>', methods=['POST', 'GET'])
@login_required
def balance_edit(id):
    if current_user.login == 'admin@admin.ru':
        if request.method == "POST":
            money = request.form['money']
            print(id)
            print(money)
            Balance.create(owner=Autorization.select().where(Autorization.id == id).get(), balance=money)
            return redirect(url_for('balance_edit', id=id))
        list = []
        balance_user = Balance.select().order_by(Balance.time.desc()).where(
            Balance.owner == Autorization.select().where(Autorization.id == id).get())
        for i in balance_user:
            list.append((i.balance, i.time, i.owner_id, i.id))
        return render_template('balance.html', datas=list)
    else:
        return '<h1>Вам сюда нельзя</h1>'


@app.route('/add_client', methods=['POST', 'GET'])
@login_required
def get_add():
    if current_user.login == 'admin@admin.ru':
        if request.method == 'POST':
            try:
                if request.form['password'] == request.form['password2']:
                    if request.form['fullName'] == '':
                        flash("Одно из полей не было заполнено")
                        return redirect(url_for('get_add'))
                    elif request.form['password'] == '':
                        flash("Одно из полей не было заполнено")
                        return redirect(url_for('get_add'))
                    elif request.form['login'] == '':
                        flash("Одно из полей не было заполнено")
                        return redirect(url_for('get_add'))
                    else:
                        fullname = request.form['fullName']
                        password = request.form['password']
                        login = request.form['login']

                        Autorization.create(login=login, full_name=fullname, password=password)
                        Balance.create(owner=Autorization.select().where(Autorization.login == login).get())

                        flash('Пользователь добавлен')
                        return redirect(url_for('client'))
                else:
                    flash('Введенные пароли не совпадают')
                    return redirect(url_for('get_add'))
            except:
                flash('Такой Login уже существует')
                return redirect(url_for('get_add'))

        return render_template('add_client.html')
    else:
        return '<h1>Вам сюда нельзя</h1>'


@app.route('/del/<id>')
@login_required
def get_del(id):
    if current_user.login == 'admin@admin.ru':
        Thing.delete().where(Thing.owner_id == id).execute()
        Balance.delete().where(Balance.owner_id == id).execute()
        Autorization.delete().where(Autorization.id == id).execute()

        flash('Пользователь удален')
        return redirect(url_for('client'))
    else:
        return '<h1>Вам сюда нельзя</h1>'


@app.route('/balance_del/<id>', methods=['POST', 'GET'])
@login_required
def balance_del(id):
    if current_user.login == 'admin@admin.ru':
        balance_id = request.values['balance_id']
        Balance.delete().where(Balance.id == id).execute()
        flash('Запись удаленна')
        return redirect(url_for('balance_edit', id=balance_id))
    else:
        return '<h1>Вам сюда нельзя</h1>'


@app.route('/thing_del/<id>')
@login_required
def thing_del(id):
    if current_user.login == 'admin@admin.ru':
        Thing.delete().where(Thing.id == id).execute()
        flash('Запись удаленна')
        return redirect(url_for('things'))
    else:
        return '<h1>Вам сюда нельзя</h1>'


@app.route('/update/<id>', methods=['POST'])
@login_required
def get_update(id):
    if current_user.login == 'admin@admin.ru':
        if request.method == 'POST':
            if request.form['fullName'] == '':

                flash("Одно из полей не было заполнено")
                return redirect(url_for('get_edit', id=id))
            elif request.form['password'] == '':

                flash("Одно из полей не было заполнено")
                return redirect(url_for('get_edit', id=id))
            else:
                fullname = request.form['fullName']
                password = request.form['password']
                id = id
                Autorization.update(password=password, full_name=fullname).where(Autorization.id == id).execute()
                flash('Запись изменена')
                return redirect(url_for('client'))
    else:
        return '<h1>Вам сюда нельзя</h1>'


if __name__ == '__main__':
    app.run()
