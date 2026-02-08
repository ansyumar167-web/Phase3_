from typing import Dict, Any
from pydantic import BaseModel
from ..services.task_service import TaskService


class CompleteTaskParams(BaseModel):
    """Parameters for complete_task tool."""
    user_id: str
    task_id: int


async def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Mark a task as complete.

    Args:
        params: Dictionary containing user_id and task_id

    Returns:
        Dictionary with task_id, status, and title
    """
    try:
        # Validate parameters
        validated = CompleteTaskParams(**params)

        # Complete task using TaskService
        result = TaskService.complete_task(validated.user_id, validated.task_id)

        return {
            "task_id": result.id,
            "status": "completed",
            "title": result.title
        }
    except Exception as e:
        return {
            "error": str(e),
            "status": "failed"
        }
