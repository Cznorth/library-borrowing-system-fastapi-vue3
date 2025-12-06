from sqlalchemy import Column, Integer, ForeignKey, DateTime, Enum
from datetime import datetime
import enum
from ..core.db import Base


class ReservationStatus(enum.Enum):
    queued = "queued"
    notified = "notified"
    expired = "expired"
    canceled = "canceled"


class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    status = Column(Enum(ReservationStatus), default=ReservationStatus.queued, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

