from typing import Dict, Any
from pydantic import BaseModel
from ..services.mcp_server import mcp_server


class UpdateTaskParams(BaseModel):
    """Parameters for update_task tool."""
    user_id: str
    task_id: int
    title: str = None
    description: str = None


async def update_task(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update a task.

    Args:
        params: Dictionary containing user_id, task_id, and optional title/description

    Returns:
        Dictionary with task_id, status, and title
    """
    result = await mcp_server.handle_call("update_task", params)

    if not result.success:
        raise Exception(result.error)

    return result.data