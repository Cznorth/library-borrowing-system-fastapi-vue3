from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ...deps import get_db, require_admin
from ...repositories.copies import CopiesRepository


router = APIRouter()


@router.get("/by-book/{book_id}")
def list_by_book(book_id: int, db: Session = Depends(get_db)):
    repo = CopiesRepository(db)
    return repo.list_by_book(book_id)


@router.post("", dependencies=[Depends(require_admin)])
def create_copy(data: dict, db: Session = Depends(get_db)):
    repo = CopiesRepository(db)
    copy = repo.create(book_id=data["book_id"], barcode=data["barcode"], shelf_location=data.get("shelf_location"))
    return copy


@router.patch("/{copy_id}", dependencies=[Depends(require_admin)])
def update_copy(copy_id: int, data: dict, db: Session = Depends(get_db)):
    repo = CopiesRepository(db)
    copy = repo.update(copy_id, **data)
    if not copy:
        raise HTTPException(status_code=404, detail="Copy not found")
    return copy


@router.delete("/{copy_id}", dependencies=[Depends(require_admin)])
def delete_copy(copy_id: int, db: Session = Depends(get_db)):
    repo = CopiesRepository(db)
    ok = repo.delete(copy_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Copy not found")
    return {"ok": True}

