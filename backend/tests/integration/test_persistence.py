"""
Integration test for conversation persistence after server restart.
"""
import pytest
from fastapi.testclient import TestClient
from src.api.chat_endpoint import app
from src.database.session import get_session_direct
from src.services.conversation_service import ConversationService
from src.services.task_service import TaskService
from src.models.task import TaskCreate


def test_conversation_persistence_after_restart():
    """
    Test that after simulated server restart,
    users can continue their conversations and access their existing tasks without data loss.

    Note: Since we can't actually restart the server in a test, we simulate this by:
    1. Creating a conversation and tasks
    2. Verifying they exist in the database
    3. Creating a new database session (simulating a restart)
    4. Verifying the data still exists
    """
    test_user_id = "persistence_test_user"

    # Step 1: Create a conversation and some tasks
    session = get_session_direct()
    conversation_id = None

    try:
        # Create a conversation
        from src.models.conversation import ConversationCreate
        conv_data = ConversationCreate(user_id=test_user_id)
        conversation_service = ConversationService()
        conversation = conversation_service.create_conversation(session, conv_data)
        conversation_id = conversation.id

        # Add a task for the user
        task_service = TaskService()
        task = TaskCreate(user_id=test_user_id, title="Test persistence task", description="Task for persistence test")
        created_task = task_service.create_task(session, task)

        # Verify they were created
        assert conversation.user_id == test_user_id
        assert created_task.user_id == test_user_id
        assert created_task.title == "Test persistence task"

        # Commit and close session (simulating end of request)
        session.commit()
    finally:
        session.close()

    # Step 2: Simulate server restart by creating a new session
    new_session = get_session_direct()

    try:
        # Step 3: Verify conversation still exists
        retrieved_conv = conversation_service.get_conversation_by_id(new_session, conversation_id, test_user_id)
        assert retrieved_conv is not None
        assert retrieved_conv.id == conversation_id
        assert retrieved_conv.user_id == test_user_id

        # Step 4: Verify task still exists
        tasks = task_service.get_tasks_by_user(new_session, test_user_id)
        user_tasks = [t for t in tasks if t.title == "Test persistence task"]
        assert len(user_tasks) >= 1
        assert user_tasks[0].user_id == test_user_id
        assert not user_tasks[0].completed  # Should still be pending

        print("✓ Conversation and task persistence verified after simulated restart")

    finally:
        # Clean up: Remove test data
        task_service = TaskService()
        for task in tasks:
            if task.title == "Test persistence task":
                task_service.delete_task(new_session, task.id, test_user_id)
        new_session.close()


def test_multiple_conversations_persistence():
    """
    Test that multiple conversations for the same user persist correctly.
    """
    test_user_id = "multi_conv_persistence_test"

    # Create multiple conversations
    session = get_session_direct()
    conversation_ids = []

    try:
        conversation_service = ConversationService()

        # Create 3 conversations
        for i in range(3):
            conv_data = ConversationCreate(user_id=test_user_id)
            conversation = conversation_service.create_conversation(session, conv_data)
            conversation_ids.append(conversation.id)

        # Verify all were created
        assert len(conversation_ids) == 3
        assert len(set(conversation_ids)) == 3  # All should be unique

        session.commit()
    finally:
        session.close()

    # Simulate restart and verify all conversations still exist
    new_session = get_session_direct()

    try:
        for conv_id in conversation_ids:
            retrieved = conversation_service.get_conversation_by_id(new_session, conv_id, test_user_id)
            assert retrieved is not None
            assert retrieved.id == conv_id
            assert retrieved.user_id == test_user_id

        print("✓ Multiple conversations persisted correctly after simulated restart")

    finally:
        new_session.close()


if __name__ == "__main__":
    test_conversation_persistence_after_restart()
    test_multiple_conversations_persistence()
    print("All persistence tests passed!")