import argparse
import csv
import io
import json
import sys
import urllib.request
from typing import Any, Dict, List, Optional

from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.core.config import settings
from app.core.db import SessionLocal
from app.repositories.books import BooksRepository
from app.repositories.copies import CopiesRepository
from app.models.book import Book
from app.models.book_copy import BookCopy
from app.services.googlebooks_provider import search_books as gb_search, get_book_by_isbn as gb_by_isbn
from app.services.openlibrary_provider import search_books as ol_search, get_book_by_isbn as ol_by_isbn, COVER_URL_TMPL


def http_head_ok(url: str, timeout: int = 3) -> bool:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "LibrarySystem/1.0"})
        req.get_method = lambda: "HEAD"
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            ct = resp.headers.get("Content-Type", "")
            return resp.status == 200 and ct.startswith("image/")
    except Exception:
        return False


def ensure_cover(item: Dict[str, Any]) -> Optional[str]:
    url = item.get("cover_url")
    isbn = item.get("isbn")
    if url and http_head_ok(url):
        return url
    # try openlibrary by isbn
    if isbn:
        ol_url = COVER_URL_TMPL.format(isbn=isbn)
        if http_head_ok(ol_url):
            return ol_url
    return None


def parse_file(path: str, fmt: str) -> List[Dict[str, Any]]:
    with open(path, "r", encoding="utf-8") as f:
        if fmt == "json":
            payload = json.load(f)
            if not isinstance(payload, list):
                raise ValueError("JSON must be an array of items")
            return payload
        elif fmt == "csv":
            reader = csv.DictReader(f)
            items: List[Dict[str, Any]] = []
            for row in reader:
                items.append({k: (v if v != "" else None) for k, v in row.items()})
            return items
        else:
            raise ValueError("Unsupported format")


def clean_item(x: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    title = x.get("title")
    author = x.get("author")
    if not title or not author:
        return None
    # normalize lengths
    x["title"] = str(title)[:255]
    x["author"] = str(author)[:255]
    if x.get("category"):
        x["category"] = str(x["category"])[:100]
    if x.get("tags"):
        x["tags"] = str(x["tags"])[:255]
    if x.get("isbn"):
        x["isbn"] = str(x["isbn"])[:20]
    # year
    year = x.get("year")
    if year is not None:
        try:
            y = int(year)
            if 1000 <= y <= 2100:
                x["year"] = y
            else:
                x["year"] = None
        except Exception:
            x["year"] = None
    return x


def run_import(args):
    items: List[Dict[str, Any]] = []
    if args.file:
        items = parse_file(args.file, args.format)
    else:
        source = args.source
        if args.keyword:
            if source == "googlebooks":
                items = gb_search(args.keyword, limit=args.limit, lang="zh")
            else:
                items = ol_search(args.keyword, page=1, limit=args.limit)
        if args.isbn:
            for code in args.isbn:
                if source == "googlebooks":
                    it = gb_by_isbn(code, lang="zh")
                else:
                    it = ol_by_isbn(code)
                if it:
                    items.append(it)

    prepared: List[Dict[str, Any]] = []
    for it in items:
        ci = clean_item(it or {})
        if not ci:
            continue
        if args.validate_images:
            cover = ensure_cover(ci)
            if not cover:
                continue
            ci["cover_url"] = cover
        prepared.append(ci)

    if args.dry_run:
        print(json.dumps({"count": len(prepared)}, ensure_ascii=False, indent=2))
        return

    db = SessionLocal()
    try:
        repo = BooksRepository(db)
        total_inserted = 0
        total_updated = 0
        total_skipped = 0
        errors: List[Dict[str, Any]] = []
        chunk = max(1, args.chunk_size)
        for i in range(0, len(prepared), chunk):
            batch = prepared[i:i+chunk]
            res = repo.bulk_upsert(batch)
            total_inserted += res["inserted"]
            total_updated += res["updated"]
            total_skipped += res["skipped"]
            errors.extend(res["errors"])
        print(json.dumps({
            "inserted": total_inserted,
            "updated": total_updated,
            "skipped": total_skipped,
            "errors": errors,
        }, ensure_ascii=False, indent=2))

        if args.add_copies and args.add_copies > 0:
            copies_repo = CopiesRepository(db)
            created_total = 0
            books = db.query(Book).all()
            for b in books:
                existing = db.query(BookCopy).filter(BookCopy.book_id == b.id).count()
                need = max(0, args.add_copies - existing)
                for i in range(need):
                    barcode = f"BC{b.id:06d}-{existing + i + 1:03d}"
                    copies_repo.create(book_id=b.id, barcode=barcode, shelf_location=None)
                    created_total += 1
            print(json.dumps({"copies_created": created_total}, ensure_ascii=False, indent=2))
    finally:
        db.close()


def main():
    parser = argparse.ArgumentParser(description="Seed initial books into database")
    parser.add_argument("--file", type=str, help="Path to JSON/CSV file")
    parser.add_argument("--format", type=str, default="json", choices=["json", "csv"], help="File format")
    parser.add_argument("--keyword", type=str, help="Keyword for provider search")
    parser.add_argument("--limit", type=int, default=20, help="Limit per provider request")
    parser.add_argument("--isbn", type=str, nargs="*", help="ISBN codes to import")
    parser.add_argument("--source", type=str, default="googlebooks", choices=["googlebooks", "openlibrary"], help="Data source")
    parser.add_argument("--validate-images", action="store_true", help="Validate cover image URLs")
    parser.add_argument("--chunk-size", type=int, default=100, help="Batch size for commit")
    parser.add_argument("--add-copies", type=int, default=0, help="Ensure each book has at least N copies")
    parser.add_argument("--dry-run", action="store_true", help="Do not write to DB, only preview counts")
    args = parser.parse_args()
    run_import(args)


if __name__ == "__main__":
    main()

