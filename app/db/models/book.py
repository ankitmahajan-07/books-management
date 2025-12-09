import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.db.base import Base

class Book(Base):
    __tablename__ = "books"
    id = sa.Column(UUID(as_uuid=True).with_variant(sa.String(36), "sqlite"), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = sa.Column(sa.String(), nullable=False, index=True)
    author = sa.Column(sa.String(), nullable=True)
    genre = sa.Column(sa.String(), nullable=True, index=True)
    year_published = sa.Column(sa.Integer(), nullable=True)
    content = sa.Column(sa.Text(), nullable=True)
    summary = sa.Column(sa.Text(), nullable=True)
    created_at = sa.Column(sa.DateTime(timezone=True), server_default=sa.func.now())
