import os

from flask import Flask, render_template, url_for
from flask_login import LoginManager, login_user, login_required, logout_user
from werkzeug.utils import redirect

from data import db_session
from data.pictures import Pictures
from data.users import User
from data.wishes import Wishes
from forms.user import RegisterForm, LoginForm

app = Flask(__name__)

app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/')
def start():
    db_sess = db_session.create_session()
    # if current_user.is_authenticated:
    #     news = db_sess.query(News).filter(
    #         (News.user == current_user) | (News.is_private != True))
    # else:
    #     news = db_sess.query(News).filter(News.is_private != True)
    wishes = db_sess.query(Wishes)
    pictures = db_sess.query(Pictures)
    return render_template("index.html", wishes=wishes, pictures=pictures)


@app.route('/index')
def index():
    db_sess = db_session.create_session()
    # if current_user.is_authenticated:
    #     news = db_sess.query(News).filter(
    #         (News.user == current_user) | (News.is_private != True))
    # else:
    #     news = db_sess.query(News).filter(News.is_private != True)
    wishes = db_sess.query(Wishes)
    pictures = db_sess.query(Pictures)
    return render_template("index.html", wishes=wishes, pictures=pictures)


@app.route('/info')
def info():
    text = '''Очень часто люди долго думают над тем, что подарить другому человеку на какой-то праздник. Но бывает, 
    они не угадывают с подарками, и мы придумали решение – сайт GiveMeAGift, в котором вы можете указывать желаемые  
    вещи, а ваши друзья точно угадают с подарком!'''
    img_url = url_for('static', filename='img/present.svg')
    print(img_url)
    return render_template('info.html', img_url=img_url, text=text)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            age=form.age.data,
            email=form.email.data,
            about=form.about.data,
            picture=form.picture.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


if __name__ == '__main__':
    db_session.global_init("db/give_me_a_gift.db")
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
