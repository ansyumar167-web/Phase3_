from typing import Dict, Any, Optional
from pydantic import BaseModel
from ..services.task_service import TaskService
from ..models.task import TaskUpdate


class UpdateTaskParams(BaseModel):
    """Parameters for update_task tool."""
    user_id: str
    task_id: int
    title: Optional[str] = None
    description: Optional[str] = None


async def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update a task.

    Args:
        params: Dictionary containing user_id, task_id, and optional title/description

    Returns:
        Dictionary with task_id, status, and title
    """
    try:
        # Validate parameters
        validated = UpdateTaskParams(**params)

        # Create update data
        update_data = TaskUpdate(
            title=validated.title,
            description=validated.description
        )

        # Update task using TaskService
        result = TaskService.update_task(validated.user_id, validated.task_id, update_data)

        return {
            "task_id": result.id,
            "status": "updated",
            "title": result.title
        }
    except Exception as e:
        return {
            "error": str(e),
            "status": "failed"
        }
