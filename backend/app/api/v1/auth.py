from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ...schemas.auth import Token, LoginRequest, RegisterRequest
from ...core.security import create_access_token
from ...deps import get_db
from ...repositories.users import UsersRepository


router = APIRouter()


@router.post("/login", response_model=Token)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    repo = UsersRepository(db)
    user = repo.get_by_username(data.username)
    if not user or not repo.verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    token = create_access_token(subject=user.username)
    return {"access_token": token}


@router.post("/register")
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    repo = UsersRepository(db)
    if repo.get_by_username(data.username) or repo.get_by_email(data.email):
        raise HTTPException(status_code=400, detail="User already exists")
    user = repo.create(data.username, data.email, data.password, data.role)
    return {"id": user.id, "username": user.username}

