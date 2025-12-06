import sys
from pathlib import Path
from typing import List

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.core.db import SessionLocal
from app.repositories.books import BooksRepository
from app.repositories.copies import CopiesRepository
from app.models.book_copy import CopyStatus


def gen_barcode(book_id: int, idx: int) -> str:
    return f"BK{book_id:05d}-{idx:03d}"


def gen_location(book_id: int) -> str:
    area = chr(ord('A') + (book_id % 6))
    shelf = (book_id % 20) + 1
    return f"{area}-{shelf}"


def main():
    db = SessionLocal()
    try:
        books_repo = BooksRepository(db)
        copies_repo = CopiesRepository(db)
        result = books_repo.list(page=1, page_size=500)
        added = 0
        for b in result["items"]:
            existing = copies_repo.list_by_book(b.id)
            if existing:
                continue
            barcode = gen_barcode(b.id, 1)
            loc = gen_location(b.id)
            copy = copies_repo.create(book_id=b.id, barcode=barcode, shelf_location=loc)
            # ensure status available
            copies_repo.update(copy.id, status=CopyStatus.available)
            added += 1
            if added >= 40:
                break
        print({"added": added})
    finally:
        db.close()


if __name__ == "__main__":
    main()

