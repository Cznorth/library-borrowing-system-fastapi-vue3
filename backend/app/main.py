from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core.config import settings
from .core.db import SessionLocal
from .repositories.users import UsersRepository
from .models.user import UserRole
from .api.routes import api_router

app = FastAPI(title="Library Borrowing System", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(api_router, prefix="/api")


@app.on_event("startup")
def ensure_default_admin():
    db = SessionLocal()
    try:
        repo = UsersRepository(db)
        # 简单检查是否存在任一管理员
        from sqlalchemy import select
        from .models.user import User
        exists_admin = db.execute(select(User).where(User.role == UserRole.admin)).first()
        if exists_admin:
            return
        username = settings.DEFAULT_ADMIN_USERNAME or "admin"
        email = settings.DEFAULT_ADMIN_EMAIL or "admin@example.com"
        password = settings.DEFAULT_ADMIN_PASSWORD or "Admin@12345"
        if not repo.get_by_username(username) and not repo.get_by_email(email):
            repo.create(username=username, email=email, password=password, role="admin")
    finally:
        db.close()

