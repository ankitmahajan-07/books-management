from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.book import BookCreate, BookRead, BookUpdate
from app.services.book_service import create_book, get_book, list_books, recommend_books, update_book, delete_book
from typing import List
from fastapi import Body

router = APIRouter(prefix="/v1/books", tags=["books"])

@router.post("/", response_model=BookRead, status_code=status.HTTP_201_CREATED)
async def create_book_endpoint(book_in: BookCreate, db: AsyncSession = Depends(get_db)):
    book = await create_book(db, book_in)
    return book

@router.get("/", response_model=List[BookRead])
async def list_books_endpoint(limit: int = 20, offset: int = 0, db: AsyncSession = Depends(get_db)):
    return await list_books(db, limit=limit, offset=offset)

@router.get("/recommend", response_model=List[BookRead])
async def recommend_books_endpoint(
    genre: str | None = None,
    topic: str | None = None,
    limit: int = 10,
    db: AsyncSession = Depends(get_db)
):
    """
    Recommend books based on genre or topic keywords.
    At least one of `genre` or `topic` should be provided.
    """
    if not genre and not topic:
        return []  # or raise HTTPException(status_code=400, detail="Provide genre or topic")
    books = await recommend_books(db, genre, topic, limit)
    return books

@router.get("/{book_id}", response_model=BookRead)
async def get_book_endpoint(book_id: str, db: AsyncSession = Depends(get_db)):
    book = await get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.put("/{book_id}", response_model=BookRead)
async def update_book_endpoint(
    book_id: str,
    data: BookUpdate = Body(...),
    db: AsyncSession = Depends(get_db)
):
    book = await update_book(db, book_id, data)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.delete("/{book_id}")
async def delete_book_endpoint(book_id: str, db: AsyncSession = Depends(get_db)):
    ok = await delete_book(db, book_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"ok": True}

