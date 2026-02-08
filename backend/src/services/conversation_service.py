from sqlmodel import Session, select
from typing import List, Optional
from ..models.conversation import Conversation, ConversationCreate, ConversationRead
from ..models.message import Message, MessageCreate, MessageRead, MessageRole
from .task_service import TaskService
from ..database.transaction_manager import TransactionManager


class ConversationService:
    """Service class for managing conversations."""

    @staticmethod
    def create_conversation(session: Session, conv_data: ConversationCreate) -> ConversationRead:
        """Create a new conversation."""
        conversation = Conversation.model_validate(conv_data)
        session.add(conversation)
        session.commit()
        session.refresh(conversation)
        return ConversationRead.model_validate(conversation)

    @staticmethod
    def get_conversation_by_id(session: Session, conv_id: int, user_id: str) -> Optional[Conversation]:
        """Get a conversation by its ID for a specific user."""
        conversation = session.get(Conversation, conv_id)
        if conversation and conversation.user_id == user_id:
            return conversation
        return None

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
        conversation = session.get(Conversation, conversation_id)
        if not conversation or conversation.user_id != user_id:
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
        conversation = session.get(Conversation, conversation_id)
        if not conversation or conversation.user_id != user_id:
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
    def get_conversations_by_user(session: Session, user_id: str) -> List[ConversationRead]:
        """Get all conversations for a specific user."""
        query = select(Conversation).where(Conversation.user_id == user_id)
        conversations = session.exec(query).all()
        return [ConversationRead.model_validate(conv) for conv in conversations]

    @staticmethod
    def delete_conversation(session: Session, conv_id: int, user_id: str) -> bool:
        """Delete a conversation."""
        conversation = session.get(Conversation, conv_id)
        if conversation and conversation.user_id == user_id:
            # Also delete all messages in this conversation
            messages_query = select(Message).where(Message.conversation_id == conv_id)
            messages = session.exec(messages_query).all()
            for message in messages:
                session.delete(message)

            # Delete the conversation
            session.delete(conversation)
            session.commit()
            return True
        return False