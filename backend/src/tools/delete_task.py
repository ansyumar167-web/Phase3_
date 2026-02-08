from typing import Dict, Any
from pydantic import BaseModel
from ..services.mcp_server import mcp_server


class DeleteTaskParams(BaseModel):
    """Parameters for delete_task tool."""
    user_id: str
    task_id: int


async def delete_task(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Delete a task.

    Args:
        params: Dictionary containing user_id and task_id

    Returns:
        Dictionary with task_id, status, and title
    """
    result = await mcp_server.handle_call("delete_task", params)

    if not result.success:
        raise Exception(result.error)

    return result.data