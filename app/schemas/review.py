from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class ReviewCreate(BaseModel):
    review_text: Optional[str]
    rating: int

class ReviewRead(BaseModel):
    id: UUID
    book_id: UUID
    user_id: UUID
    review_text: Optional[str]
    rating: int

    class Config:
        from_attributes = True
