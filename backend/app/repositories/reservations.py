from sqlalchemy.orm import Session
from ..models.reservation import Reservation, ReservationStatus


class ReservationsRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, book_id: int, user_id: int):
        r = Reservation(book_id=book_id, user_id=user_id)
        self.db.add(r)
        self.db.commit()
        self.db.refresh(r)
        return r

    def list_by_user(self, user_id: int):
        return self.db.query(Reservation).filter(Reservation.user_id == user_id).all()

    def cancel(self, reservation_id: int):
        r = self.db.query(Reservation).get(reservation_id)
        if not r:
            return None
        r.status = ReservationStatus.canceled
        self.db.commit()
        self.db.refresh(r)
        return r

