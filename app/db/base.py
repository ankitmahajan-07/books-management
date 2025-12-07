from sqlalchemy.orm import declarative_base

Base = declarative_base()

# Import all models here so Alembic's autogenerate can see them
# (No model imports here to avoid circular import)
