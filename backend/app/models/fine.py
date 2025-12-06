from sqlalchemy import Column, Integer, ForeignKey, DateTime, Numeric, Enum
from datetime import datetime
import enum
from ..core.db import Base


class FineStatus(enum.Enum):
    unpaid = "unpaid"
    paid = "paid"


class Fine(Base):
    __tablename__ = "fines"

    id = Column(Integer, primary_key=True, index=True)
    loan_id = Column(Integer, ForeignKey("loans.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    amount = Column(Numeric(10, 2), nullable=False)
    status = Column(Enum(FineStatus), default=FineStatus.unpaid, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    paid_at = Column(DateTime, nullable=True)

