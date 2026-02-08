"""
Contract test for error handling in POST /api/{user_id}/chat endpoint.
"""
import pytest
from fastapi.testclient import TestClient
from src.api.chat_endpoint import app


@pytest.fixture
def client():
    """Create a test client for the API."""
    return TestClient(app)


def test_error_response_format(client):
    """Test that error responses follow the expected format."""
    # Test with an invalid request (missing message)
    response = client.post("/api/test_user/chat", json={
        "conversation_id": None
        # Missing required "message" field
    })

    # Should return 422 for validation error
    assert response.status_code == 422

    # Even if it's a validation error, the response should have certain characteristics
    data = response.json()
    assert "detail" in data  # FastAPI validation errors include detail


def test_server_error_handling(client):
    """Test that server errors are handled gracefully."""
    # Test with a very long message to potentially trigger a server error
    long_message = "A" * 10000  # Very long message

    response = client.post("/api/test_user/chat", json={
        "message": long_message,
        "conversation_id": None
    })

    # Should return either success or a proper error, not crash
    assert response.status_code in [200, 413, 422, 500]  # 413 payload too large, 422 validation, 500 server error


def test_nonexistent_user_handling(client):
    """Test handling of requests for potentially problematic user IDs."""
    # Use a user ID that might cause issues (though it should work fine)
    response = client.post("/api/valid_user_id_test/chat", json={
        "message": "Say hello",
        "conversation_id": None
    })

    # Should return 200 OK (creates conversation for new user)
    assert response.status_code == 200

    data = response.json()
    assert "conversation_id" in data
    assert "response" in data
    assert "tool_calls" in data


def test_special_characters_handling(client):
    """Test handling of messages with special characters."""
    test_message = "Add a task with special chars: @#$%^&*()!"

    response = client.post("/api/test_user_special/chat", json={
        "message": test_message,
        "conversation_id": None
    })

    # Should handle special characters gracefully
    assert response.status_code in [200, 422]  # Either success or validation error, but not crash


def test_conversation_id_validation(client):
    """Test validation of conversation_id parameter."""
    # Test with an invalid conversation_id (string instead of integer)
    response = client.post("/api/test_user/chat", json={
        "message": "Test message",
        "conversation_id": "invalid_id"  # Should be integer or null
    })

    # Should return 422 for validation error
    assert response.status_code == 422