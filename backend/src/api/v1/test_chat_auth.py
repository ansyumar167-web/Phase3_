"""
Tests for the chat endpoint authentication enforcement
"""
import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI
from jose import jwt
from datetime import datetime, timedelta
import os
from unittest.mock import patch
import sys
import os
# Add the src directory to the path so we can import from the project
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from .chat import router
from config import settings
from auth.config import SECRET_KEY, ALGORITHM

# Create a test app with the chat router
test_app = FastAPI()
test_app.include_router(router)

client = TestClient(test_app)


def create_test_token(user_id: str = "test_user", expires_delta: timedelta = None):
    """Helper function to create a test JWT token."""
    if expires_delta is None:
        expires_delta = timedelta(minutes=30)

    expire = datetime.utcnow() + expires_delta
    to_encode = {
        "sub": user_id,
        "user_id": user_id,
        "exp": expire.timestamp(),
        "iat": datetime.utcnow().timestamp()
    }
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def test_chat_endpoint_requires_authentication():
    """Test that the chat endpoint returns 401 when no authorization header is provided."""
    response = client.post("/api/v1/test_user/chat", json={"message": "Hello"})
    assert response.status_code == 401
    assert response.json()["detail"] == "No authorization header provided"


def test_chat_endpoint_invalid_token_type():
    """Test that the chat endpoint returns 401 when invalid token type is provided."""
    response = client.post(
        "/api/v1/test_user/chat",
        json={"message": "Hello"},
        headers={"Authorization": "InvalidType fake_token"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid token type"


def test_chat_endpoint_invalid_token_format():
    """Test that the chat endpoint returns 401 when authorization header format is invalid."""
    response = client.post(
        "/api/v1/test_user/chat",
        json={"message": "Hello"},
        headers={"Authorization": "invalid_format_without_space"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid authorization header format"


def test_chat_endpoint_invalid_token():
    """Test that the chat endpoint returns 401 when an invalid token is provided."""
    response = client.post(
        "/api/v1/test_user/chat",
        json={"message": "Hello"},
        headers={"Authorization": "Bearer invalid_token_here"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid or expired token"


def test_chat_endpoint_expired_token():
    """Test that the chat endpoint returns 401 when an expired token is provided."""
    expired_token = create_test_token(expires_delta=timedelta(seconds=-1))

    response = client.post(
        "/api/v1/test_user/chat",
        json={"message": "Hello"},
        headers={"Authorization": f"Bearer {expired_token}"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid or expired token"


def test_chat_endpoint_user_id_mismatch():
    """Test that the chat endpoint returns 403 when user_id in URL doesn't match authenticated user."""
    token = create_test_token(user_id="different_user")

    response = client.post(
        "/api/v1/test_user/chat",  # URL has test_user
        json={"message": "Hello"},
        headers={"Authorization": f"Bearer {token}"}  # Token is for different_user
    )
    assert response.status_code == 403
    assert "user_id does not match" in response.json()["detail"]


def test_chat_endpoint_valid_authentication():
    """Test that the chat endpoint accepts valid authentication."""
    token = create_test_token(user_id="test_user")

    # Since we're mocking the database calls, we expect this to fail at the DB level
    # but not at the authentication level
    with patch('database.session.get_session') as mock_session:
        # Create a mock session that raises an exception (to simulate DB connection issue)
        # but we're testing that authentication passes first
        mock_session.side_effect = Exception("DB connection failed")

        response = client.post(
            "/api/v1/test_user/chat",
            json={"message": "Hello"},
            headers={"Authorization": f"Bearer {token}"}
        )
        # Should fail at DB level, not authentication level
        assert response.status_code != 401
        assert response.status_code != 403


def test_chat_endpoint_valid_authentication_same_user():
    """Test that the chat endpoint works when user_id matches authenticated user."""
    token = create_test_token(user_id="same_user")

    # Mock the database operations to simulate successful processing
    with patch('database.session.get_session') as mock_get_session, \
         patch('services.conversation_service.ConversationService.create_conversation') as mock_create_conv, \
         patch('services.message_service.MessageService.add_message_to_conversation') as mock_add_msg, \
         patch('services.message_service.MessageService.get_latest_messages_for_conversation') as mock_get_msgs:

        # Mock a conversation object
        class MockConversation:
            id = 1

        mock_create_conv.return_value = MockConversation()
        mock_add_msg.return_value = None
        mock_get_msgs.return_value = []

        response = client.post(
            "/api/v1/same_user/chat",  # URL has same_user
            json={"message": "Hello"},
            headers={"Authorization": f"Bearer {token}"}  # Token is for same_user
        )

        # Should be successful (or at least pass authentication)
        assert response.status_code in [200, 500]  # 200 for success, 500 for DB error after auth
        if response.status_code == 500:
            # If it's a 500, it means authentication passed and it failed at DB level
            assert "processing" in response.json()["detail"]