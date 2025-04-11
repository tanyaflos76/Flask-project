from flask import Blueprint, redirect, render_template
from flask_login import current_user

from app.core.dependencies.flask import DatabaseDependency
from app.lib.forms import CreatingListForm
from app.lib.models import WishListModel


router = Blueprint("wish_list", __name__)


@router.route("/create", methods=["GET", "POST"])
def create_wishlist(db: DatabaseDependency):
    form = CreatingListForm()
    if form.validate_on_submit():
        wishlists = WishListModel()
        wishlists.title = form.title.data
        wishlists.description = form.description.data
        wishlists.is_public = form.is_public.data
        current_user.wish_lists.append(wishlists)
        db.merge(current_user)
        db.commit()
        return redirect("/profile")
    return render_template("create_wishlist.html", title="Добавление wish-листа", form=form)
