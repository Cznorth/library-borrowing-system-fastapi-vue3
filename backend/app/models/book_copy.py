from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum
from ..core.db import Base


class CopyStatus(enum.Enum):
    available = "available"
    loaned = "loaned"
    retired = "retired"


class BookCopy(Base):
    __tablename__ = "book_copies"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False, index=True)
    barcode = Column(String(64), unique=True, nullable=False)
    shelf_location = Column(String(64))
    status = Column(Enum(CopyStatus), default=CopyStatus.available, nullable=False)

    book = relationship("Book")

