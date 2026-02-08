from fastapi import APIRouter, HTTPException, Depends, status
from typing import List, Optional
from sqlmodel import Session
from ..database.session import get_session
from ..services.task_service import TaskService
from ..models.task import TaskCreate, TaskUpdate, TaskResponse
from ..api.chat_endpoint import get_current_user_from_token
from ..config import settings
import time
from ..utils.logging_config import get_logger, log_api_request

router = APIRouter(prefix=f"{settings.api_v1_str}/tasks", tags=["tasks"])
logger = get_logger("api.task_endpoint")


@router.get("", response_model=dict)
async def get_tasks(
    user_id: Optional[str] = None,
    status: Optional[str] = None,
    current_user=Depends(get_current_user_from_token),
    session: Session = Depends(get_session)
):
    """
    Get all tasks for the authenticated user.

    Query params:
    - user_id: Optional, but must match authenticated user
    - status: Optional filter ("all", "pending", "completed")
    """
    start_time = time.time()

    # Use authenticated user's ID
    auth_user_id = str(current_user.id)

    # If user_id provided in query, verify it matches authenticated user
    if user_id and user_id != auth_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot access tasks for other users"
        )

    try:
        logger.info(f"Fetching tasks for user: {auth_user_id}, status filter: {status}")
        tasks = TaskService.get_tasks(auth_user_id, status)

        duration = time.time() - start_time
        log_api_request(f"{settings.api_v1_str}/tasks", "GET", user_id=auth_user_id, status_code=200, duration=duration)

        return {"tasks": tasks}
    except Exception as e:
        duration = time.time() - start_time
        logger.error(f"Error fetching tasks for user {auth_user_id}: {str(e)}")
        log_api_request(f"{settings.api_v1_str}/tasks", "GET", user_id=auth_user_id, status_code=500, duration=duration)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching tasks: {str(e)}"
        )


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    current_user=Depends(get_current_user_from_token),
    session: Session = Depends(get_session)
):
    """
    Create a new task for the authenticated user.
    """
    start_time = time.time()
    auth_user_id = str(current_user.id)

    # Ensure task is created for the authenticated user
    if task_data.user_id != auth_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot create tasks for other users"
        )

    try:
        logger.info(f"Creating task for user: {auth_user_id}, title: {task_data.title}")
        task = TaskService.create_task(task_data)

        duration = time.time() - start_time
        log_api_request(f"{settings.api_v1_str}/tasks", "POST", user_id=auth_user_id, status_code=201, duration=duration)

        return task
    except Exception as e:
        duration = time.time() - start_time
        logger.error(f"Error creating task for user {auth_user_id}: {str(e)}")
        log_api_request(f"{settings.api_v1_str}/tasks", "POST", user_id=auth_user_id, status_code=500, duration=duration)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating task: {str(e)}"
        )


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    current_user=Depends(get_current_user_from_token),
    session: Session = Depends(get_session)
):
    """
    Get a specific task by ID.
    """
    auth_user_id = str(current_user.id)

    try:
        task = TaskService.get_task_by_id(auth_user_id, task_id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        return task
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching task {task_id} for user {auth_user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching task: {str(e)}"
        )


@router.patch("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_update: TaskUpdate,
    current_user=Depends(get_current_user_from_token),
    session: Session = Depends(get_session)
):
    """
    Update a task (title, description, or completion status).
    """
    start_time = time.time()
    auth_user_id = str(current_user.id)

    try:
        logger.info(f"Updating task {task_id} for user: {auth_user_id}")
        task = TaskService.update_task(auth_user_id, task_id, task_update)

        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )

        duration = time.time() - start_time
        log_api_request(f"{settings.api_v1_str}/tasks/{task_id}", "PATCH", user_id=auth_user_id, status_code=200, duration=duration)

        return task
    except HTTPException:
        raise
    except Exception as e:
        duration = time.time() - start_time
        logger.error(f"Error updating task {task_id} for user {auth_user_id}: {str(e)}")
        log_api_request(f"{settings.api_v1_str}/tasks/{task_id}", "PATCH", user_id=auth_user_id, status_code=500, duration=duration)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating task: {str(e)}"
        )


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    current_user=Depends(get_current_user_from_token),
    session: Session = Depends(get_session)
):
    """
    Delete a task.
    """
    start_time = time.time()
    auth_user_id = str(current_user.id)

    try:
        logger.info(f"Deleting task {task_id} for user: {auth_user_id}")
        success = TaskService.delete_task(auth_user_id, task_id)

        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )

        duration = time.time() - start_time
        log_api_request(f"{settings.api_v1_str}/tasks/{task_id}", "DELETE", user_id=auth_user_id, status_code=204, duration=duration)

        return None
    except HTTPException:
        raise
    except Exception as e:
        duration = time.time() - start_time
        logger.error(f"Error deleting task {task_id} for user {auth_user_id}: {str(e)}")
        log_api_request(f"{settings.api_v1_str}/tasks/{task_id}", "DELETE", user_id=auth_user_id, status_code=500, duration=duration)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting task: {str(e)}"
        )
