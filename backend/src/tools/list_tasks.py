from typing import Dict, Any, List
from pydantic import BaseModel
from ..services.task_service import TaskService


class ListTasksParams(BaseModel):
    """Parameters for list_tasks tool."""
    user_id: str
    status: str = "all"  # all, pending, completed


async def execute(params: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    List tasks for a user.

    Args:
        params: Dictionary containing user_id and optional status filter

    Returns:
        List of task dictionaries
    """
    try:
        # Validate parameters
        validated = ListTasksParams(**params)

        # Get tasks using TaskService
        tasks = TaskService.get_tasks(validated.user_id, validated.status)

        # Convert to dictionary format
        return [
            {
                "id": task.id,
                "user_id": task.user_id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed
            }
            for task in tasks
        ]
    except Exception as e:
        return [{"error": str(e)}]
