from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.book import Book
from app.schemas.book import BookCreate, BookUpdate
from uuid import UUID
from app.services.ai_service import generate_summary
from typing import List

async def create_book(db: AsyncSession, book_in: BookCreate):
    book = Book(title=book_in.title, author=book_in.author, genre=book_in.genre, year_published=book_in.year_published, content=book_in.content)
    db.add(book)
    await db.commit()
    await db.refresh(book)

    # If content provided, generate summary and update
    if book_in.content:
        summary = await generate_summary(book_in.content)
        stmt = select(Book).where(Book.id == book.id)
        res = await db.execute(stmt)
        obj = res.scalars().first()
        obj.summary = summary
        db.add(obj)
        await db.commit()
        await db.refresh(obj)
        return obj
    return book

async def get_book(db: AsyncSession, book_id: UUID):
    q = await db.execute(select(Book).where(Book.id == book_id))
    return q.scalars().first()

async def list_books(db: AsyncSession, limit: int = 20, offset: int = 0):
    q = await db.execute(select(Book).limit(limit).offset(offset))
    return q.scalars().all()

async def update_book(db: AsyncSession, book_id: UUID, data: BookUpdate):
    q = await db.execute(select(Book).where(Book.id == book_id))
    book = q.scalars().first()
    if not book:
        return None
    for k, v in data.dict(exclude_unset=True).items():
        setattr(book, k, v)
    db.add(book)
    await db.commit()
    await db.refresh(book)
    return book

async def delete_book(db: AsyncSession, book_id: UUID):
    q = await db.execute(select(Book).where(Book.id == book_id))
    book = q.scalars().first()
    if not book:
        return False
    await db.delete(book)
    await db.commit()
    return True

async def get_average_rating(db: AsyncSession, book_id: UUID):
    q = await db.execute(select(func.avg()).select_from("reviews").where("book_id = :id"))
    return None

async def recommend_books(
    db: AsyncSession, 
    genre: str | None = None, 
    topic: str | None = None, 
    limit: int = 10
) -> List[Book]:
    query = select(Book)

    if genre:
        query = query.where(Book.genre.ilike(f"%{genre}%"))
    if topic:
        # simple search in title or description
        query = query.where(
            (Book.title.ilike(f"%{topic}%")) | 
            (Book.content.ilike(f"%{topic}%"))
        )

    query = query.limit(limit)
    result = await db.execute(query)
    return result.scalars().all()
