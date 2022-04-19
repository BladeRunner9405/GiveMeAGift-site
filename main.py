import os
import sqlite3

from flask import Flask, render_template, url_for, abort, make_response, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_restful import Api
from werkzeug.utils import redirect, secure_filename

from data import db_session, wishes_api, wishes_resources
from data.pictures import Pictures
from data.users import User
from data.wishes import Wishes
from forms.user import RegisterForm, LoginForm
from forms.wish import WishForm

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

# для списка объектов
api.add_resource(wishes_resources.WishesListResource, '/api/v2/wishes')

# для одного объекта
api.add_resource(wishes_resources.WishesResource, '/api/v2/wishes/<int:wishes_id>')

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
    return render_template("index.html", wishes=wishes)


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
def register():
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
        )
        user.set_password(form.password.data)
        import os.path
        path = os.path.join('static', 'img')
        num_files = len([_ for _ in os.listdir(path)
                         if os.path.isfile(os.path.join(path, _))])
        f = form.picture.data
        filename = secure_filename(f.filename)
        way = os.path.join(
            'static', 'img', str(num_files + 1) + "avatar"
        )
        f.save(way)
        user.picture = f'../static/img/{num_files + 1}avatar'
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')

    return render_template('register.html', title='Регистрация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/add_wish', methods=['GET', 'POST'])
def add_wish():
    form = WishForm()
    if form.validate_on_submit():
        import os.path
        path = os.path.join('static', 'img')
        num_files = len([f for f in os.listdir(path)
                         if os.path.isfile(os.path.join(path, f))])
        db_sess = db_session.create_session()
        wish = Wishes()
        wish.title = form.title.data
        wish.description = form.content.data
        f = form.main_picture.data
        print(f)
        filename = secure_filename(f.filename)
        way = os.path.join(
            'static', 'img', str(num_files + 1)
        )
        f.save(way)
        wish.main_picture = f'../static/img/{num_files + 1}'
        # wish.is_private = form.is_private.data
        current_user.wishes.append(wish)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('add_wish.html', form=form)


@app.route('/news_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def news_delete(id):
    db_sess = db_session.create_session()
    wish = db_sess.query(Wishes).filter(Wishes.id == id,
                                        Wishes.user_id == current_user.id
                                        ).first()
    if wish:
        db_sess.delete(wish)
        db_sess.commit()
    else:
        abort(404)
    return redirect(f'/profile/{current_user.id}')


@app.route('/profile/<int:id>', methods=['GET', 'POST'])
def profile(id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == id).first()
    wishes = db_sess.query(Wishes).filter(Wishes.user_id == id)
    return render_template('profile.html', user=user, wishes=wishes)


@app.route('/book_wish/<int:id>', methods=['GET', 'POST'])
def book_wish(id):
    database = 'db/give_me_a_gift.db'
    con = sqlite3.connect(database)
    cur = con.cursor()
    answer = cur.execute(f'SELECT booked FROM users WHERE id == {current_user.id}').fetchall()[0][0]
    if type(answer) != int:
        answer = answer.split()
    else:
        answer = [str(answer)]
    if str(id) not in answer:
        answer.append(str(id))
        answer = ' '.join(answer)
        command1 = f"UPDATE users SET booked = '{answer}' WHERE id = {current_user.id}"
        command2 = f"UPDATE wishes SET is_booked = 1 WHERE id = {id}"

        cur.execute(command1).fetchall()
        cur.execute(command2).fetchall()
        con.commit()
    con.close()
    return redirect(f'/booked_wishes')


@app.route('/wish_is_ready/<int:id>', methods=['GET', 'POST'])
def wish_is_ready(id):
    database = 'db/give_me_a_gift.db'
    con = sqlite3.connect(database)
    cur = con.cursor()

    answer = cur.execute(f'SELECT booked FROM users WHERE id == {current_user.id}').fetchall()[0][0]
    if type(answer) != int:
        answer = answer.split()
    else:
        answer = [str(answer)]
    if str(id) in answer:
        del answer[answer.index(str(id))]
        answer = ' '.join(answer)
        command1 = f"UPDATE users SET booked = '{answer}' WHERE id = {current_user.id}"
        cur.execute(command1).fetchall()
    command = f"DELETE FROM wishes WHERE id = {id}"
    cur.execute(command).fetchall()
    con.commit()
    con.close()
    return redirect(f'/booked_wishes')


@app.route('/unbook_wish/<int:id>', methods=['GET', 'POST'])
def unbook_wish(id):
    database = 'db/give_me_a_gift.db'
    con = sqlite3.connect(database)
    cur = con.cursor()
    answer = cur.execute(f'SELECT booked FROM users WHERE id == {current_user.id}').fetchall()[0][0]
    if type(answer) != int:
        answer = answer.split()
    else:
        answer = [str(answer)]
    if str(id) in answer:
        del answer[answer.index(str(id))]
        answer = ' '.join(answer)
        command1 = f"UPDATE users SET booked = '{answer}' WHERE id = {current_user.id}"
        command2 = f"UPDATE wishes SET is_booked = 0 WHERE id = {id}"
        cur.execute(command1).fetchall()
        cur.execute(command2).fetchall()
        con.commit()
    con.close()
    return redirect(f'/booked_wishes')


@app.route('/booked_wishes', methods=['GET', 'POST'])
def booked_wishes():
    db_sess = db_session.create_session()
    database = 'db/give_me_a_gift.db'
    con = sqlite3.connect(database)
    cur = con.cursor()
    answer = cur.execute(f'SELECT booked FROM users WHERE id == {current_user.id}').fetchall()[0][0]
    if type(answer) != int:
        answer = list(map(int, answer.split()))
    else:
        answer = [int(answer)]
    wishes = db_sess.query(Wishes)
    pictures = db_sess.query(Pictures)
    return render_template("booked_wishes.html", wishes=wishes, pictures=pictures, booked=answer)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    db_session.global_init("db/give_me_a_gift.db")
    app.register_blueprint(wishes_api.blueprint)
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
