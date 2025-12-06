from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ...deps import get_db, get_current_user
from ...repositories.fines import FinesRepository


router = APIRouter()


@router.get("/me")
def my_fines(db: Session = Depends(get_db), current=Depends(get_current_user)):
    repo = FinesRepository(db)
    return repo.list_by_user(current.id)


@router.post("/{fine_id}/pay")
def pay(fine_id: int, db: Session = Depends(get_db), current=Depends(get_current_user)):
    repo = FinesRepository(db)
    fine = repo.mark_paid(fine_id)
    if not fine:
        raise HTTPException(status_code=404, detail="fine_not_found")
    return fine

