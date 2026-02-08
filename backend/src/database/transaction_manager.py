"""
Database transaction management.
"""
from contextlib import contextmanager
from sqlmodel import Session
from typing import Generator
from .connection_pool import get_engine


class TransactionManager:
    """Manages database transactions."""

    @staticmethod
    @contextmanager
    def get_session() -> Generator[Session, None, None]:
        """Get a session with automatic transaction management."""
        engine = get_engine()
        with Session(engine, expire_on_commit=False) as session:
            try:
                yield session
                session.commit()
            except Exception:
                session.rollback()
                raise
            finally:
                session.close()

    @staticmethod
    @contextmanager
    def get_read_only_session() -> Generator[Session, None, None]:
        """Get a read-only session."""
        engine = get_engine()
        with Session(engine, expire_on_commit=False) as session:
            try:
                # Set the session to read-only mode
                session.connection(execution_options={"isolation_level": "READ COMMITTED"})
                yield session
            finally:
                session.close()

    @staticmethod
    def execute_in_transaction(func, *args, **kwargs):
        """Execute a function within a transaction."""
        engine = get_engine()
        with Session(engine, expire_on_commit=False) as session:
            try:
                result = func(session, *args, **kwargs)
                session.commit()
                return result
            except Exception:
                session.rollback()
                raise
            finally:
                session.close()


# Convenience functions
@contextmanager
def get_session() -> Generator[Session, None, None]:
    """Convenience function to get a managed session."""
    with TransactionManager.get_session() as session:
        yield session


def execute_in_transaction(func, *args, **kwargs):
    """Convenience function to execute in transaction."""
    return TransactionManager.execute_in_transaction(func, *args, **kwargs)