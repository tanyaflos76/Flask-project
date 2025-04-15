from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .abc import AbstractModel
from .reservation import ReservationModel

if TYPE_CHECKING:
    from .user import UserModel
    from .wish import WishModel


class WishListModel(AbstractModel):
    __tablename__ = "wish_lists"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column("user_id", ForeignKey("users.id"))
    title: Mapped[str | None]
    description: Mapped[str | None]
    is_public: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        index=True,
    )
    user: Mapped["UserModel"] = relationship("UserModel", back_populates="wish_lists")
    wishes: Mapped[list["WishModel"]] = relationship("WishModel", back_populates="wish_lists")
