import json
import urllib.parse
import urllib.request
from typing import Any, Dict, List, Optional


SEARCH_URL = "https://openlibrary.org/search.json"
COVER_URL_TMPL = "https://covers.openlibrary.org/b/isbn/{isbn}-L.jpg"


def _http_get(url: str, timeout: int = 10) -> Dict[str, Any]:
    req = urllib.request.Request(url, headers={"User-Agent": "LibrarySystem/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = resp.read()
        return json.loads(data.decode("utf-8"))


def _to_book_item(doc: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    isbns = doc.get("isbn") or []
    isbn = (isbns[0] if isinstance(isbns, list) and isbns else None)
    title = doc.get("title")
    authors = doc.get("author_name") or []
    publisher = None
    pubs = doc.get("publisher") or []
    if isinstance(pubs, list) and pubs:
        publisher = pubs[0]
    year = doc.get("first_publish_year")
    subjects = doc.get("subject") or []
    category = None
    tags = None
    if isinstance(subjects, list) and subjects:
        category = subjects[0][:100]
        tags = ", ".join(subjects[:8])[:255]
    cover_url = COVER_URL_TMPL.format(isbn=isbn) if isbn else None

    if not title or not authors:
        return None

    return {
        "isbn": isbn,
        "title": title,
        "author": ", ".join(authors)[:255],
        "publisher": publisher,
        "year": year,
        "category": category,
        "tags": tags,
        "summary": None,
        "cover_url": cover_url,
    }


def search_books(keyword: str, page: int = 1, limit: int = 20) -> List[Dict[str, Any]]:
    params = {"q": keyword, "page": page}
    url = f"{SEARCH_URL}?{urllib.parse.urlencode(params)}"
    payload = _http_get(url)
    docs = payload.get("docs") or []
    items: List[Dict[str, Any]] = []
    for doc in docs:
        item = _to_book_item(doc)
        if item:
            items.append(item)
        if len(items) >= limit:
            break
    return items


def get_book_by_isbn(isbn: str) -> Optional[Dict[str, Any]]:
    # 使用搜索接口按 ISBN 精确命中
    params = {"q": isbn}
    url = f"{SEARCH_URL}?{urllib.parse.urlencode(params)}"
    payload = _http_get(url)
    docs = payload.get("docs") or []
    for doc in docs:
        isbns = doc.get("isbn") or []
        if isinstance(isbns, list) and isbn in isbns:
            return _to_book_item(doc)
    return None
