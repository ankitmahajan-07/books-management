import sqlalchemy as sa
import uuid
from app.db.base import Base
from sqlalchemy.dialects.postgresql import UUID


class Review(Base):
    __tablename__ = "reviews"
    id = sa.Column(UUID(as_uuid=True).with_variant(sa.String(36), "sqlite"), primary_key=True, default=lambda: str(uuid.uuid4()))
    book_id = sa.Column(UUID(as_uuid=True).with_variant(sa.String(36), "sqlite"), sa.ForeignKey("books.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = sa.Column(UUID(as_uuid=True).with_variant(sa.String(36), "sqlite"), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    review_text = sa.Column(sa.Text(), nullable=True)
    rating = sa.Column(sa.SmallInteger(), nullable=False)
    created_at = sa.Column(sa.DateTime(timezone=True), server_default=sa.func.now())
