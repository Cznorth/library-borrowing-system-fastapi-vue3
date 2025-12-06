import json
import os
import urllib.parse
import urllib.request
from typing import Any, Dict, List, Optional


BASE_URL = "https://www.googleapis.com/books/v1/volumes"


def _http_get(url: str, timeout: int = 10) -> Dict[str, Any]:
    req = urllib.request.Request(url, headers={"User-Agent": "LibrarySystem/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = resp.read()
        return json.loads(data.decode("utf-8"))


def _pick_isbn(identifiers: List[Dict[str, Any]]) -> Optional[str]:
    if not identifiers:
        return None
    prefer = ["ISBN_13", "ISBN_10"]
    by_type = {i.get("type"): i.get("identifier") for i in identifiers}
    for t in prefer:
        v = by_type.get(t)
        if v:
            return v
    # fallback any
    return identifiers[0].get("identifier")


def _normalize_cover(url: Optional[str]) -> Optional[str]:
    if not url:
        return None
    # ensure https
    if url.startswith("http:"):
        url = "https:" + url[5:]
    return url


def _to_book_item(item: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    vi = item.get("volumeInfo") or {}
    title = vi.get("title")
    authors = vi.get("authors") or []
    if not title or not authors:
        return None
    identifiers = vi.get("industryIdentifiers") or []
    isbn = _pick_isbn(identifiers)
    cover_url = None
    images = vi.get("imageLinks") or {}
    if images:
        cover_url = _normalize_cover(images.get("thumbnail") or images.get("smallThumbnail"))
    publisher = vi.get("publisher")
    published = vi.get("publishedDate") or ""
    year = None
    if isinstance(published, str) and len(published) >= 4:
        try:
            year = int(published[:4])
        except Exception:
            year = None
    categories = vi.get("categories") or []
    category = categories[0][:100] if categories else None
    tags = ", ".join(categories[:8])[:255] if categories else None
    summary = vi.get("description")

    return {
        "isbn": isbn,
        "title": title,
        "author": ", ".join(authors)[:255],
        "publisher": publisher,
        "year": year,
        "category": category,
        "tags": tags,
        "summary": summary,
        "cover_url": cover_url,
    }


def search_books(keyword: str, limit: int = 20, lang: str = "zh") -> List[Dict[str, Any]]:
    params = {"q": keyword, "langRestrict": lang, "maxResults": max(1, min(limit, 40))}
    api_key = os.getenv("GOOGLE_BOOKS_API_KEY")
    if api_key:
        params["key"] = api_key
    url = f"{BASE_URL}?{urllib.parse.urlencode(params)}"
    payload = _http_get(url)
    items = payload.get("items") or []
    results: List[Dict[str, Any]] = []
    for it in items:
        book = _to_book_item(it)
        if book:
            results.append(book)
        if len(results) >= limit:
            break
    return results


def get_book_by_isbn(isbn: str, lang: str = "zh") -> Optional[Dict[str, Any]]:
    q = f"isbn:{isbn}"
    params = {"q": q, "langRestrict": lang}
    api_key = os.getenv("GOOGLE_BOOKS_API_KEY")
    if api_key:
        params["key"] = api_key
    url = f"{BASE_URL}?{urllib.parse.urlencode(params)}"
    payload = _http_get(url)
    items = payload.get("items") or []
    for it in items:
        book = _to_book_item(it)
        if book:
            return book
    return None

