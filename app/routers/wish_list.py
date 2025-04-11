from flask import Blueprint, redirect, render_template
from flask_login import current_user

from app.core.dependencies.flask import DatabaseDependency
from app.lib.forms import CreatingListForm
from app.lib.models import WishListModel


router = Blueprint("wish_list", __name__)


@router.route("/create-wishlist", methods=["GET", "POST"])
def create_wishlist(db: DatabaseDependency):
    form = CreatingListForm()
    if form.validate_on_submit():
        wishlist = WishListModel()
        wishlist.user_id = current_user.id
        wishlist.title = form.title.data
        wishlist.description = form.description.data
        wishlist.is_public = form.is_public.data
        db.add(wishlist)
        db.flush()
        return redirect("/profile")
    return render_template("create_wishlist.html", title="Добавление wish-листа", form=form)
