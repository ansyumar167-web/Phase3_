"""MCP Client for communicating with the MCP server tools."""
import asyncio
from typing import Dict, Any, Optional
from ..config import settings
from ..tools import add_task, list_tasks, complete_task, delete_task, update_task


class MCPClient:
    """
    MCP Client for communicating with the MCP server tools.
    In production, this directly calls the tool functions instead of using a separate MCP server.
    """

    def __init__(self, host: str = None, port: int = None):
        """
        Initialize the MCP client.

        Args:
            host: Host address of the MCP server (defaults to config) - not used in direct mode
            port: Port of the MCP server (defaults to config) - not used in direct mode
        """
        self.host = host or settings.mcp_server_host
        self.port = port or settings.mcp_server_port
        self.connected = True  # Always connected in direct mode

    async def connect(self):
        """Connect to the MCP server - no-op in direct mode."""
        self.connected = True

    async def disconnect(self):
        """Disconnect from the MCP server - no-op in direct mode."""
        self.connected = False

    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Call an MCP tool with the given arguments.

        Args:
            tool_name: Name of the tool to call (e.g., "add_task", "list_tasks", etc.)
            arguments: Arguments to pass to the tool

        Returns:
            Result from the tool call
        """
        try:
            # Direct tool mapping - call the actual tool functions
            if tool_name == "add_task":
                return await add_task.execute(arguments)
            elif tool_name == "list_tasks":
                return await list_tasks.execute(arguments)
            elif tool_name == "complete_task":
                return await complete_task.execute(arguments)
            elif tool_name == "delete_task":
                return await delete_task.execute(arguments)
            elif tool_name == "update_task":
                return await update_task.execute(arguments)
            else:
                return {"error": f"Unknown tool: {tool_name}"}
        except Exception as e:
            return {"error": str(e)}

    async def add_task(self, user_id: str, title: str, description: Optional[str] = None) -> Dict[str, Any]:
        """Call the add_task tool."""
        arguments = {
            "user_id": user_id,
            "title": title
        }
        if description:
            arguments["description"] = description

        return await self.call_tool("add_task", arguments)

    async def list_tasks(self, user_id: str, status: Optional[str] = None) -> Dict[str, Any]:
        """Call the list_tasks tool."""
        arguments = {
            "user_id": user_id
        }
        if status:
            arguments["status"] = status

        return await self.call_tool("list_tasks", arguments)

    async def complete_task(self, user_id: str, task_id: int) -> Dict[str, Any]:
        """Call the complete_task tool."""
        arguments = {
            "user_id": user_id,
            "task_id": task_id
        }

        return await self.call_tool("complete_task", arguments)

    async def delete_task(self, user_id: str, task_id: int) -> Dict[str, Any]:
        """Call the delete_task tool."""
        arguments = {
            "user_id": user_id,
            "task_id": task_id
        }

        return await self.call_tool("delete_task", arguments)

    async def update_task(self, user_id: str, task_id: int, title: Optional[str] = None,
                         description: Optional[str] = None) -> Dict[str, Any]:
        """Call the update_task tool."""
        arguments = {
            "user_id": user_id,
            "task_id": task_id
        }
        if title is not None:
            arguments["title"] = title
        if description is not None:
            arguments["description"] = description

        return await self.call_tool("update_task", arguments)


# Global MCP client instance
_mcp_client: Optional[MCPClient] = None


def get_mcp_client() -> MCPClient:
    """Get the global MCP client instance."""
    global _mcp_client
    if _mcp_client is None:
        _mcp_client = MCPClient()
    return _mcp_client


# Ensure the client instance is initialized when module is loaded
if _mcp_client is None:
    _mcp_client = MCPClient()