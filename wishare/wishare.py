from flask import Flask, render_template, redirect
from data import db_session
from data.users import User
from forms.user import RegisterForm, LoginForm
from flask_login import LoginManager, login_user, current_user

from forms.wishlists import CreatingListForm
from data.wish_lists import Wish_list

application = Flask(__name__)

application.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(application)


@application.route('/')
@application.route('/index')
def index():
    return render_template("start_window.html")


@application.route('/register', methods=['GET', 'POST'])
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
            username=form.name.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@application.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html', message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@application.route('/profile', methods=['GET', 'POST'])
def profile():
    db_sess = db_session.create_session()
    wishlists = db_sess.query(Wish_list).filter(Wish_list.is_public == True)
    return render_template("profile.html", wishlists=wishlists)


@application.route('/create-wishlist', methods=['GET', 'POST'])
def create_wishlist():
    form = CreatingListForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        wishlists = Wish_list()
        wishlists.title = form.title.data
        wishlists.description = form.description.data
        wishlists.is_public = form.is_public.data
        current_user.wish_lists.append(wishlists)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/profile')
    return render_template('create_wishlist.html', title='Добавление wish-листа',
                           form=form)


def main():
    db_session.global_init("db/wishare.db")
    application.run()


if __name__ == '__main__':
    main()
