"""
Tests for the chat endpoint successful message transmission and response
"""
import sys
import os
# Add the src directory to the path so we can import from the project
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI
from jose import jwt
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch
from .chat import router, ChatResponse
from auth.config import SECRET_KEY, ALGORITHM
from models.conversation import ConversationCreate, Conversation
from models.message import MessageCreate, Message
from models.message import MessageRole

# Create a test app with the chat router
test_app = FastAPI()
test_app.include_router(router)

client = TestClient(test_app)


def create_test_token(user_id: str = "test_user"):
    """Helper function to create a test JWT token."""
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode = {
        "sub": user_id,
        "user_id": user_id,
        "exp": expire.timestamp(),
        "iat": datetime.utcnow().timestamp()
    }
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def test_successful_hello_message():
    """Test successful message transmission with hello greeting."""
    token = create_test_token(user_id="test_user")

    # Mock all database operations
    with patch('database.session.get_session') as mock_get_session:
        # Create a mock session
        mock_session = MagicMock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        mock_get_session.return_value.__exit__.return_value = None

        # Mock conversation creation
        mock_conversation = MagicMock(spec=Conversation)
        mock_conversation.id = 1
        mock_session.add.return_value = None
        mock_session.commit.return_value = None
        mock_session.refresh.return_value = None

        # Mock the conversation creation method
        with patch('services.conversation_service.ConversationService.create_conversation') as mock_create_conv:
            mock_create_conv.return_value = mock_conversation

            # Mock the message service
            with patch('services.message_service.MessageService.add_message_to_conversation') as mock_add_msg, \
                 patch('services.message_service.MessageService.get_latest_messages_for_conversation') as mock_get_msgs:

                mock_get_msgs.return_value = []

                response = client.post(
                    "/api/v1/test_user/chat",
                    json={"message": "Hello, how are you?"},
                    headers={"Authorization": f"Bearer {token}"}
                )

                assert response.status_code == 200
                data = response.json()
                assert "conversation_id" in data
                assert "response" in data
                assert "tool_calls" in data
                assert isinstance(data["tool_calls"], list)
                assert "Hello!" in data["response"] or "received your message" in data["response"]


def test_successful_goodbye_message():
    """Test successful message transmission with goodbye message."""
    token = create_test_token(user_id="test_user")

    # Mock all database operations
    with patch('database.session.get_session') as mock_get_session:
        mock_session = MagicMock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        mock_get_session.return_value.__exit__.return_value = None

        mock_conversation = MagicMock(spec=Conversation)
        mock_conversation.id = 1
        mock_session.add.return_value = None
        mock_session.commit.return_value = None
        mock_session.refresh.return_value = None

        with patch('services.conversation_service.ConversationService.create_conversation') as mock_create_conv:
            mock_create_conv.return_value = mock_conversation

            with patch('services.message_service.MessageService.add_message_to_conversation') as mock_add_msg, \
                 patch('services.message_service.MessageService.get_latest_messages_for_conversation') as mock_get_msgs:

                mock_get_msgs.return_value = []

                response = client.post(
                    "/api/v1/test_user/chat",
                    json={"message": "Goodbye, see you later!"},
                    headers={"Authorization": f"Bearer {token}"}
                )

                assert response.status_code == 200
                data = response.json()
                assert "conversation_id" in data
                assert "response" in data
                assert "tool_calls" in data
                assert "Goodbye!" in data["response"] or "Thanks for chatting" in data["response"]


def test_successful_generic_message():
    """Test successful message transmission with generic message."""
    token = create_test_token(user_id="test_user")

    # Mock all database operations
    with patch('database.session.get_session') as mock_get_session:
        mock_session = MagicMock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        mock_get_session.return_value.__exit__.return_value = None

        mock_conversation = MagicMock(spec=Conversation)
        mock_conversation.id = 1
        mock_session.add.return_value = None
        mock_session.commit.return_value = None
        mock_session.refresh.return_value = None

        with patch('services.conversation_service.ConversationService.create_conversation') as mock_create_conv:
            mock_create_conv.return_value = mock_conversation

            with patch('services.message_service.MessageService.add_message_to_conversation') as mock_add_msg, \
                 patch('services.message_service.MessageService.get_latest_messages_for_conversation') as mock_get_msgs:

                mock_get_msgs.return_value = []

                response = client.post(
                    "/api/v1/test_user/chat",
                    json={"message": "This is a test message"},
                    headers={"Authorization": f"Bearer {token}"}
                )

                assert response.status_code == 200
                data = response.json()
                assert "conversation_id" in data
                assert "response" in data
                assert "tool_calls" in data
                assert "This is a mock AI response" in data["response"]


def test_message_with_existing_conversation():
    """Test successful message transmission with existing conversation."""
    token = create_test_token(user_id="test_user")

    # Mock all database operations
    with patch('database.session.get_session') as mock_get_session:
        mock_session = MagicMock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        mock_get_session.return_value.__exit__.return_value = None

        mock_conversation = MagicMock(spec=Conversation)
        mock_conversation.id = 5
        mock_session.add.return_value = None
        mock_session.commit.return_value = None
        mock_session.refresh.return_value = None

        # Mock getting an existing conversation
        with patch('services.conversation_service.ConversationService.get_conversation_by_id') as mock_get_conv:
            mock_get_conv.return_value = mock_conversation

            with patch('services.message_service.MessageService.add_message_to_conversation') as mock_add_msg, \
                 patch('services.message_service.MessageService.get_latest_messages_for_conversation') as mock_get_msgs:

                mock_get_msgs.return_value = []

                response = client.post(
                    "/api/v1/test_user/chat",
                    json={"message": "Continuing the conversation", "conversation_id": 5},
                    headers={"Authorization": f"Bearer {token}"}
                )

                assert response.status_code == 200
                data = response.json()
                assert data["conversation_id"] == 5
                assert "response" in data
                assert "tool_calls" in data


def test_empty_message_validation():
    """Test that empty messages are handled appropriately."""
    token = create_test_token(user_id="test_user")

    # Mock all database operations
    with patch('database.session.get_session') as mock_get_session:
        mock_session = MagicMock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        mock_get_session.return_value.__exit__.return_value = None

        mock_conversation = MagicMock(spec=Conversation)
        mock_conversation.id = 1
        mock_session.add.return_value = None
        mock_session.commit.return_value = None
        mock_session.refresh.return_value = None

        with patch('services.conversation_service.ConversationService.create_conversation') as mock_create_conv:
            mock_create_conv.return_value = mock_conversation

            with patch('services.message_service.MessageService.add_message_to_conversation') as mock_add_msg, \
                 patch('services.message_service.MessageService.get_latest_messages_for_conversation') as mock_get_msgs:

                mock_get_msgs.return_value = []

                response = client.post(
                    "/api/v1/test_user/chat",
                    json={"message": ""},  # Empty message
                    headers={"Authorization": f"Bearer {token}"}
                )

                # Should return 422 for validation error due to empty message
                assert response.status_code == 422


def test_missing_message_field():
    """Test that missing message field is handled appropriately."""
    token = create_test_token(user_id="test_user")

    response = client.post(
        "/api/v1/test_user/chat",
        json={},  # Missing message field
        headers={"Authorization": f"Bearer {token}"}
    )

    # Should return 422 for validation error due to missing required field
    assert response.status_code == 422