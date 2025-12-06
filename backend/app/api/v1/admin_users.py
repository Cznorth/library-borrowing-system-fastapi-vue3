from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ...deps import get_db, require_admin
from ...repositories.users import UsersRepository
from ...models.user import User, UserRole


router = APIRouter(dependencies=[Depends(require_admin)])


@router.get("")
def list_users(page: int = 1, page_size: int = 10, db: Session = Depends(get_db)):
    repo = UsersRepository(db)
    query = db.query(User)
    total = query.count()
    items = query.offset((page - 1) * page_size).limit(page_size).all()
    return {"total": total, "items": items}


@router.patch("/{user_id}")
def update_user(user_id: int, data: dict, db: Session = Depends(get_db)):
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    for k, v in data.items():
        if k in {"username", "email", "role"}:
            if k == "role":
                if isinstance(v, str):
                    val = v.lower()
                    if val == "user":
                        val = "reader"
                    try:
                        setattr(user, k, UserRole(val))
                    except Exception:
                        raise HTTPException(status_code=422, detail="Invalid role")
                elif isinstance(v, UserRole):
                    setattr(user, k, v)
                else:
                    raise HTTPException(status_code=422, detail="Invalid role")
            else:
                setattr(user, k, v)
    db.commit()
    db.refresh(user)
    return user


@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"ok": True}

