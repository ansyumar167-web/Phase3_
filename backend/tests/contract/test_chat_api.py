"""
Contract test for POST /api/{user_id}/chat endpoint.
"""
import pytest
from fastapi.testclient import TestClient
from src.api.chat_endpoint import app


@pytest.fixture
def client():
    """Create a test client for the API."""
    return TestClient(app)


def test_chat_endpoint_exists(client):
    """Test that the chat endpoint exists and returns expected response structure."""
    # Test with a sample request
    response = client.post("/api/test_user/chat", json={
        "message": "Say hello",
        "conversation_id": None
    })

    # Should return 200 OK or appropriate error
    assert response.status_code in [200, 422]  # 422 if validation fails, 200 if success

    if response.status_code == 200:
        # If successful, check response structure
        data = response.json()
        assert "conversation_id" in data
        assert "response" in data
        assert "tool_calls" in data
        assert isinstance(data["tool_calls"], list)


def test_chat_endpoint_required_fields(client):
    """Test that the chat endpoint validates required fields."""
    # Test without required message field
    response = client.post("/api/test_user/chat", json={
        "conversation_id": None
    })

    # Should return 422 for validation error
    assert response.status_code == 422


def test_chat_endpoint_method_allowed(client):
    """Test that the chat endpoint only allows POST method."""
    response = client.get("/api/test_user/chat")
    # GET should not be allowed on this endpoint
    assert response.status_code in [404, 405]  # Not found or Method not allowed