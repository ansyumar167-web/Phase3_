from sqlmodel import SQLModel
from .async_session import engine
from .models import User, Conversation, Message, Task
import asyncio
from typing import Optional


async def create_tables():
    """Create all database tables asynchronously."""
    async with engine.begin() as conn:
        # Create tables based on models
        await conn.run_sync(SQLModel.metadata.create_all)


async def init_db():
    """Initialize the database with required tables."""
    print("Initializing database...")
    await create_tables()
    print("Database initialized successfully!")


async def drop_tables():
    """Drop all database tables (use with caution!)."""
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)


def run_init_db():
    """Synchronous wrapper to run database initialization."""
    asyncio.run(init_db())


if __name__ == "__main__":
    run_init_db()