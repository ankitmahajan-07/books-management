from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class BookCreate(BaseModel):
    title: str
    author: Optional[str] = None
    genre: Optional[str] = None
    year_published: Optional[int] = None
    content: Optional[str] = None

class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    genre: Optional[str] = None
    year_published: Optional[int] = None
    content: Optional[str] = None

class BookRead(BaseModel):
    id: UUID
    title: str
    author: Optional[str]
    genre: Optional[str]
    year_published: Optional[int]
    content: Optional[str]

    class Config:
        from_attributes = True
