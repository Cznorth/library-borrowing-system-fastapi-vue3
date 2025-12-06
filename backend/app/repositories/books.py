from sqlalchemy.orm import Session
from typing import List
from ..models.book import Book


class BooksRepository:
    def __init__(self, db: Session):
        self.db = db

    def list(self, q: str | None = None, page: int = 1, page_size: int = 10):
        query = self.db.query(Book)
        if q:
            like = f"%{q}%"
            query = query.filter((Book.title.ilike(like)) | (Book.author.ilike(like)))
        total = query.count()
        items = query.offset((page - 1) * page_size).limit(page_size).all()
        return {"total": total, "items": items}

    def get(self, book_id: int):
        return self.db.query(Book).get(book_id)

    def create(self, **data):
        book = Book(**data)
        self.db.add(book)
        self.db.commit()
        self.db.refresh(book)
        return book

    def update(self, book_id: int, **data):
        book = self.get(book_id)
        if not book:
            return None
        for k, v in data.items():
            setattr(book, k, v)
        self.db.commit()
        self.db.refresh(book)
        return book

    def delete(self, book_id: int):
        book = self.get(book_id)
        if not book:
            return False
        self.db.delete(book)
        self.db.commit()
        return True

    def get_by_isbn(self, isbn: str):
        return self.db.query(Book).filter(Book.isbn == isbn).first()

    def bulk_upsert(self, items: List[dict]):
        inserted = 0
        updated = 0
        skipped = 0
        errors: list[dict] = []
        for idx, data in enumerate(items, start=1):
            try:
                title = data.get("title")
                author = data.get("author")
                if not title or not author:
                    skipped += 1
                    continue
                isbn = data.get("isbn")
                if isbn:
                    existing = self.get_by_isbn(isbn)
                else:
                    existing = None
                if existing:
                    for k, v in data.items():
                        setattr(existing, k, v)
                    updated += 1
                else:
                    book = Book(**data)
                    self.db.add(book)
                    inserted += 1
            except Exception as e:
                errors.append({"index": idx, "error": str(e)})
        self.db.commit()
        return {"inserted": inserted, "updated": updated, "skipped": skipped, "errors": errors}

