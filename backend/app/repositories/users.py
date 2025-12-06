from sqlalchemy.orm import Session
from passlib.context import CryptContext
from ..models.user import User, UserRole


pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


class UsersRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_username(self, username: str):
        return self.db.query(User).filter(User.username == username).first()

    def get_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()

    def create(self, username: str, email: str, password: str, role: str = "reader"):
        hashed = pwd_context.hash(password)
        user = User(username=username, email=email, password_hash=hashed, role=UserRole(role))
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def verify_password(self, plain: str, hashed: str) -> bool:
        return pwd_context.verify(plain, hashed)

