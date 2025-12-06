from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
import json
from sqlalchemy.orm import Session
from ...deps import get_db, require_admin
from ...repositories.books import BooksRepository
from ...models.book import Book
from ...schemas.book import BookCreate
from ...services.openlibrary_provider import get_book_by_isbn, search_books


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
def create_book(data: BookCreate, db: Session = Depends(get_db)):
    repo = BooksRepository(db)
    b = repo.create(**data.model_dump())
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


@router.post("/import/by_isbn", dependencies=[Depends(require_admin)])
def import_by_isbn(payload: dict, db: Session = Depends(get_db)):
    isbn = payload.get("isbn")
    if not isbn:
        raise HTTPException(status_code=400, detail="isbn required")
    item = get_book_by_isbn(isbn)
    if not item:
        raise HTTPException(status_code=404, detail="Book not found from provider")
    repo = BooksRepository(db)
    result = repo.bulk_upsert([item])
    return result


@router.post("/import/by_keyword", dependencies=[Depends(require_admin)])
def import_by_keyword(payload: dict, db: Session = Depends(get_db)):
    keyword = payload.get("keyword")
    limit = payload.get("limit", 20)
    if not keyword:
        raise HTTPException(status_code=400, detail="keyword required")
    items = search_books(keyword=keyword, page=1, limit=int(limit))
    repo = BooksRepository(db)
    result = repo.bulk_upsert(items)
    return result


@router.post("/bulk", dependencies=[Depends(require_admin)])
async def import_bulk(file: UploadFile = File(None), items: list[BookCreate] | None = None, db: Session = Depends(get_db)):
    repo = BooksRepository(db)
    parsed: list[dict] = []
    if file is not None:
        content = await file.read()
        name = (file.filename or "").lower()
        if name.endswith(".csv"):
            import csv
            import io
            reader = csv.DictReader(io.StringIO(content.decode("utf-8")))
            for row in reader:
                parsed.append({k: v if v != "" else None for k, v in row.items()})
        else:
            payload = json.loads(content.decode("utf-8"))
            if isinstance(payload, list):
                parsed = payload
            else:
                raise HTTPException(status_code=400, detail="invalid bulk file content")
    elif items is not None:
        parsed = [i.model_dump() for i in items]
    else:
        raise HTTPException(status_code=400, detail="file or items required")
    result = repo.bulk_upsert(parsed)
    return result

