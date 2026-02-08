"""
Integration test for "Show all tasks" user journey.
"""
import pytest
from fastapi.testclient import TestClient
from src.api.chat_endpoint import app
from src.database.session import get_session_direct
from src.services.task_service import TaskService
from src.models.task import TaskCreate


@pytest.fixture
def client():
    """Create a test client for the API."""
    return TestClient(app)


def test_list_all_tasks_integration(client):
    """Test the complete 'Show all tasks' user journey."""
    test_user_id = "integration_test_user_list_all"

    # First, add a few tasks to the user's list
    session = get_session_direct()
    try:
        task_service = TaskService()

        # Add a couple of tasks
        task1 = TaskCreate(user_id=test_user_id, title="Buy groceries", description="Milk and eggs")
        task2 = TaskCreate(user_id=test_user_id, title="Call mom", description="Wish her happy birthday")

        task_service.create_task(session, task1)
        task_service.create_task(session, task2)
    finally:
        session.close()

    # Now ask to see all tasks
    response = client.post(f"/api/{test_user_id}/chat", json={
        "message": "Show me all my tasks",
        "conversation_id": None
    })

    # Should return 200 OK
    assert response.status_code == 200

    # Parse the response
    data = response.json()
    assert "conversation_id" in data
    assert "response" in data
    assert "tool_calls" in data

    # Verify that list_tasks was called
    assert "list_tasks" in data["tool_calls"]

    # Verify that the response mentions tasks
    assert "task" in data["response"].lower()


def test_list_pending_tasks_integration(client):
    """Test the 'What's pending?' user journey."""
    test_user_id = "integration_test_user_list_pending"

    # Add some tasks and complete one
    session = get_session_direct()
    try:
        task_service = TaskService()

        # Add a couple of tasks
        task1 = TaskCreate(user_id=test_user_id, title="Buy groceries", description="Milk and eggs")
        task2 = TaskCreate(user_id=test_user_id, title="Call mom", description="Wish her happy birthday")

        created_task1 = task_service.create_task(session, task1)
        created_task2 = task_service.create_task(session, task2)

        # Complete one of the tasks
        task_service.complete_task(session, created_task2.id, test_user_id)
    finally:
        session.close()

    # Now ask to see pending tasks
    response = client.post(f"/api/{test_user_id}/chat", json={
        "message": "What's pending?",
        "conversation_id": None
    })

    # Should return 200 OK
    assert response.status_code == 200

    # Parse the response
    data = response.json()
    assert "conversation_id" in data
    assert "response" in data
    assert "tool_calls" in data

    # Verify that list_tasks was called
    assert "list_tasks" in data["tool_calls"]

    # Response should mention pending tasks
    assert "pending" in data["response"].lower() or "task" in data["response"].lower()


def test_list_empty_tasks_integration(client):
    """Test the 'Show all tasks' journey when user has no tasks."""
    test_user_id = "integration_test_user_empty_list"

    # Ask to see all tasks when none exist
    response = client.post(f"/api/{test_user_id}/chat", json={
        "message": "Show me all my tasks",
        "conversation_id": None
    })

    # Should return 200 OK
    assert response.status_code == 200

    # Parse the response
    data = response.json()
    assert "conversation_id" in data
    assert "response" in data
    assert "tool_calls" in data

    # Verify that list_tasks was called
    assert "list_tasks" in data["tool_calls"]

    # Response should indicate that there are no tasks
    response_text = data["response"].lower()
    assert "no" in response_text or "empty" in response_text or "0" in response_text or "none" in response_text