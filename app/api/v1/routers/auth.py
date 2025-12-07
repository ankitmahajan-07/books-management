from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.auth_service import authenticate_user, create_user, create_tokens_for_user
from app.schemas.user import UserCreate, Token

router = APIRouter(prefix="/v1/auth", tags=["auth"])

@router.post("/register", response_model=dict)
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    print("user details:", user_in)
    user = await create_user(db, user_in)
    return {"id": str(user.id), "username": user.username}

@router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    tokens = await create_tokens_for_user(user)
    return tokens
