from sqlalchemy import Column, Integer, String, DateTime, Enum
from datetime import datetime
import enum
from ..core.db import Base


class UserRole(enum.Enum):
    reader = "reader"
    admin = "admin"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.reader, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

