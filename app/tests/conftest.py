import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.base import Base
from app.db.session import get_db
import pytest
from unittest.mock import AsyncMock
import uuid

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


# -------------------------
# ENGINE (FUNCTION SCOPE)
# -------------------------
@pytest_asyncio.fixture
async def engine():
    engine = create_async_engine(TEST_DATABASE_URL, future=True)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine
    await engine.dispose()


# -------------------------
# DATABASE SESSION
# -------------------------
@pytest_asyncio.fixture
async def db_session(engine):
    async_session = sessionmaker(
        engine,
        expire_on_commit=False,
        class_=AsyncSession,
    )
    async with async_session() as session:
        yield session


# -------------------------
# DEPENDENCY OVERRIDE
# -------------------------
@pytest_asyncio.fixture(autouse=True)
async def override_get_db(db_session):
    async def _override():
        yield db_session

    app.dependency_overrides[get_db] = _override
    yield
    app.dependency_overrides.clear()


# -------------------------
# HTTP TEST CLIENT
# -------------------------
@pytest_asyncio.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(autouse=True)
def mock_generate_summary(monkeypatch):
    monkeypatch.setattr("app.services.ai_service.generate_summary", AsyncMock(return_value="This is a summary."))

@pytest.fixture(autouse=True)
def mock_auth_user(monkeypatch):
    monkeypatch.setattr("app.core.security.get_current_user", AsyncMock(return_value={"id": uuid.uuid4()}))
