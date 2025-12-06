from sqlalchemy.orm import Session
from ..models.fine import Fine, FineStatus


class FinesRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, loan_id: int, user_id: int, amount: float):
        fine = Fine(loan_id=loan_id, user_id=user_id, amount=amount)
        self.db.add(fine)
        self.db.commit()
        self.db.refresh(fine)
        return fine

    def list_by_user(self, user_id: int):
        return self.db.query(Fine).filter(Fine.user_id == user_id).all()

    def mark_paid(self, fine_id: int):
        fine = self.db.query(Fine).get(fine_id)
        if not fine:
            return None
        fine.status = FineStatus.paid
        self.db.commit()
        self.db.refresh(fine)
        return fine

