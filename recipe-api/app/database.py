"""Database connection setup (SQLAlchemy)."""
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import settings

# The engine is the "connection manager" to PostgreSQL.
engine = create_engine(settings.database_url, pool_pre_ping=True)

# A session is one "conversation" with the database (one per request).
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    """All database models inherit from this class."""


def get_db():
    """Gives each request its own session and always closes it at the end."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
