import sqlalchemy as sa
import uuid
from app.db.base import Base

class User(Base):
    __tablename__ = "users"
    id = sa.Column(sa.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = sa.Column(sa.String(length=150), unique=True, nullable=False, index=True)
    email = sa.Column(sa.String(length=255), unique=True, nullable=False, index=True)
    hashed_password = sa.Column(sa.String(length=255), nullable=False)
    role = sa.Column(sa.String(length=50), nullable=False, server_default="user")
    created_at = sa.Column(sa.DateTime(timezone=True), server_default=sa.func.now())
