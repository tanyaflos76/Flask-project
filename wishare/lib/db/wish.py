from pathlib import Path
from typing import Sequence
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from wishare.lib.forms.wish import CreatingWishForm
from wishare.lib.models import WishModel


UPLOADS_DIR = Path(__name__).resolve().parent / "uploads"


def get_unique_filename(filename: str):
    ext = filename.rsplit(".", 1)[1].lower()
    return f"{uuid4().hex}.{ext}"


def save_uploaded_file(file: FileStorage) -> str:
    filename = secure_filename(file.filename)
    unique_filename = get_unique_filename(filename)
    file_path = UPLOADS_DIR / unique_filename
    file.save(file_path)
    return unique_filename


def create_wish(db: Session, form: CreatingWishForm, list_id: int) -> None:
    image_filename = None
    if form.image.data:
        image_filename = save_uploaded_file(form.image.data)

    wish = WishModel(
        wish_list_id=list_id,
        name=form.name.data,
        image_name=image_filename,
        link=form.link.data,
        description=form.description.data,
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
