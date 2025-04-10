from flask import Flask, render_template, redirect
from data import db_session
from data.users import User
from forms.user import RegisterForm

application = Flask(__name__)

application.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


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


def main():
    db_session.global_init("db/wishare.db")
    application.run()


if __name__ == '__main__':
    main()
