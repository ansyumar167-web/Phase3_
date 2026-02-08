from typing import Dict, Any
from pydantic import BaseModel
from ..services.mcp_server import mcp_server


class AddTaskParams(BaseModel):
    """Parameters for add_task tool."""
    user_id: str
    title: str
    description: str = ""


async def add_task(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Add a new task.

    Args:
        params: Dictionary containing user_id, title, and optional description

    Returns:
        Dictionary with task_id, status, and title
    """
    result = await mcp_server.handle_call("add_task", params)

    if not result.success:
        raise Exception(result.error)

    return result.data