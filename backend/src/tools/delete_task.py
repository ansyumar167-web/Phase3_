from typing import Dict, Any
from pydantic import BaseModel
from ..services.task_service import TaskService


class DeleteTaskParams(BaseModel):
    """Parameters for delete_task tool."""
    user_id: str
    task_id: int


async def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Delete a task.

    Args:
        params: Dictionary containing user_id and task_id

    Returns:
        Dictionary with task_id, status, and title
    """
    try:
        # Validate parameters
        validated = DeleteTaskParams(**params)

        # Delete task using TaskService
        result = TaskService.delete_task(validated.user_id, validated.task_id)

        return {
            "task_id": result.id,
            "status": "deleted",
            "title": result.title
        }
    except Exception as e:
        return {
            "error": str(e),
            "status": "failed"
        }
