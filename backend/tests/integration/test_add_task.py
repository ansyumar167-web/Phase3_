"""
Integration test for "Add a task" user journey.
"""
import pytest
from fastapi.testclient import TestClient
from src.api.chat_endpoint import app
from src.database.session import get_session_direct
from src.services.task_service import TaskService


@pytest.fixture
def client():
    """Create a test client for the API."""
    return TestClient(app)


def test_add_task_integration(client):
    """Test the complete 'Add a task' user journey."""
    # Use a unique user ID for this test
    test_user_id = "integration_test_user_add_task"

    # Send request to add a task
    response = client.post(f"/api/{test_user_id}/chat", json={
        "message": "Add a task to buy groceries",
        "conversation_id": None
    })

    # Should return 200 OK
    assert response.status_code == 200

    # Parse the response
    data = response.json()
    assert "conversation_id" in data
    assert "response" in data
    assert "tool_calls" in data

    # Verify that add_task was called
    assert "add_task" in data["tool_calls"]

    # Verify that the response is appropriate
    assert "buy groceries" in data["response"].lower() or "added" in data["response"].lower()

    # Verify the task was actually created in the database
    session = get_session_direct()
    try:
        task_service = TaskService()
        tasks = task_service.get_tasks_by_user(session, test_user_id)

        # Should have at least one task with the right title
        added_tasks = [t for t in tasks if "buy groceries" in t.title.lower()]
        assert len(added_tasks) >= 1

        # Verify the task properties
        task = added_tasks[0]
        assert task.user_id == test_user_id
        assert not task.completed  # New tasks should not be completed by default
    finally:
        session.close()


def test_add_task_with_description_integration(client):
    """Test adding a task with a description."""
    test_user_id = "integration_test_user_desc"

    response = client.post(f"/api/{test_user_id}/chat", json={
        "message": "Add a task to call mom with description Remember to wish her happy birthday",
        "conversation_id": None
    })

    assert response.status_code == 200
    data = response.json()

    # Verify response structure
    assert "conversation_id" in data
    assert "response" in data
    assert "tool_calls" in data

    # Verify that add_task was called
    assert "add_task" in data["tool_calls"]

    # Verify the task was created with description
    session = get_session_direct()
    try:
        task_service = TaskService()
        tasks = task_service.get_tasks_by_user(session, test_user_id)

        # Look for a task that includes "call mom" in the title
        added_tasks = [t for t in tasks if "call mom" in t.title.lower()]
        assert len(added_tasks) >= 1
    finally:
        session.close()