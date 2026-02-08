"""MCP Client for communicating with the MCP server tools."""
import asyncio
from typing import Dict, Any, Optional
from mcp_use import MCPClient as BaseMCPClient
from ..config import settings


class MCPClient:
    """
    MCP Client for communicating with the MCP server tools.
    This class connects to the actual MCP server and makes real tool calls.
    """

    def __init__(self, host: str = None, port: int = None):
        """
        Initialize the MCP client.

        Args:
            host: Host address of the MCP server (defaults to config)
            port: Port of the MCP server (defaults to config)
        """
        self.host = host or settings.mcp_server_host
        self.port = port or settings.mcp_server_port
        self.base_client = None
        self.connected = False

    async def connect(self):
        """Connect to the MCP server."""
        if not self.connected:
            try:
                # Create the base MCP client - using correct constructor parameters
                self.base_client = BaseMCPClient()

                # Connect to the server
                await self.base_client.connect(f"http://{self.host}:{self.port}")
                self.connected = True
                print(f"Connected to MCP server at {self.host}:{self.port}")
            except Exception as e:
                print(f"Failed to connect to MCP server: {e}")
                raise

    async def disconnect(self):
        """Disconnect from the MCP server."""
        if self.connected and self.base_client:
            await self.base_client.disconnect()
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
        if not self.connected:
            await self.connect()

        try:
            # Call the tool via the MCP protocol
            result = await self.base_client.call_tool(tool_name, arguments)
            return result
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