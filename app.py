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
                return redirect(url_for('client'))
        return '<h1>Введен не правильный логин или пароль</h1>'
    return render_template('login.html')


@app.route('/client')
@login_required
def client():
    if current_user.login == 'admin@admin.ru':
        data = Autorization.select().order_by(Autorization.time.desc())
        auto = []
        for i in data:
            auto.append((i.id, i.login, i.password, str(i.time), i.full_name, i.balance))
        return render_template('client.html', datas=auto)
    return '<h1>Вам сюда нельзя</h1>'


@app.route('/edit/<id>')
@login_required
def get_edit(id):
    data = Autorization.select().where(Autorization.id == id).get()
    auto = []
    auto.append((data.id, data.login, data.password, str(data.time), data.full_name))
    data = auto[0]
    return render_template('edit.html', data=data)


@app.route('/balance/<id>', methods=['POST', 'GET'])
@login_required
def balance_edit(id):
    if request.method == 'POST':
        if request.form['balance'] == '':
            return redirect(url_for('client'))

        else:
            try:
                balance = request.form['balance']
                Autorization.update(balance=balance).where(Autorization.id == id).execute()
                flash('Баланс изменен')
                return redirect(url_for('client'))
            except:
                flash('БАЛАНС НЕ ИЗМЕНИЛСЯ')
                return redirect(url_for('client'))

    data = Autorization.select().where(Autorization.id == id).get()
    auto = []
    auto.append((data.id, data.full_name, data.balance))
    data = auto[0]

    return render_template('balance.html', data=data)


@app.route('/add_client', methods=['POST', 'GET'])
@login_required
def get_add():
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

                    Autorization.create(login=login, password=password, full_name=fullname)

                    flash('Пользователь добавлен')
                    return redirect(url_for('client'))
            else:
                flash('Введенные пароли не совпадают')
                return redirect(url_for('get_add'))
        except:
            flash('Такой Login уже существует')
            return redirect(url_for('get_add'))

    return render_template('add_client.html')


@app.route('/del/<id>')
@login_required
def get_del(id):
    Autorization.delete().where(Autorization.id == id).execute()
    flash('Пользователь удален')
    return redirect(url_for('client'))


@app.route('/update/<id>', methods=['POST'])
@login_required
def get_update(id):
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


if __name__ == '__main__':
    app.run()
