"""Database configuration and session management."""
from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool
import logging

from .config import settings

logger = logging.getLogger(__name__)

# Create engine with connection pooling
engine = create_engine(
    settings.database_url,
    echo=settings.debug,
    poolclass=QueuePool,
    pool_size=settings.database_pool_size,
    max_overflow=settings.database_max_overflow,
    pool_pre_ping=True,  # Verify connections before using
    pool_recycle=3600,   # Recycle connections after 1 hour
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False
)

Base = declarative_base()


@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_conn, connection_record):
    """Set database connection parameters."""
    # This can be used for SQLite-specific settings if needed
    pass


def get_db() -> Session:
    """
    Dependency for getting database session.
    
    Yields:
        Session: Database session
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

