import pytest
from httpx import AsyncClient
from uuid import uuid4
from unittest.mock import AsyncMock
from app.main import app
from app.db.models.user import User  # SQLAlchemy User model

# -------------------------------
# Override get_current_user for tests
# -------------------------------
async def override_get_current_user():
    return User(id=uuid4(), username="testuser", email="test@test.com", hashed_password="fake")

from app.core.security import get_current_user
app.dependency_overrides[get_current_user] = override_get_current_user

# -------------------------------
# Fixtures
# -------------------------------
@pytest.fixture
def review_payload():
    return {"comment": "Amazing book!", "rating": 5}

@pytest.fixture
async def created_book(client: AsyncClient, monkeypatch):
    # Mock AI summary
    monkeypatch.setattr(
        "app.services.ai_service.generate_summary",
        AsyncMock(return_value='{"summary": "This is a summary."}')
    )

    resp = await client.post("/v1/books/", json={
        "title": "New Book",
        "author": "Author",
        "genre": "Fiction",
        "content": "Some content"
    })
    assert resp.status_code == 201
    return resp.json()

@pytest.fixture
async def created_review(client: AsyncClient, created_book, review_payload):
    book = await created_book
    book_id = book["id"]

    resp = await client.post(f"/v1/books/{book_id}/reviews", json=review_payload)
    assert resp.status_code == 201
    data = resp.json()
    data["book_id"] = book_id
    return data

# -------------------------------
# Tests
# -------------------------------
@pytest.mark.asyncio
async def test_post_review(client: AsyncClient, created_book, review_payload):
    book = await created_book
    book_id = book["id"]

    resp = await client.post(f"/v1/books/{book_id}/reviews", json=review_payload)
    data = resp.json()

    assert resp.status_code == 201
    assert data["comment"] == review_payload["comment"]
    assert data["rating"] == review_payload["rating"]
    assert data["book_id"] == book_id

@pytest.mark.asyncio
async def test_get_reviews(client: AsyncClient, created_review):
    review = await created_review
    book_id = review["book_id"]

    resp = await client.get(f"/v1/books/{book_id}/reviews")
    data = resp.json()

    assert resp.status_code == 200
    assert len(data) > 0
    assert data[0]["book_id"] == book_id

@pytest.mark.asyncio
async def test_book_summary(client: AsyncClient, created_review):
    review = await created_review
    book_id = review["book_id"]

    resp = await client.get(f"/v1/books/{book_id}/summary")
    data = resp.json()

    assert resp.status_code == 200
    assert "average_rating" in data
    assert isinstance(data["average_rating"], float)
