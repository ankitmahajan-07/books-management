from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.user import User
from app.core.security import get_password_hash, verify_password, create_access_token
from app.schemas.user import UserCreate
from fastapi import HTTPException, status

async def get_user_by_username(db: AsyncSession, username: str):
    q = await db.execute(select(User).where(User.username == username))
    return q.scalars().first()

async def create_user(db: AsyncSession, user_in: UserCreate, role: str = "user"):
    # validate unique
    existing = await get_user_by_username(db, user_in.username)
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")
    user = User(username=user_in.username, email=user_in.email, hashed_password=get_password_hash(user_in.password), role=role)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

async def authenticate_user(db: AsyncSession, username: str, password: str):
    user = await get_user_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

async def create_tokens_for_user(user: User):
    token = create_access_token({"sub": str(user.id), "role": user.role})
    return {"access_token": token, "token_type": "bearer"}
