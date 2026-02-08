from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession as SQLModelAsyncSession
from contextlib import asynccontextmanager
import os
from typing import AsyncGenerator
from ..config import settings
import logging

logger = logging.getLogger(__name__)

import re

# Determine if using PostgreSQL or SQLite
database_url_str = str(settings.database_url)
is_postgresql = 'postgresql' in database_url_str

# Ensure PostgreSQL URL uses asyncpg driver
if is_postgresql and 'postgresql+asyncpg://' not in database_url_str:
    # Replace postgresql:// with postgresql+asyncpg://
    database_url_str = database_url_str.replace('postgresql://', 'postgresql+asyncpg://', 1)

# Create async engine with appropriate configuration
connect_args = {}

if is_postgresql:
    # PostgreSQL-specific settings
    connect_args = {
        "server_settings": {
            "application_name": "todo-chatbot-backend",
            "tcp_keepalives_idle": "600",  # 10 minutes
            "tcp_keepalives_interval": "30",  # 30 seconds
            "tcp_keepalives_count": "3",  # 3 keepalive attempts
        },
        "command_timeout": 30,  # 30 seconds timeout
        "statement_timeout": settings.neon_statement_timeout,  # Use configured timeout
    }

engine = create_async_engine(
    database_url_str,
    echo=settings.database_echo,  # Controlled by settings
    pool_size=settings.neon_pool_size if is_postgresql else 5,
    max_overflow=settings.neon_max_overflow if is_postgresql else 10,
    pool_pre_ping=True if is_postgresql else True,  # Safe to use for both
    pool_recycle=settings.neon_pool_recycle if is_postgresql else 3600,
    pool_timeout=settings.neon_pool_timeout if is_postgresql else 30,
    pool_reset_on_return="commit" if is_postgresql else "commit",
    connect_args=connect_args,
)

logger.info(f"Database engine created with pool configuration: "
           f"size={settings.neon_pool_size if is_postgresql else 5}, "
           f"max_overflow={settings.neon_max_overflow if is_postgresql else 10}, "
           f"recycle={settings.neon_pool_recycle if is_postgresql else 3600}s, "
           f"timeout={settings.neon_pool_timeout if is_postgresql else 30}s")


# Create async session factory
AsyncSessionFactory = sessionmaker(
    engine,
    class_=SQLModelAsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)


@asynccontextmanager
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Async context manager for database sessions.
    Ensures proper session cleanup after use.
    """
    async with AsyncSessionFactory() as session:
        try:
            logger.debug("Acquired database session")
            yield session
        except Exception as e:
            logger.error(f"Database session error: {str(e)}")
            await session.rollback()
            raise
        finally:
            await session.close()
            logger.debug("Released database session")


async def close_engine():
    """Close the database engine connection."""
    logger.info("Closing database engine")
    await engine.dispose()


def get_connection_pool_stats():
    """Get statistics about the current connection pool."""
    pool = engine.pool
    return {
        "size": pool.size(),
        "checkedin": pool.checkedin(),
        "overflow": pool.overflow(),
        "checkedout": pool.checkedout(),
    }