import pytest
from httpx import AsyncClient
import uuid

# --------------------------
#  FIXTURES
# --------------------------

@pytest.fixture
async def created_book(client):
    """
    Creates a book and returns the created payload + id.
    """
    payload = {"title": "Don Quixote", "author": "Cervantes", "genre": "Classic", "content": "A classic novel."}
    resp = await client.post("/v1/books/", json=payload)
    assert resp.status_code == 201
    data = resp.json()
    print("Created book data:", data)
    return data  # includes id


# --------------------------
#  TESTS: CREATE
# --------------------------

@pytest.mark.asyncio
async def test_create_book(client):
    payload = {"title": "Dune", "author": "Frank Herbert", "genre": "Sci-Fi", "content": "Epic science fiction."}
    resp = await client.post("/v1/books/", json=payload)
    assert resp.status_code == 201

    data = resp.json()
    assert data["title"] == payload["title"]
    assert data["author"] == payload["author"]


# --------------------------
#  TESTS: GET BOOK
# --------------------------

@pytest.mark.asyncio
async def test_get_book_success(client, created_book):
    book = await created_book
    book_id = book["id"]

    resp = await client.get(f"/v1/books/{book_id}")
    assert resp.status_code == 200

    data = resp.json()
    assert data["id"] == book_id


@pytest.mark.asyncio
async def test_get_book_not_found(client):
    resp = await client.get("/v1/books/999999")
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Book not found"


# --------------------------
#  TESTS: LIST BOOKS
# --------------------------

@pytest.mark.asyncio
async def test_list_books(client, created_book):
    await created_book
    resp = await client.get("/v1/books/?limit=10&offset=0")
    assert resp.status_code == 200

    data = resp.json()
    assert isinstance(data, list)
    assert len(data) >= 1  # at least created book exists


# --------------------------
#  TESTS: UPDATE BOOK
# --------------------------

@pytest.mark.asyncio
async def test_update_book(client, created_book):
    # Await the fixture to get the actual book
    book = await created_book
    book_id = book["id"]
    print("Book ID for update test:", book_id)

    update_payload = {"title": "Don Quixote Revised"}
    resp = await client.put(f"/v1/books/{book_id}", json=update_payload)
    print("response text:", resp.text)
    assert resp.status_code == 200

    data = resp.json()
    assert data["title"] == "Don Quixote Revised"


# --------------------------
# TEST: UPDATE BOOK NOT FOUND
# --------------------------
@pytest.mark.asyncio
async def test_update_book_not_found(client):
    random_uuid = str(uuid.uuid4())  # generate a valid UUID
    resp = await client.put(f"/v1/books/{random_uuid}", json={"title": "X"})
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Book not found"


# --------------------------
#  TESTS: DELETE
# --------------------------

@pytest.mark.asyncio
async def test_delete_book(client, created_book):
    book = await created_book
    book_id = book["id"]

    resp = await client.delete(f"/v1/books/{book_id}")
    assert resp.status_code == 200
    assert resp.json() == {"ok": True}

    # ensure deleted
    resp2 = await client.get(f"/v1/books/{book_id}")
    assert resp2.status_code == 404


@pytest.mark.asyncio
async def test_delete_book_not_found(client):
    resp = await client.delete("/v1/books/999999")
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Book not found"


# --------------------------
#  TESTS: RECOMMENDATIONS
# --------------------------

@pytest.mark.asyncio
async def test_recommend_books_by_genre(client):
    # create some books
    await client.post("/v1/books/", json={"title": "Book A", "author": "A", "genre": "Fantasy", "content": "Fantasy A"})
    await client.post("/v1/books/", json={"title": "Book B", "author": "B", "genre": "Fantasy", "content": "Fantasy B"})
    await client.post("/v1/books/", json={"title": "Book C", "author": "C", "genre": "Horror", "content": "Horror C"})

    resp = await client.get("/v1/books/recommend?genre=Fantasy")
    assert resp.status_code == 200

    data = resp.json()
    assert len(data) >= 2
    assert all("Fantasy" in (b.get("genre") or "") for b in data)


@pytest.mark.asyncio
async def test_recommend_books_by_topic(client):
    await client.post("/v1/books/", json={
        "title": "AI Basics",
        "author": "X",
        "genre": "Tech",
        "content": "An introductory AI book."
    })

    resp = await client.get("/v1/books/recommend?topic=AI")
    assert resp.status_code == 200

    data = resp.json()
    assert len(data) >= 1


@pytest.mark.asyncio
async def test_recommend_requires_input(client):
    resp = await client.get("/v1/books/recommend")
    assert resp.status_code == 200  # your code returns empty list
    assert resp.json() == []        # validate expected behavior
