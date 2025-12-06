from typing import Generator
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from .core.config import settings
from .core.db import SessionLocal
from .repositories.users import UsersRepository
from .models.user import UserRole


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(token: str = Depends(oauth2_scheme), db=Depends(get_db)):
    credentials_exception = HTTPException(status_code=401, detail="Could not validate credentials")
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    repo = UsersRepository(db)
    user = repo.get_by_username(username)
    if not user:
        raise credentials_exception
    return user


def require_admin(current=Depends(get_current_user)):
    if current.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Admin privilege required")
    return current

