import os

from flask import Flask, render_template, url_for

app = Flask(__name__)


@app.route('/')
def start():
    return render_template('base.html')

@app.route('/info')
def index():
    text = '''Очень часто люди долго думают над тем, что подарить другому человеку на какой-то праздник. Но бывает, 
    они не угадывают с подарками, и мы придумали решение – сайт GiveMeAGift, в котором вы можете указывать желаемые  
    вещи, а ваши друзья точно угадают с подарком!'''
    img_url = url_for('static', filename='img/present.svg')
    print(img_url)
    return render_template('info.html', img_url=img_url, text=text)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)