from sqlmodel import Session, select
from typing import List, Optional
from ..models.message import Message, MessageCreate, MessageRead, MessageRole
from ..database.transaction_manager import TransactionManager
from datetime import datetime


class MessageService:
    """Service class for managing messages."""

    @staticmethod
    def add_message_to_conversation(
        session: Session,
        message_data: MessageCreate
    ) -> MessageRead:
        """Add a message to a conversation."""
        message = Message.model_validate(message_data)
        session.add(message)
        session.commit()
        session.refresh(message)
        return MessageRead.model_validate(message)

    @staticmethod
    def get_messages_for_conversation(
        session: Session,
        conversation_id: int,
        user_id: str
    ) -> List[MessageRead]:
        """Get all messages for a specific conversation."""
        # First, verify the conversation belongs to the user
        from .conversation_service import ConversationService
        conversation = ConversationService.get_conversation_by_id(session, conversation_id, user_id)
        if not conversation:
            return []

        # Get all messages for this conversation
        query = select(Message).where(Message.conversation_id == conversation_id)
        messages = session.exec(query).all()
        return [MessageRead.model_validate(msg) for msg in messages]

    @staticmethod
    def get_latest_messages_for_conversation(
        session: Session,
        conversation_id: int,
        user_id: str,
        limit: int = 10
    ) -> List[MessageRead]:
        """Get the latest messages for a specific conversation."""
        # First, verify the conversation belongs to the user
        from .conversation_service import ConversationService
        conversation = ConversationService.get_conversation_by_id(session, conversation_id, user_id)
        if not conversation:
            return []

        # Get the latest messages for this conversation
        query = (
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.desc())
            .limit(limit)
        )
        messages = session.exec(query).all()

        # Reverse the list to return messages in chronological order
        return [MessageRead.model_validate(msg) for msg in reversed(messages)]

    @staticmethod
    def get_message_by_id(
        session: Session,
        message_id: int,
        user_id: str
    ) -> Optional[MessageRead]:
        """Get a specific message by ID for a user."""
        message = session.get(Message, message_id)
        if message and message.user_id == user_id:
            return MessageRead.model_validate(message)
        return None

    @staticmethod
    def delete_message(
        session: Session,
        message_id: int,
        user_id: str
    ) -> bool:
        """Delete a message."""
        message = session.get(Message, message_id)
        if message and message.user_id == user_id:
            session.delete(message)
            session.commit()
            return True
        return False

    @staticmethod
    def get_user_messages(
        session: Session,
        user_id: str,
        limit: int = 50
    ) -> List[MessageRead]:
        """Get recent messages for a user across all conversations."""
        query = (
            select(Message)
            .where(Message.user_id == user_id)
            .order_by(Message.created_at.desc())
            .limit(limit)
        )
        messages = session.exec(query).all()
        return [MessageRead.model_validate(msg) for msg in messages]