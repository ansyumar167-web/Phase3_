"""
Database connection pooling for concurrent access.
"""
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool
from ..config import settings
import threading


# Thread-local storage for database connections
_local_storage = threading.local()


class ConnectionPoolManager:
    """Manages database connection pools for concurrent access."""

    def __init__(self):
        """Initialize the connection pool manager."""
        self._engine = None
        self._lock = threading.Lock()

    def get_engine(self):
        """Get the database engine with connection pooling."""
        if self._engine is None:
            with self._lock:
                if self._engine is None:  # Double-check locking
                    connection_string = str(settings.database_url)

                    # Create engine with connection pooling
                    self._engine = create_engine(
                        connection_string,
                        poolclass=QueuePool,
                        pool_size=20,  # Number of connections to maintain
                        max_overflow=30,  # Additional connections beyond pool_size
                        pool_pre_ping=True,  # Verify connections before use
                        pool_recycle=3600,  # Recycle connections after 1 hour
                        pool_timeout=30,  # Timeout for getting connection from pool
                        echo=settings.database_echo
                    )
        return self._engine

    def get_connection(self):
        """Get a database connection from the pool."""
        engine = self.get_engine()
        return engine.connect()

    def dispose_engine(self):
        """Dispose of the engine and close all connections."""
        if self._engine:
            self._engine.dispose()
            self._engine = None


# Global connection pool manager instance
connection_pool_manager = ConnectionPoolManager()


def get_engine():
    """Convenience function to get the shared engine."""
    return connection_pool_manager.get_engine()


def get_connection():
    """Convenience function to get a connection from the pool."""
    return connection_pool_manager.get_connection()