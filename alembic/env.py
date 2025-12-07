from logging.config import fileConfig
from sqlalchemy import pool, create_engine
from alembic import context
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from app.db.base import Base
from app.core.config import settings

config = context.config
fileConfig(config.config_file_name)
target_metadata = Base.metadata

def run_migrations_offline():
    url = settings.database_url
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = create_engine(settings.database_url.replace("+asyncpg", "+psycopg2"), poolclass=pool.NullPool)
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
