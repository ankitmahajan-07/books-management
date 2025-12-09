from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List

from app.db.session import get_db
from app.services.review_service import add_review, list_reviews_for_book, get_aggregate_rating
from app.schemas.review import ReviewCreate, ReviewRead
from app.core.security import get_current_user  # NEW


router = APIRouter(prefix="/v1/books", tags=["reviews"])


@router.post("/{book_id}/reviews", response_model=ReviewRead)
async def post_review(
    book_id: UUID,
    review_in: ReviewCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)  # ✅ Use authenticated user
):
    """
    Add a review for a book (one per user per book).
    """
    review = await add_review(
        db=db,
        book_id=book_id,
        user_id=current_user.id,
        review_in=review_in
    )
    return review


@router.get("/{book_id}/reviews", response_model=List[ReviewRead])
async def get_reviews(book_id: UUID, db: AsyncSession = Depends(get_db)):
    """
    Fetch all reviews for a book.
    """
    return await list_reviews_for_book(db, book_id)


@router.get("/{book_id}/rating", response_model=dict)
async def book_rating(book_id: UUID, db: AsyncSession = Depends(get_db)):
    """
    Return average rating for book.
    """
    avg = await get_aggregate_rating(db, book_id)
    return {"average_rating": float(avg) if avg is not None else None}
