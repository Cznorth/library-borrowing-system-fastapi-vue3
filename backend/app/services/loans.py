from datetime import datetime
from sqlalchemy.orm import Session
from ..models.book_copy import BookCopy, CopyStatus
from ..models.loan import Loan
from ..models.fine import Fine
from ..repositories.loans import LoansRepository
from ..repositories.copies import CopiesRepository
from ..repositories.fines import FinesRepository


MAX_BORROW = 5
INITIAL_DUE_DAYS = 30
RENEW_TIMES_MAX = 1
RENEW_EXTEND_DAYS = 15
FINE_PER_DAY = 0.5


class LoansService:
    def __init__(self, db: Session):
        self.db = db
        self.loans = LoansRepository(db)
        self.copies = CopiesRepository(db)
        self.fines = FinesRepository(db)

    def current_loans_count(self, user_id: int) -> int:
        return self.db.query(Loan).filter(Loan.user_id == user_id, Loan.return_date == None).count()

    def borrow(self, copy_id: int, user_id: int):
        if self.current_loans_count(user_id) >= MAX_BORROW:
            raise ValueError("borrow_limit_reached")
        copy = self.copies.get(copy_id)
        if not copy or copy.status != CopyStatus.available:
            raise ValueError("copy_not_available")
        loan = self.loans.create(copy_id, user_id, INITIAL_DUE_DAYS)
        copy.status = CopyStatus.loaned
        self.db.commit()
        return loan

    def return_book(self, loan_id: int):
        loan = self.loans.get(loan_id)
        if not loan or loan.return_date is not None:
            raise ValueError("invalid_loan")
        loan = self.loans.mark_return(loan)
        copy = self.copies.get(loan.copy_id)
        copy.status = CopyStatus.available
        self.db.commit()
        if loan.due_date < loan.return_date:
            days = (loan.return_date - loan.due_date).days
            amount = round(days * FINE_PER_DAY, 2)
            self.fines.create(loan_id=loan.id, user_id=loan.user_id, amount=amount)
        return loan

    def renew(self, loan_id: int):
        loan = self.loans.get(loan_id)
        if not loan or loan.return_date is not None:
            raise ValueError("invalid_loan")
        if loan.due_date < datetime.utcnow():
            raise ValueError("overdue_cannot_renew")
        if loan.renew_count >= RENEW_TIMES_MAX:
            raise ValueError("renew_limit_reached")
        return self.loans.renew(loan, RENEW_EXTEND_DAYS)

