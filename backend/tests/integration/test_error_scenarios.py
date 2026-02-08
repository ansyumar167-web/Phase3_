"""
Integration test for "Complete non-existent task" scenario.
"""
import pytest
from fastapi.testclient import TestClient
from src.api.chat_endpoint import app


@pytest.fixture
def client():
    """Create a test client for the API."""
    return TestClient(app)


def test_complete_nonexistent_task_scenario(client):
    """Test the complete scenario when trying to complete a non-existent task."""
    test_user_id = "integration_test_user_nonexistent_task"

    # Attempt to complete a task that definitely doesn't exist
    # Using a very high ID that shouldn't exist
    response = client.post(f"/api/{test_user_id}/chat", json={
        "message": "Complete task 999999",
        "conversation_id": None
    })

    # Should return 200 OK (AI should handle this gracefully)
    assert response.status_code == 200

    # Parse the response
    data = response.json()
    assert "conversation_id" in data
    assert "response" in data
    assert "tool_calls" in data

    # The response should indicate that the task wasn't found or provide an error message
    response_text = data["response"].lower()
    assert any(keyword in response_text for keyword in [
        "not found", "doesn't exist", "error", "couldn't find",
        "invalid", "missing", "failed", "problem"
    ])


def test_delete_nonexistent_task_scenario(client):
    """Test the scenario when trying to delete a non-existent task."""
    test_user_id = "integration_test_user_delete_nonexistent"

    # Attempt to delete a task that doesn't exist
    response = client.post(f"/api/{test_user_id}/chat", json={
        "message": "Delete task 999999",
        "conversation_id": None
    })

    # Should return 200 OK (AI should handle this gracefully)
    assert response.status_code == 200

    # Parse the response
    data = response.json()
    assert "conversation_id" in data
    assert "response" in data
    assert "tool_calls" in data

    # The response should indicate an appropriate error or message
    response_text = data["response"].lower()
    assert any(keyword in response_text for keyword in [
        "not found", "doesn't exist", "error", "couldn't find",
        "invalid", "missing", "failed", "problem"
    ])


def test_update_nonexistent_task_scenario(client):
    """Test the scenario when trying to update a non-existent task."""
    test_user_id = "integration_test_user_update_nonexistent"

    # Attempt to update a task that doesn't exist
    response = client.post(f"/api/{test_user_id}/chat", json={
        "message": "Change task 999999 to new title",
        "conversation_id": None
    })

    # Should return 200 OK (AI should handle this gracefully)
    assert response.status_code == 200

    # Parse the response
    data = response.json()
    assert "conversation_id" in data
    assert "response" in data
    assert "tool_calls" in data

    # The response should indicate an appropriate error or message
    response_text = data["response"].lower()
    assert any(keyword in response_text for keyword in [
        "not found", "doesn't exist", "error", "couldn't find",
        "invalid", "missing", "failed", "problem"
    ])


def test_invalid_command_scenario(client):
    """Test handling of completely invalid or unrecognized commands."""
    test_user_id = "integration_test_user_invalid_cmd"

    # Send a command that doesn't make sense
    response = client.post(f"/api/{test_user_id}/chat", json={
        "message": "This is not a valid todo command at all",
        "conversation_id": None
    })

    # Should return 200 OK (AI should respond gracefully)
    assert response.status_code == 200

    # Parse the response
    data = response.json()
    assert "conversation_id" in data
    assert "response" in data
    assert "tool_calls" in data

    # The response should be a helpful message
    response_text = data["response"].lower()
    # Should provide help or clarification rather than crashing
    assert len(response_text) > 0  # Should have some response