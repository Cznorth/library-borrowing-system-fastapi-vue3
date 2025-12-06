from typing import Optional
from pydantic import BaseModel, Field, HttpUrl


class BookBase(BaseModel):
    isbn: Optional[str] = Field(default=None, max_length=20)
    title: str = Field(min_length=1, max_length=255)
    author: str = Field(min_length=1, max_length=255)
    publisher: Optional[str] = Field(default=None, max_length=255)
    year: Optional[int] = Field(default=None, ge=1000, le=2100)
    category: Optional[str] = Field(default=None, max_length=100)
    tags: Optional[str] = Field(default=None, max_length=255)
    summary: Optional[str] = None
    cover_url: Optional[HttpUrl] = None


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    isbn: Optional[str] = Field(default=None, max_length=20)
    title: Optional[str] = Field(default=None, max_length=255)
    author: Optional[str] = Field(default=None, max_length=255)
    publisher: Optional[str] = Field(default=None, max_length=255)
    year: Optional[int] = Field(default=None, ge=1000, le=2100)
    category: Optional[str] = Field(default=None, max_length=100)
    tags: Optional[str] = Field(default=None, max_length=255)
    summary: Optional[str] = None
    cover_url: Optional[HttpUrl] = None

