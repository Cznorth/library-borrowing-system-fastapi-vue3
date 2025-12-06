from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ...deps import get_db
from ...repositories.books import BooksRepository
from ...models.book import Book


router = APIRouter()


@router.get("")
def list_books(q: str | None = None, page: int = 1, page_size: int = 10, db: Session = Depends(get_db)):
    repo = BooksRepository(db)
    result = repo.list(q=q, page=page, page_size=page_size)
    return {"total": result["total"], "items": [
        {
            "id": b.id,
            "isbn": b.isbn,
            "title": b.title,
            "author": b.author,
            "publisher": b.publisher,
            "year": b.year,
            "category": b.category,
            "tags": b.tags,
            "summary": b.summary,
            "cover_url": b.cover_url,
        } for b in result["items"]
    ]}


@router.get("/{book_id}")
def get_book(book_id: int, db: Session = Depends(get_db)):
    repo = BooksRepository(db)
    b: Book | None = repo.get(book_id)
    if not b:
        raise HTTPException(status_code=404, detail="Book not found")
    return b


@router.post("")
def create_book(data: dict, db: Session = Depends(get_db)):
    repo = BooksRepository(db)
    b = repo.create(**data)
    return b


@router.patch("/{book_id}")
def update_book(book_id: int, data: dict, db: Session = Depends(get_db)):
    repo = BooksRepository(db)
    b = repo.update(book_id, **data)
    if not b:
        raise HTTPException(status_code=404, detail="Book not found")
    return b


@router.delete("/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    repo = BooksRepository(db)
    ok = repo.delete(book_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"ok": True}

