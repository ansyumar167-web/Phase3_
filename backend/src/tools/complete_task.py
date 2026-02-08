from typing import Dict, Any
from pydantic import BaseModel
from ..services.mcp_server import mcp_server


class CompleteTaskParams(BaseModel):
    """Parameters for complete_task tool."""
    user_id: str
    task_id: int


async def complete_task(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Mark a task as complete.

    Args:
        params: Dictionary containing user_id and task_id

    Returns:
        Dictionary with task_id, status, and title
    """
    result = await mcp_server.handle_call("complete_task", params)

    if not result.success:
        raise Exception(result.error)

    return result.data