from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ...deps import get_db, get_current_user
from ...repositories.reservations import ReservationsRepository
from ...repositories.copies import CopiesRepository
from ...models.book_copy import CopyStatus


router = APIRouter()


@router.get("/me")
def my_reservations(db: Session = Depends(get_db), current=Depends(get_current_user)):
    repo = ReservationsRepository(db)
    return repo.list_by_user(current.id)


@router.post("")
def reserve(book_id: int, db: Session = Depends(get_db), current=Depends(get_current_user)):
    # Only allow reservation when no available copies
    copies = CopiesRepository(db).list_by_book(book_id)
    if any(c.status == CopyStatus.available for c in copies):
        raise HTTPException(status_code=400, detail="book_has_available_copy")
    r = ReservationsRepository(db).create(book_id, current.id)
    return r


@router.post("/{reservation_id}/cancel")
def cancel(reservation_id: int, db: Session = Depends(get_db), current=Depends(get_current_user)):
    r = ReservationsRepository(db).cancel(reservation_id)
    if not r:
        raise HTTPException(status_code=404, detail="reservation_not_found")
    return r

