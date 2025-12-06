from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from ...deps import get_db, get_current_user
from ...services.loans import LoansService
from ...models.loan import Loan
from ...models.book_copy import BookCopy


router = APIRouter()


@router.get("/me")
def my_loans(db: Session = Depends(get_db), current=Depends(get_current_user)):
    return db.query(Loan).options(
        joinedload(Loan.copy).joinedload(BookCopy.book)
    ).filter(Loan.user_id == current.id, Loan.return_date == None).all()


@router.post("")
def borrow(copy_id: int, db: Session = Depends(get_db), current=Depends(get_current_user)):
    svc = LoansService(db)
    try:
        loan = svc.borrow(copy_id, current.id)
        return {"id": loan.id, "due_date": loan.due_date, "copy_id": loan.copy_id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{loan_id}/return")
def return_book(loan_id: int, db: Session = Depends(get_db), current=Depends(get_current_user)):
    svc = LoansService(db)
    try:
        loan = svc.return_book(loan_id)
        return {"id": loan.id, "return_date": loan.return_date}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{loan_id}/renew")
def renew(loan_id: int, db: Session = Depends(get_db), current=Depends(get_current_user)):
    svc = LoansService(db)
    try:
        loan = svc.renew(loan_id)
        return {"id": loan.id, "due_date": loan.due_date, "renew_count": loan.renew_count}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

