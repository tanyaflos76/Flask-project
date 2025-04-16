from flask import Blueprint, redirect, render_template, request, jsonify
from flask_login import current_user

from wishare.core.dependencies.flask import DatabaseDependency
from wishare.lib.db import wish as wish_db, wish_list as wish_list_db, reservation as reservation_db
from wishare.lib.forms import CreatingListForm
from wishare.lib.forms.wish import CreatingWishForm

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


@router.route("/create-wish/<int:wishlist_id>", methods=["GET", "POST"])
def create_wish(db: DatabaseDependency, wishlist_id):
    form = CreatingWishForm()
    if form.validate_on_submit():
        wish_db.create_wish(db, form, wishlist_id)
        return redirect(f"/wishlist/{wishlist_id}")
    return render_template("create_wish.html", title="Добавление wish-а", form=form)


@router.route('/reserve_multiple', methods=["GET", "POST"])
def reserve_multiple(db: DatabaseDependency):
    data = request.get_json()
    wish_ids = data.get('wishes', [])
    wishlist = wish_list_db.get_wish_list_by_wish_id(db, wish_ids[0])
    for wish_id in wish_ids:
        user_id = wish_list_db.get_user_id_by_wish_id(db, wish_id)
        reservation_db.create_reservation(db, user_id, wish_id, True)
        wish = wish_db.get_wish_by_wish_id(db, wish_id)
        wish.is_taken = True
    return redirect(f"/wishlist/{wishlist.id}")
