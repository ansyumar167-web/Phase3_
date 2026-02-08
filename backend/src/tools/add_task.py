from typing import Dict, Any
from pydantic import BaseModel
from ..services.task_service import TaskService
from ..models.task import TaskCreate


class AddTaskParams(BaseModel):
    """Parameters for add_task tool."""
    user_id: str
    title: str
    description: str = ""


async def execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Add a new task.

    Args:
        params: Dictionary containing user_id, title, and optional description

    Returns:
        Dictionary with task_id, status, and title
    """
    try:
        # Validate parameters
        validated = AddTaskParams(**params)

        # Create task using TaskService
        task_data = TaskCreate(
            user_id=validated.user_id,
            title=validated.title,
            description=validated.description
        )

        result = TaskService.create_task(task_data)

        return {
            "task_id": result.id,
            "status": "created",
            "title": result.title
        }
    except Exception as e:
        return {
            "error": str(e),
            "status": "failed"
        }
