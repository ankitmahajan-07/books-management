import sqlalchemy as sa
import uuid
from app.db.base import Base


class Review(Base):
    __tablename__ = "reviews"
    id = sa.Column(sa.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    book_id = sa.Column(sa.String(36), sa.ForeignKey("books.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = sa.Column(sa.String(36), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    review_text = sa.Column(sa.Text(), nullable=True)
    rating = sa.Column(sa.SmallInteger(), nullable=False)
    created_at = sa.Column(sa.DateTime(timezone=True), server_default=sa.func.now())
