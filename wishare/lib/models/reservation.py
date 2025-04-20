from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .abc import AbstractModel


if TYPE_CHECKING:
    from .user import UserModel
    from .wish import WishModel


class ReservationModel(AbstractModel):
    __tablename__ = "reservations"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    wish_id: Mapped[int] = mapped_column("wish_id", ForeignKey("wishes.id"))
    user_id: Mapped[int] = mapped_column("user_id", ForeignKey("users.id"))
    is_confirmed: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        index=True,
    )
    wishes: Mapped["WishModel"] = relationship("WishModel", back_populates="reservations")
    user: Mapped["UserModel"] = relationship("UserModel", back_populates="reservations")
