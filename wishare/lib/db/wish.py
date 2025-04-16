from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from wishare.lib.forms.wish import CreatingWishForm
from wishare.lib.models import WishModel


def create_wish(db: Session, form: CreatingWishForm, list_id: int) -> None:
    wish = WishModel(
        wish_list_id=list_id,
        name=form.name.data,
        description=form.description.data,
        link=form.link.data,
        price=form.price.data,
    )
    db.add(wish)
    db.flush()


def get_wishes(db: Session, list_id: int) -> Sequence[WishModel]:
    query = select(WishModel).where(WishModel.wish_list_id == list_id)
    wishes = db.execute(query).scalars().all()
    return wishes

def get_wish_by_wish_id(db: Session, wish_id: int) -> WishModel | None:
    wish = db.query(WishModel).filter(WishModel.id == wish_id).first()
    return wish