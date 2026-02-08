from datetime import datetime
from sqlmodel import Field, SQLModel
from typing import Optional
from enum import Enum


class MessageRole(str, Enum):
    """Enumeration of possible message roles."""
    USER = "user"
    ASSISTANT = "assistant"


class MessageBase(SQLModel):
    """Base model for Message with common fields."""
    user_id: str = Field(min_length=1)
    conversation_id: int = Field(foreign_key="conversation.id")
    role: MessageRole
    content: str = Field(min_length=1, max_length=10000)


class Message(MessageBase, table=True):
    """Message model representing individual exchanges in a conversation."""
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class MessageRead(MessageBase):
    """Schema for reading Message data."""
    id: int
    created_at: datetime


class MessageCreate(MessageBase):
    """Schema for creating Message data."""
    user_id: str = Field(min_length=1)
    conversation_id: int
    role: MessageRole
    content: str = Field(min_length=1, max_length=10000)