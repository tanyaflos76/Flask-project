from flask import Blueprint, redirect, render_template
from flask_login import current_user, login_user

from app.core.dependencies.flask import DatabaseDependency
from app.lib.db import user as user_db, wish_list as wish_list_db
from app.lib.forms import LoginForm, RegisterForm


router = Blueprint("user", __name__)


@router.route("/register", methods=["GET", "POST"])
def reqister(db: DatabaseDependency):
    form = RegisterForm()
    kwargs = {"title": "Регистрация", "form": form}
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template(
                "register.html",
                **kwargs,
                message="Пароли не совпадают",
            )
        if user_db.get_user_by_email(db, form.email.data):
            return render_template(
                "register.html",
                **kwargs,
                message="Такой пользователь уже есть",
            )
        user_db.create_user(db, form)
        return redirect("/login")
    return render_template("register.html", **kwargs)


@router.route("/login", methods=["GET", "POST"])
def login(db: DatabaseDependency):
    form = LoginForm()
    if form.validate_on_submit():
        user = user_db.get_user_by_email(db, form.email.data)
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template("login.html", message="Неправильный логин или пароль", form=form)
    return render_template("login.html", title="Авторизация", form=form)


@router.route("/profile", methods=["GET", "POST"])
def profile(db: DatabaseDependency):
    wishlists = wish_list_db.get_wish_lists(db, current_user.id)
    return render_template("profile.html", wishlists=wishlists)
