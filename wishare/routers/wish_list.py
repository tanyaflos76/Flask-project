from flask import Blueprint, redirect, render_template
from flask_login import current_user

from wishare.core.dependencies.flask import DatabaseDependency
from wishare.lib.db import wish as wish_db, wish_list as wish_list_db
from wishare.lib.forms import CreatingListForm


router = Blueprint("wish_list", __name__)


@router.route("/create-wishlist", methods=["GET", "POST"])
def create_wishlist(db: DatabaseDependency):
    form = CreatingListForm()
    if form.validate_on_submit():
        wish_list_db.create_wish_list(db, form, current_user.id)
        return redirect("/profile")
    return render_template("create_wishlist.html", title="Добавление wish-листа", form=form)


@router.route("/wishlist/<int:wishlist_id>")
def show_wishlist(db: DatabaseDependency, wishlist_id):
    wishes = wish_db.get_wishes(db, wishlist_id)
    wishlist = wish_list_db.get_wish_list_by_id(db, wishlist_id)
    return render_template("show_wishlist.html", wishlist=wishlist, wishes=wishes)
