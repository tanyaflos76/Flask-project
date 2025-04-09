from flask import Flask, render_template

application = Flask(__name__)

application.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@application.route('/')
@application.route('/index')
def index():
    return render_template("start_window.html")


if __name__ == '__main__':
    application.run(port=8080, host='127.0.0.1')
