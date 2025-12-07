from fastapi import FastAPI
from app.api.v1.routers import auth, books, reviews
from app.core.config import settings

app = FastAPI(title="Book Management API")

app.include_router(auth.router)
app.include_router(books.router)
app.include_router(reviews.router)

@app.get("/healthz")
async def health():
    return {"status": "ok"}
