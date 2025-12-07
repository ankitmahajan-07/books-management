from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from uuid import UUID

from app.db.models.review import Review
from app.db.models.book import Book
from app.schemas.review import ReviewCreate


async def add_review(db: AsyncSession, book_id: UUID, user_id: UUID, review_in: ReviewCreate):
    """
    Creates a new review for a book.
    Restriction: One review per user per book.
    """
    # Ensure the book exists
    book = await db.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    # Check for existing review by same user on same book
    existing_q = await db.execute(
        select(Review).where(
            Review.book_id == book_id,
            Review.user_id == user_id
        )
    )
    existing = existing_q.scalar_one_or_none()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="You have already reviewed this book"
        )

    # Create new review
    review = Review(
        book_id=book_id,
        user_id=user_id,
        review_text=review_in.review_text,
        rating=review_in.rating,
    )

    db.add(review)
    await db.commit()
    await db.refresh(review)

    return review


async def list_reviews_for_book(db: AsyncSession, book_id: UUID):
    """
    Fetch all reviews for a given book.
    """
    q = await db.execute(select(Review).where(Review.book_id == book_id))
    return q.scalars().all()


async def get_aggregate_rating(db: AsyncSession, book_id: UUID):
    """
    Returns average rating for a book.
    """
    q = await db.execute(
        select(func.avg(Review.rating)).where(Review.book_id == book_id)
    )
    avg_rating = q.scalar()
    return float(avg_rating) if avg_rating is not None else None
