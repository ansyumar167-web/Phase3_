"""
Neon PostgreSQL database migration and setup for the Todo AI Agent.

This module handles:
1. Creating the database schema based on models
2. Setting up proper indexes for efficient queries
3. Initializing with sample data if needed
4. Providing connection optimization for Neon's serverless architecture
"""

import asyncio
from sqlmodel import SQLModel, Session, select
from sqlalchemy import text
from .session import get_engine
from .session import get_session_context
from ..models.task import Task, TaskCreate
from ..models.conversation import Conversation, ConversationCreate
from ..models.message import Message, MessageCreate, MessageRole
from typing import List
import logging

logger = logging.getLogger(__name__)

def create_db_and_tables():
    """Create database tables and indexes optimized for Neon PostgreSQL."""
    engine = get_engine()

    print("[INFO] Creating database tables...")
    SQLModel.metadata.create_all(engine)
    print("[INFO] Database tables created successfully!")

    # Create additional indexes optimized for Neon PostgreSQL
    create_indexes(engine)
    print("[INFO] Indexes created successfully!")

def create_indexes(engine):
    """Create additional indexes optimized for query performance."""
    with engine.connect() as conn:
        # Index on user_id for efficient user-based queries (common in all tables)
        try:
            conn.execute(text("CREATE INDEX IF NOT EXISTS idx_tasks_user_id ON tasks (user_id);"))
            conn.execute(text("CREATE INDEX IF NOT EXISTS idx_conversation_user_id ON conversation (user_id);"))
            conn.execute(text("CREATE INDEX IF NOT EXISTS idx_message_user_id ON message (user_id);"))
        except Exception as e:
            print(f"Warning: Could not create user_id indexes: {e}")

        # Index on completed field for task queries
        try:
            conn.execute(text("CREATE INDEX IF NOT EXISTS idx_tasks_completed ON tasks (completed);"))
        except Exception as e:
            print(f"Warning: Could not create completed index: {e}")

        # Composite index for user_id and completed for efficient filtering
        try:
            conn.execute(text("CREATE INDEX IF NOT EXISTS idx_tasks_user_completed ON tasks (user_id, completed);"))
        except Exception as e:
            print(f"Warning: Could not create user/completed composite index: {e}")

        # Index on conversation_id for message queries
        try:
            conn.execute(text("CREATE INDEX IF NOT EXISTS idx_message_conversation_id ON message (conversation_id);"))
        except Exception as e:
            print(f"Warning: Could not create conversation_id index: {e}")

        # Index on created_at for chronological queries
        try:
            conn.execute(text("CREATE INDEX IF NOT EXISTS idx_tasks_created_at ON tasks (created_at);"))
            conn.execute(text("CREATE INDEX IF NOT EXISTS idx_conversation_created_at ON conversation (created_at);"))
            conn.execute(text("CREATE INDEX IF NOT EXISTS idx_message_created_at ON message (created_at);"))
        except Exception as e:
            print(f"Warning: Could not create timestamp indexes: {e}")

        conn.commit()

def verify_connection():
    """Verify that the database connection is working properly."""
    try:
        engine = get_engine()
        with engine.connect() as conn:
            # Test basic connectivity
            result = conn.execute(text("SELECT 1"))
            row = result.fetchone()
            if row and row[0] == 1:
                print("[OK] Database connection successful!")
                return True
            else:
                print("[FAIL] Database connection failed!")
                return False
    except Exception as e:
        print(f"[FAIL] Database connection failed: {e}")
        return False

def initialize_sample_data():
    """Initialize the database with sample data for testing."""
    try:
        with get_session_context() as session:
            # Check if sample data already exists
            existing_tasks = session.exec(select(Task)).first()
            if existing_tasks:
                print("[INFO] Sample data already exists, skipping initialization.")
                return

            print("[INFO] Initializing sample data...")

            # Create sample tasks
            sample_tasks = [
                TaskCreate(user_id="ziakhan", title="Buy groceries", description="Milk, eggs, bread"),
                TaskCreate(user_id="ziakhan", title="Call mom", description="Check on her health"),
                TaskCreate(user_id="ziakhan", title="Finish project", description="Complete the AI agent project"),
                TaskCreate(user_id="test_user", title="Learn Python", description="Study advanced Python concepts"),
                TaskCreate(user_id="test_user", title="Exercise", description="Go for a 30-minute run"),
            ]

            for task_data in sample_tasks:
                task = Task.from_orm(task_data) if hasattr(Task, 'from_orm') else Task(**task_data.dict())
                session.add(task)

            session.commit()
            print("[INFO] Sample data initialized successfully!")

    except Exception as e:
        print(f"[ERROR] Error initializing sample data: {e}")

def optimize_neon_connection_pool():
    """Provide connection pool recommendations for Neon PostgreSQL serverless."""
    print("\n[INFO] Neon PostgreSQL Connection Pool Recommendations:")
    print("   - pool_size: 20 (maintain 20 connections)")
    print("   - max_overflow: 30 (allow 30 additional connections)")
    print("   - pool_pre_ping: True (verify connections before use)")
    print("   - pool_recycle: 3600 (recycle connections every 1 hour)")
    print("   - pool_timeout: 30 (timeout for getting connection from pool)")
    print("   - SSL mode: require (enforce encrypted connections)")

def run_full_setup():
    """Run the complete database setup process."""
    print("[INFO] Starting Neon PostgreSQL setup for Todo AI Agent...")

    # Verify connection first
    if not verify_connection():
        print("[ERROR] Cannot proceed without database connection.")
        return False

    # Create tables and indexes
    create_db_and_tables()

    # Initialize sample data
    initialize_sample_data()

    # Show optimization tips
    optimize_neon_connection_pool()

    print("\n[SUCCESS] Neon PostgreSQL setup completed successfully!")
    print("[INFO] Next steps:")
    print("   1. Verify your DATABASE_URL in environment variables")
    print("   2. Run your application with 'python -m backend.main'")
    print("   3. Test the API endpoints")

    return True

if __name__ == "__main__":
    run_full_setup()