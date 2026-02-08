from datetime import datetime
from sqlmodel import Field, SQLModel
from typing import Optional


class ConversationBase(SQLModel):
    """Base model for Conversation with common fields."""
    user_id: str = Field(min_length=1)


class Conversation(ConversationBase, table=True):
    """Conversation model representing a user's conversation thread."""
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class ConversationRead(ConversationBase):
    """Schema for reading Conversation data."""
    id: int
    created_at: datetime
    updated_at: datetime


class ConversationCreate(ConversationBase):
    """Schema for creating Conversation data."""
    user_id: str = Field(min_length=1)