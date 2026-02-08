from typing import Dict, Any, List
from pydantic import BaseModel
from ..services.mcp_server import mcp_server


class ListTasksParams(BaseModel):
    """Parameters for list_tasks tool."""
    user_id: str
    status: str = "all"  # all, pending, completed


async def list_tasks(params: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    List tasks for a user.

    Args:
        params: Dictionary containing user_id and optional status filter

    Returns:
        List of task dictionaries
    """
    result = await mcp_server.handle_call("list_tasks", params)

    if not result.success:
        raise Exception(result.error)

    return result.data