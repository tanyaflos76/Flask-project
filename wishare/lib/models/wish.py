from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, Numeric, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .abc import AbstractModel


if TYPE_CHECKING:
    from .reservation import ReservationModel
    from .wish_list import WishListModel


class WishModel(AbstractModel):
    __tablename__ = "wishes"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    wish_list_id: Mapped[int] = mapped_column("wish_list_id", ForeignKey("wish_lists.id"))
    name: Mapped[str | None]
    description: Mapped[str | None]
    image_name: Mapped[str | None]
    price: Mapped[float | None] = mapped_column(Numeric(10, 2))
    is_taken: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default="false")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        index=True,
    )
    wish_lists: Mapped["WishListModel"] = relationship("WishListModel", back_populates="wishes")
    reservations: Mapped[list["ReservationModel"]] = relationship("ReservationModel", back_populates="wishes")
