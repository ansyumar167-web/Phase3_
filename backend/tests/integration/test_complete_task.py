"""
Integration test for "Complete task" user journey.
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


def test_complete_task_by_id_integration(client):
    """Test the complete task journey by specifying a task ID."""
    test_user_id = "integration_test_user_complete_by_id"

    # First, add a task
    session = get_session_direct()
    try:
        task_service = TaskService()
        task = TaskCreate(user_id=test_user_id, title="Buy groceries", description="Milk and eggs")
        created_task = task_service.create_task(session, task)
        task_id = created_task.id
    finally:
        session.close()

    # Now complete the task by ID
    response = client.post(f"/api/{test_user_id}/chat", json={
        "message": f"Mark task {task_id} as complete",
        "conversation_id": None
    })

    # Should return 200 OK
    assert response.status_code == 200

    # Parse the response
    data = response.json()
    assert "conversation_id" in data
    assert "response" in data
    assert "tool_calls" in data

    # Verify that complete_task was called
    assert "complete_task" in data["tool_calls"]

    # Verify that the response confirms completion
    assert "complete" in data["response"].lower() or "done" in data["response"].lower()

    # Verify the task was actually marked as completed in the database
    session = get_session_direct()
    try:
        task_service = TaskService()
        retrieved_task = task_service.get_task_by_id(session, task_id, test_user_id)

        assert retrieved_task is not None
        assert retrieved_task.completed is True
    finally:
        session.close()


def test_complete_task_by_description_integration(client):
    """Test completing a task by description (if the AI supports this)."""
    test_user_id = "integration_test_user_complete_by_desc"

    # First, add a task
    session = get_session_direct()
    try:
        task_service = TaskService()
        task = TaskCreate(user_id=test_user_id, title="Call mom", description="Wish her happy birthday")
        created_task = task_service.create_task(session, task)
        task_id = created_task.id
    finally:
        session.close()

    # Now try to complete the task by description
    response = client.post(f"/api/{test_user_id}/chat", json={
        "message": "Complete the task about calling mom",
        "conversation_id": None
    })

    # Should return 200 OK (or handle gracefully if not implemented)
    assert response.status_code == 200

    # Parse the response
    data = response.json()
    assert "conversation_id" in data
    assert "response" in data
    assert "tool_calls" in data

    # The AI might call list_tasks first to identify the task, then complete_task
    tool_calls = data["tool_calls"]
    assert any(call in ["list_tasks", "complete_task"] for call in tool_calls)


def test_complete_nonexistent_task_integration(client):
    """Test attempting to complete a task that doesn't exist."""
    test_user_id = "integration_test_user_complete_nonexistent"

    # Try to complete a task with an invalid ID
    response = client.post(f"/api/{test_user_id}/chat", json={
        "message": "Mark task 99999 as complete",
        "conversation_id": None
    })

    # Should return 200 OK (the AI should handle this gracefully)
    assert response.status_code == 200

    # Parse the response
    data = response.json()
    assert "conversation_id" in data
    assert "response" in data
    assert "tool_calls" in data

    # The response should indicate that the task wasn't found
    response_text = data["response"].lower()
    assert "not found" in response_text or "doesn't exist" in response_text or "error" in response_text