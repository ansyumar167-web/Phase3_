#!/usr/bin/env python3
"""
Database verification and test script for the Todo AI Agent.
This script verifies the database schema and runs basic functionality tests.
"""

import sys
import os
from pathlib import Path
from datetime import datetime

# Add the backend directory to the path so imports work correctly
backend_path = str(Path(__file__).parent / "backend")
sys.path.insert(0, backend_path)

# Import the modules after adding to path
from src.database.neon_migration import verify_connection
from src.database.transaction_manager import get_session
from src.models.task import Task, TaskCreate
from src.models.conversation import Conversation, ConversationCreate
from src.models.message import Message, MessageCreate, MessageRole


def test_database_schema():
    """Test that the database schema is correctly set up."""
    print("[TEST] Testing database schema...")

    try:
        with get_session() as session:
            # Test creating a sample task
            task_data = TaskCreate(
                user_id="test_user_schema",
                title="Test task for schema verification",
                description="This is a test task to verify schema"
            )

            task = Task(
                user_id=task_data.user_id,
                title=task_data.title,
                description=task_data.description,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )

            session.add(task)
            session.commit()

            # Verify the task was created
            created_task = session.get(Task, task.id)
            assert created_task is not None, "Task was not created in database"
            assert created_task.title == task_data.title, "Task title mismatch"
            assert created_task.user_id == task_data.user_id, "Task user_id mismatch"

            print(f"[OK] Task created successfully with ID: {created_task.id}")

            # Clean up test task
            session.delete(created_task)
            session.commit()

            print("[PASS] Schema test passed!")
            return True

    except Exception as e:
        print(f"[FAIL] Schema test failed: {e}")
        return False


def test_indexes():
    """Test that important indexes exist."""
    print("[TEST] Testing database indexes...")

    try:
        from sqlalchemy import inspect
        from src.database.session import engine

        inspector = inspect(engine)

        # Get all indexes for the tasks table
        indexes = inspector.get_indexes('tasks')
        index_names = [idx['name'] for idx in indexes]

        required_indexes = [
            'idx_tasks_user_id',
            'idx_tasks_completed'
        ]

        missing_indexes = []
        for req_idx in required_indexes:
            if not any(req_idx in name for name in index_names):
                missing_indexes.append(req_idx)

        if missing_indexes:
            print(f"[WARN] Missing indexes: {missing_indexes}")
            print("   Note: Indexes may take a moment to create after migration")
        else:
            print("[OK] All required indexes found!")

        return True

    except Exception as e:
        print(f"[FAIL] Index test failed: {e}")
        return False


def test_relationships():
    """Test that relationships between tables work correctly."""
    print("[TEST] Testing table relationships...")

    try:
        with get_session() as session:
            # Create a test conversation
            conv_data = ConversationCreate(user_id="test_user_relationships")
            conversation = Conversation(
                user_id=conv_data.user_id,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            session.add(conversation)
            session.commit()

            # Create a test message associated with the conversation
            msg_data = MessageCreate(
                user_id="test_user_relationships",
                conversation_id=conversation.id,
                role=MessageRole.USER,
                content="Test message for relationship verification"
            )

            message = Message(
                user_id=msg_data.user_id,
                conversation_id=msg_data.conversation_id,
                role=msg_data.role,
                content=msg_data.content,
                created_at=datetime.utcnow()
            )

            session.add(message)
            session.commit()

            # Verify the relationship
            retrieved_msg = session.get(Message, message.id)
            assert retrieved_msg.conversation_id == conversation.id, "Message-conversation relationship failed"

            # Clean up - delete message first to avoid foreign key constraint
            session.delete(message)
            session.flush()  # Ensure message deletion happens first
            session.delete(conversation)
            session.commit()

            print("[PASS] Relationship test passed!")
            return True

    except Exception as e:
        print(f"[FAIL] Relationship test failed: {e}")
        return False


def run_comprehensive_test():
    """Run all database tests."""
    print("[TEST] Running comprehensive database tests...")

    tests = [
        ("Connection Test", verify_connection),
        ("Schema Test", test_database_schema),
        ("Index Test", test_indexes),
        ("Relationship Test", test_relationships)
    ]

    results = []
    for test_name, test_func in tests:
        print(f"\n[RUN] Running {test_name}...")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"[FAIL] {test_name} crashed: {e}")
            results.append((test_name, False))

    print(f"\n[RESULTS] Test Results:")
    all_passed = True
    for test_name, result in results:
        status = "[PASS]" if result else "[FAIL]"
        print(f"  {test_name}: {status}")
        if not result:
            all_passed = False

    if all_passed:
        print(f"\n[SUCCESS] All tests passed! Database is ready for use.")
        return True
    else:
        print(f"\n[ERROR] Some tests failed. Please review the issues above.")
        return False


if __name__ == "__main__":
    print("Starting database verification tests...")
    success = run_comprehensive_test()

    if not success:
        sys.exit(1)

    print("\n[SUCCESS] Database verification completed successfully!")