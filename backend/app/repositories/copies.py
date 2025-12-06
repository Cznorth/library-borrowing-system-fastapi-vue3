from sqlalchemy.orm import Session
from ..models.book_copy import BookCopy


class CopiesRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_by_book(self, book_id: int):
        return self.db.query(BookCopy).filter(BookCopy.book_id == book_id).all()

    def get(self, copy_id: int):
        return self.db.query(BookCopy).get(copy_id)

    def create(self, book_id: int, barcode: str, shelf_location: str | None = None):
        copy = BookCopy(book_id=book_id, barcode=barcode, shelf_location=shelf_location)
        self.db.add(copy)
        self.db.commit()
        self.db.refresh(copy)
        return copy

    def update(self, copy_id: int, **data):
        copy = self.get(copy_id)
        if not copy:
            return None
        for k, v in data.items():
            setattr(copy, k, v)
        self.db.commit()
        self.db.refresh(copy)
        return copy

    def delete(self, copy_id: int):
        copy = self.get(copy_id)
        if not copy:
            return False
        self.db.delete(copy)
        self.db.commit()
        return True

