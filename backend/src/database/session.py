from sqlmodel import create_engine, Session
from contextlib import contextmanager
import os
from typing import Generator
from ..config import settings
import re


# Determine if using PostgreSQL or SQLite and create appropriate sync engine
database_url_str = str(settings.database_url)
is_postgresql = 'postgresql' in database_url_str

# For sync engine, we need to ensure proper PostgreSQL driver is used
if is_postgresql:
    # Replace postgresql+asyncpg:// with postgresql:// for sync operations
    if 'postgresql+asyncpg://' in database_url_str:
        database_url_str = database_url_str.replace('postgresql+asyncpg://', 'postgresql://', 1)
    # If it's already postgresql://, keep it as is

# Create the database engine with appropriate configuration
if is_postgresql:
    # PostgreSQL-specific settings
    engine = create_engine(
        database_url_str,
        echo=settings.database_echo,
        pool_pre_ping=True,
        pool_recycle=settings.neon_pool_recycle,
        pool_size=settings.neon_pool_size,
        max_overflow=settings.neon_max_overflow,
        pool_timeout=settings.neon_pool_timeout,
        connect_args={
            "connect_timeout": 10,
        }
    )
else:
    # SQLite settings
    engine = create_engine(
        database_url_str,
        echo=settings.database_echo,
        pool_pre_ping=True,
        pool_recycle=3600,  # Default for SQLite
        pool_size=5,        # Default for SQLite
        max_overflow=10,    # Default for SQLite
        pool_timeout=30,    # Default for SQLite
        connect_args={
            "timeout": 10,
        }
    )


from contextlib import contextmanager

from contextlib import contextmanager

def get_session():
    """
    Get a database session for FastAPI dependency injection.

    This function is a generator that yields a session and ensures it's closed.
    It's designed to work with FastAPI's Depends system.
    expire_on_commit=False keeps objects accessible after commit/rollback.

    Usage:
        def some_function(session: Session = Depends(get_session)):
            # Perform database operations
            session.add(obj)
            session.commit()
    """
    session = Session(engine, expire_on_commit=False)
    try:
        yield session
    finally:
        session.close()

@contextmanager
def get_session_context():
    """
    Context manager for database sessions.

    Usage:
        with get_session_context() as session:
            # Perform database operations
            session.add(obj)
            session.commit()
    """
    session = Session(engine, expire_on_commit=False)
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def get_session_direct():
    """
    Get a direct database session (without context manager).
    This is useful for async operations where context managers might not work well.
    expire_on_commit=False keeps objects accessible after commit/rollback.

    Returns:
        Session: A database session that must be manually closed
    """
    return Session(engine, expire_on_commit=False)


def get_engine():
    """
    Get the database engine directly.

    Returns:
        Engine: The SQLAlchemy engine instance
    """
    return engine


def create_db_and_tables():
    """
    Create database tables based on the models.
    This should be called during application startup.
    """
    # Only import models if they haven't been imported yet to prevent conflicts
    import sys
    if 'src.database.models' not in sys.modules:
        from ..database.models import User, Conversation, Message, Task  # Import canonical models

    # Create all tables defined in the models
    from sqlmodel import SQLModel
    SQLModel.metadata.create_all(engine)


# Initialize the database tables when this module is imported
# This is commented out to allow manual control over when tables are created
# create_db_and_tables()