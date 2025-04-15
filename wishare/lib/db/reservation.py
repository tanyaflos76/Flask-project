from sqlalchemy.orm import Session

from wishare.lib.models.reservation import ReservationModel


def create_reservation(db: Session, user_id: int, wish_id: int, is_confirmed: bool) -> None:
    reservation = ReservationModel(
        wish_id=wish_id,
        user_id=user_id,
        is_confirmed=is_confirmed,
    )
    db.add(reservation)
    db.flush()
