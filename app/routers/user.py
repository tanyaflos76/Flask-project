from flask import Blueprint, redirect, render_template
from flask_login import login_user

from app.core.dependencies.flask import DatabaseDependency
from app.lib.forms import LoginForm, RegisterForm
from app.lib.models import UserModel, WishListModel


router = Blueprint("user", __name__)


@router.route("/register", methods=["GET", "POST"])
def reqister(db: DatabaseDependency):
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template(
                "register.html",
                title="Регистрация",
                form=form,
                message="Пароли не совпадают",
            )
        if db.query(UserModel).filter(UserModel.email == form.email.data).first():
            return render_template(
                "register.html",
                title="Регистрация",
                form=form,
                message="Такой пользователь уже есть",
            )
        user = UserModel(
            username=form.name.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db.add(user)
        db.commit()
        return redirect("/login")
    return render_template("register.html", title="Регистрация", form=form)


@router.route("/login", methods=["GET", "POST"])
def login(db: DatabaseDependency):
    form = LoginForm()
    if form.validate_on_submit():
        user = db.query(UserModel).filter(UserModel.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template("login.html", message="Неправильный логин или пароль", form=form)
    return render_template("login.html", title="Авторизация", form=form)


@router.route("/profile", methods=["GET", "POST"])
def profile(db: DatabaseDependency):
    wishlists = db.query(WishListModel).filter(WishListModel.is_public == True)
    return render_template("profile.html", wishlists=wishlists)
