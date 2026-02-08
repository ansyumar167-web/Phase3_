from typing import List, Optional
from sqlmodel import select, Session
from ..database.models import Task as DBTask
from ..models.task import TaskCreate, TaskUpdate, TaskResponse
from datetime import datetime
from ..database.session import get_session_context


class TaskService:
    """
    Service class for managing tasks with CRUD operations.
    """

    @staticmethod
    def create_task(task_data: TaskCreate) -> TaskResponse:
        """
        Create a new task.

        Args:
            task_data: TaskCreate object containing task information

        Returns:
            TaskResponse object with the created task details
        """
        with get_session_context() as session:
            task = DBTask(
                user_id=task_data.user_id,
                title=task_data.title,
                description=task_data.description,
                completed=False,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            session.add(task)
            session.commit()
            session.refresh(task)

            return TaskResponse(
                id=task.id,
                user_id=task.user_id,
                title=task.title,
                description=task.description,
                completed=task.completed,
                created_at=task.created_at,
                updated_at=task.updated_at
            )

    @staticmethod
    def get_tasks(user_id: str, status: Optional[str] = None) -> List[TaskResponse]:
        """
        Retrieve tasks for a specific user with optional status filter.

        Args:
            user_id: The ID of the user whose tasks to retrieve
            status: Optional filter for task status ("all", "pending", "completed")

        Returns:
            List of TaskResponse objects
        """
        with get_session_context() as session:
            query = select(DBTask).where(DBTask.user_id == user_id)

            if status and status != "all":
                if status == "completed":
                    query = query.where(DBTask.completed == True)
                elif status == "pending":
                    query = query.where(DBTask.completed == False)

            tasks = session.exec(query).all()

            return [
                TaskResponse(
                    id=task.id,
                    user_id=task.user_id,
                    title=task.title,
                    description=task.description,
                    completed=task.completed,
                    created_at=task.created_at,
                    updated_at=task.updated_at
                )
                for task in tasks
            ]

    @staticmethod
    def get_task_by_id(user_id: str, task_id: int) -> Optional[TaskResponse]:
        """
        Retrieve a specific task by user ID and task ID.

        Args:
            user_id: The ID of the user who owns the task
            task_id: The ID of the task to retrieve

        Returns:
            TaskResponse object or None if not found
        """
        with get_session_context() as session:
            task = session.get(DBTask, task_id)
            if task and task.user_id == user_id:
                return TaskResponse(
                    id=task.id,
                    user_id=task.user_id,
                    title=task.title,
                    description=task.description,
                    completed=task.completed,
                    created_at=task.created_at,
                    updated_at=task.updated_at
                )
            return None

    @staticmethod
    def update_task(user_id: str, task_id: int, task_update: TaskUpdate) -> Optional[TaskResponse]:
        """
        Update an existing task.

        Args:
            user_id: The ID of the user who owns the task
            task_id: The ID of the task to update
            task_update: TaskUpdate object with fields to update

        Returns:
            Updated TaskResponse object or None if not found
        """
        with get_session_context() as session:
            task = session.get(DBTask, task_id)
            if not task or task.user_id != user_id:
                return None

            # Update fields that were provided
            if task_update.title is not None:
                task.title = task_update.title
            if task_update.description is not None:
                task.description = task_update.description
            if task_update.completed is not None:
                task.completed = task_update.completed

            task.updated_at = datetime.utcnow()
            session.add(task)
            session.commit()
            session.refresh(task)

            return TaskResponse(
                id=task.id,
                user_id=task.user_id,
                title=task.title,
                description=task.description,
                completed=task.completed,
                created_at=task.created_at,
                updated_at=task.updated_at
            )

    @staticmethod
    def delete_task(user_id: str, task_id: int) -> bool:
        """
        Delete a task.

        Args:
            user_id: The ID of the user who owns the task
            task_id: The ID of the task to delete

        Returns:
            True if deletion was successful, False otherwise
        """
        with get_session_context() as session:
            task = session.get(DBTask, task_id)
            if not task or task.user_id != user_id:
                return False

            session.delete(task)
            session.commit()
            return True

    @staticmethod
    def complete_task(user_id: str, task_id: int) -> Optional[TaskResponse]:
        """
        Mark a task as complete.

        Args:
            user_id: The ID of the user who owns the task
            task_id: The ID of the task to mark as complete

        Returns:
            Updated TaskResponse object or None if not found
        """
        with get_session_context() as session:
            task = session.get(DBTask, task_id)
            if not task or task.user_id != user_id:
                return None

            task.completed = True
            task.updated_at = datetime.utcnow()
            session.add(task)
            session.commit()
            session.refresh(task)

            return TaskResponse(
                id=task.id,
                user_id=task.user_id,
                title=task.title,
                description=task.description,
                completed=task.completed,
                created_at=task.created_at,
                updated_at=task.updated_at
            )