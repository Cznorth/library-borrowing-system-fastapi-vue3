from sqlalchemy import Column, Integer, String, Text
from ..core.db import Base


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    isbn = Column(String(20), unique=True, index=True)
    title = Column(String(255), index=True, nullable=False)
    author = Column(String(255), index=True, nullable=False)
    publisher = Column(String(255))
    year = Column(Integer)
    category = Column(String(100))
    tags = Column(String(255))
    summary = Column(Text)
    cover_url = Column(String(255))

