from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from wishare.lib.forms.wishlists import CreatingListForm
from wishare.lib.models.wish_list import WishListModel


def create_wish_list(db: Session, form: CreatingListForm, user_id: int) -> None:
    wishlist = WishListModel(
        user_id=user_id,
        title=form.title.data,
        description=form.description.data,
        is_public=form.is_public.data,
    )
    db.add(wishlist)
    db.flush()


def get_wish_lists(db: Session, user_id: int) -> Sequence[WishListModel]:
    query = select(WishListModel).where(WishListModel.user_id == user_id)
    wishlists = (db.execute(query)).scalars().all()
    return wishlists


def get_wish_list_by_id(db: Session, list_id: int) -> WishListModel | None:
    query = select(WishListModel).where(WishListModel.id == list_id)
    result = db.execute(query).scalar()
    return result



