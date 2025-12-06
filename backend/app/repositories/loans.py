from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from ..models.loan import Loan


class LoansRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, loan_id: int):
        return self.db.query(Loan).get(loan_id)

    def create(self, copy_id: int, user_id: int, due_days: int = 30):
        loan = Loan(copy_id=copy_id, user_id=user_id, loan_date=datetime.utcnow(), due_date=datetime.utcnow() + timedelta(days=due_days))
        self.db.add(loan)
        self.db.commit()
        self.db.refresh(loan)
        return loan

    def mark_return(self, loan: Loan):
        loan.return_date = datetime.utcnow()
        self.db.commit()
        self.db.refresh(loan)
        return loan

    def renew(self, loan: Loan, extend_days: int = 15):
        loan.due_date = loan.due_date + timedelta(days=extend_days)
        loan.renew_count += 1
        self.db.commit()
        self.db.refresh(loan)
        return loan

