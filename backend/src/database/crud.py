from typing import List, Optional
from sqlmodel import select, func
from .models import User, Conversation, Message, Task
from .async_session import get_async_session
from sqlalchemy.exc import IntegrityError
from contextlib import asynccontextmanager


class UserCRUD:
    @staticmethod
    async def create_user(user: User) -> User:
        """Create a new user."""
        async with get_async_session() as session:
            session.add(user)
            await session.commit()
            await session.refresh(user)
            return user

    @staticmethod
    async def get_user_by_id(user_id: int) -> Optional[User]:
        """Get user by ID."""
        async with get_async_session() as session:
            statement = select(User).where(User.id == user_id)
            result = await session.exec(statement)
            return result.first()

    @staticmethod
    async def get_user_by_email(email: str) -> Optional[User]:
        """Get user by email."""
        async with get_async_session() as session:
            statement = select(User).where(User.email == email)
            result = await session.exec(statement)
            return result.first()

    @staticmethod
    async def get_user_by_username(username: str) -> Optional[User]:
        """Get user by username."""
        async with get_async_session() as session:
            statement = select(User).where(User.username == username)
            result = await session.exec(statement)
            return result.first()

    @staticmethod
    async def update_user(user_id: int, **kwargs) -> Optional[User]:
        """Update user details."""
        async with get_async_session() as session:
            statement = select(User).where(User.id == user_id)
            result = await session.exec(statement)
            user = result.first()

            if not user:
                return None

            for key, value in kwargs.items():
                setattr(user, key, value)

            await session.commit()
            await session.refresh(user)
            return user

    @staticmethod
    async def delete_user(user_id: int) -> bool:
        """Delete a user."""
        async with get_async_session() as session:
            statement = select(User).where(User.id == user_id)
            result = await session.exec(statement)
            user = result.first()

            if not user:
                return False

            await session.delete(user)
            await session.commit()
            return True


class ConversationCRUD:
    @staticmethod
    async def create_conversation(conversation: Conversation) -> Conversation:
        """Create a new conversation."""
        async with get_async_session() as session:
            session.add(conversation)
            await session.commit()
            await session.refresh(conversation)
            return conversation

    @staticmethod
    async def get_conversation_by_id(conversation_id: int) -> Optional[Conversation]:
        """Get conversation by ID."""
        async with get_async_session() as session:
            statement = select(Conversation).where(Conversation.id == conversation_id)
            result = await session.exec(statement)
            return result.first()

    @staticmethod
    async def get_conversations_by_user(user_id: int) -> List[Conversation]:
        """Get all conversations for a user."""
        async with get_async_session() as session:
            statement = select(Conversation).where(Conversation.user_id == user_id).order_by(Conversation.created_at.desc())
            result = await session.exec(statement)
            return result.all()

    @staticmethod
    async def update_conversation(conversation_id: int, **kwargs) -> Optional[Conversation]:
        """Update conversation details."""
        async with get_async_session() as session:
            statement = select(Conversation).where(Conversation.id == conversation_id)
            result = await session.exec(statement)
            conversation = result.first()

            if not conversation:
                return None

            for key, value in kwargs.items():
                setattr(conversation, key, value)

            await session.commit()
            await session.refresh(conversation)
            return conversation

    @staticmethod
    async def delete_conversation(conversation_id: int) -> bool:
        """Delete a conversation and all associated messages."""
        async with get_async_session() as session:
            # Delete associated messages first due to foreign key constraint
            from .crud import MessageCRUD
            await MessageCRUD.delete_messages_by_conversation(conversation_id)

            statement = select(Conversation).where(Conversation.id == conversation_id)
            result = await session.exec(statement)
            conversation = result.first()

            if not conversation:
                return False

            await session.delete(conversation)
            await session.commit()
            return True


class MessageCRUD:
    @staticmethod
    async def create_message(message: Message) -> Message:
        """Create a new message."""
        async with get_async_session() as session:
            session.add(message)
            await session.commit()
            await session.refresh(message)
            return message

    @staticmethod
    async def get_message_by_id(message_id: int) -> Optional[Message]:
        """Get message by ID."""
        async with get_async_session() as session:
            statement = select(Message).where(Message.id == message_id)
            result = await session.exec(statement)
            return result.first()

    @staticmethod
    async def get_messages_by_conversation(conversation_id: int, limit: int = 100) -> List[Message]:
        """Get messages for a conversation, ordered by creation time."""
        async with get_async_session() as session:
            statement = select(Message).where(
                Message.conversation_id == conversation_id
            ).order_by(Message.created_at.asc()).limit(limit)
            result = await session.exec(statement)
            return result.all()

    @staticmethod
    async def get_messages_by_user(user_id: int, limit: int = 100) -> List[Message]:
        """Get messages for a user, ordered by creation time."""
        async with get_async_session() as session:
            statement = select(Message).where(
                Message.user_id == user_id
            ).order_by(Message.created_at.desc()).limit(limit)
            result = await session.exec(statement)
            return result.all()

    @staticmethod
    async def update_message(message_id: int, **kwargs) -> Optional[Message]:
        """Update message details."""
        async with get_async_session() as session:
            statement = select(Message).where(Message.id == message_id)
            result = await session.exec(statement)
            message = result.first()

            if not message:
                return None

            for key, value in kwargs.items():
                setattr(message, key, value)

            await session.commit()
            await session.refresh(message)
            return message

    @staticmethod
    async def delete_message(message_id: int) -> bool:
        """Delete a message."""
        async with get_async_session() as session:
            statement = select(Message).where(Message.id == message_id)
            result = await session.exec(statement)
            message = result.first()

            if not message:
                return False

            await session.delete(message)
            await session.commit()
            return True

    @staticmethod
    async def delete_messages_by_conversation(conversation_id: int) -> int:
        """Delete all messages in a conversation."""
        async with get_async_session() as session:
            from sqlalchemy import delete
            statement = delete(Message).where(Message.conversation_id == conversation_id)
            result = await session.exec(statement)
            await session.commit()
            return result.rowcount


class TaskCRUD:
    @staticmethod
    async def create_task(task: Task) -> Task:
        """Create a new task."""
        async with get_async_session() as session:
            session.add(task)
            await session.commit()
            await session.refresh(task)
            return task

    @staticmethod
    async def get_task_by_id(task_id: int) -> Optional[Task]:
        """Get task by ID."""
        async with get_async_session() as session:
            statement = select(Task).where(Task.id == task_id)
            result = await session.exec(statement)
            return result.first()

    @staticmethod
    async def get_tasks_by_user(user_id: str, completed: Optional[bool] = None) -> List[Task]:
        """Get tasks for a user, optionally filtered by completion status."""
        async with get_async_session() as session:
            statement = select(Task).where(Task.user_id == user_id)
            if completed is not None:
                statement = statement.where(Task.completed == completed)
            statement = statement.order_by(Task.created_at.desc())
            result = await session.exec(statement)
            return result.all()

    @staticmethod
    async def get_tasks_by_conversation(conversation_id: int) -> List[Task]:
        """Get tasks associated with a conversation."""
        async with get_async_session() as session:
            statement = select(Task).where(
                Task.conversation_id == conversation_id
            ).order_by(Task.created_at.desc())
            result = await session.exec(statement)
            return result.all()

    @staticmethod
    async def update_task(task_id: int, **kwargs) -> Optional[Task]:
        """Update task details."""
        async with get_async_session() as session:
            statement = select(Task).where(Task.id == task_id)
            result = await session.exec(statement)
            task = result.first()

            if not task:
                return None

            for key, value in kwargs.items():
                setattr(task, key, value)

            await session.commit()
            await session.refresh(task)
            return task

    @staticmethod
    async def delete_task(task_id: int) -> bool:
        """Delete a task."""
        async with get_async_session() as session:
            statement = select(Task).where(Task.id == task_id)
            result = await session.exec(statement)
            task = result.first()

            if not task:
                return False

            await session.delete(task)
            await session.commit()
            return True

    @staticmethod
    async def complete_task(task_id: int) -> Optional[Task]:
        """Mark a task as completed."""
        return await TaskCRUD.update_task(task_id, completed=True)

    @staticmethod
    async def delete_task_permanently(task_id: int) -> Optional[Task]:
        """Mark a task as deleted."""
        # Since we're using a boolean completed field, we'll delete permanently instead
        async with get_async_session() as session:
            statement = select(Task).where(Task.id == task_id)
            result = await session.exec(statement)
            task = result.first()

            if not task:
                return None

            await session.delete(task)
            await session.commit()
            return task

    @staticmethod
    async def get_task_count_by_user(user_id: str, completed: Optional[bool] = None) -> int:
        """Get count of tasks for a user, optionally filtered by completion status."""
        async with get_async_session() as session:
            statement = select(func.count(Task.id)).where(Task.user_id == user_id)
            if completed is not None:
                statement = statement.where(Task.completed == completed)
            result = await session.exec(statement)
            return result.one()