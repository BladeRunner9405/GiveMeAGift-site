import os

from flask import Flask, render_template, url_for

from data import db_session
from data.pictures import Pictures
from data.wishes import Wishes

app = Flask(__name__)


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


if __name__ == '__main__':
    db_session.global_init("db/give_me_a_gift.db")
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
