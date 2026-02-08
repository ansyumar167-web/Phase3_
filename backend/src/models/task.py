from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Task(SQLModel, table=True):
    """
    Task model representing a user's task in the todo list.

    Fields:
    - user_id: The ID of the user who owns this task
    - id: Auto-generated unique identifier for the task
    - title: The title of the task (required)
    - description: Optional description of the task
    - completed: Boolean indicating if the task is completed (default: False)
    - created_at: Timestamp when the task was created
    - updated_at: Timestamp when the task was last updated
    """
    __tablename__ = "tasks"
    __table_args__ = {'extend_existing': True}

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)  # Using string for user_id as per spec
    title: str = Field(max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class TaskCreate(SQLModel):
    """Schema for creating a new task"""
    user_id: str
    title: str
    description: Optional[str] = None


class TaskUpdate(SQLModel):
    """Schema for updating an existing task"""
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


class TaskResponse(SQLModel):
    """Schema for returning task information"""
    id: int
    user_id: str
    title: str
    description: Optional[str] = None
    completed: bool
    created_at: datetime
    updated_at: datetime