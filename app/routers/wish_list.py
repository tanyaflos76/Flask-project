from flask import Blueprint, redirect, render_template
from flask_login import current_user

from app.core.dependencies.flask import DatabaseDependency
from app.lib.db import wish_list as wish_list_db
from app.lib.forms import CreatingListForm


router = Blueprint("wish_list", __name__)


@router.route("/create-wishlist", methods=["GET", "POST"])
def create_wishlist(db: DatabaseDependency):
    form = CreatingListForm()
    if form.validate_on_submit():
        wish_list_db.create_wish_list(db, form, current_user.id)
        return redirect("/profile")
    return render_template("create_wishlist.html", title="Добавление wish-листа", form=form)
