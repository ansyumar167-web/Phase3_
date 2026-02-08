import asyncio
from typing import Dict, Any, List, Optional
from mcp_use import MCPServer
from mcp import LoggingLevel
import json
from ..models.task import TaskCreate, TaskUpdate
from .task_service import TaskService


class TodoMCPServer:
    """
    MCP (Model Context Protocol) Server that exposes task management tools for AI agents.

    This server implements the MCP specification and provides tools for:
    - add_task: Create a new task
    - list_tasks: Retrieve tasks with optional filtering
    - complete_task: Mark a task as complete
    - delete_task: Remove a task
    - update_task: Modify task properties
    """

    def __init__(self):
        # Initialize the MCP server
        self.server = MCPServer(
            name="todo-mcp-server",
            version="1.0.0",
            instructions="MCP server for managing todo tasks"
        )

        # Register tools using the proper decorator pattern
        self._setup_tools()

    def _setup_tools(self):
        """
        Register all MCP tools that will be available to AI agents.
        Each tool corresponds to a specific task management operation.
        """
        # Tool for adding a new task
        @self.server.tool("add_task", description="Create a new task")
        async def add_task_handler(context: Dict[str, Any]) -> Dict[str, Any]:
            """
            MCP Tool: Create a new task

            Expected input parameters:
            - user_id: string (required) - The ID of the user creating the task
            - title: string (required) - The title of the task
            - description: string (optional) - Description of the task

            Returns:
            - task_id: integer - The ID of the created task
            - status: string - "created"
            - title: string - The title of the created task
            """
            try:
                user_id = context.get("user_id")
                title = context.get("title")
                description = context.get("description", None)

                if not user_id or not title:
                    raise ValueError("user_id and title are required parameters")

                task_create = TaskCreate(
                    user_id=user_id,
                    title=title,
                    description=description
                )

                task_response = TaskService.create_task(task_create)

                return {
                    "task_id": task_response.id,
                    "status": "created",
                    "title": task_response.title
                }
            except Exception as e:
                await self.server.log_message(LoggingLevel.ERROR, f"Error in add_task: {str(e)}")
                raise e

        # Tool for listing tasks
        @self.server.tool("list_tasks", description="Retrieve tasks from the list")
        async def list_tasks_handler(context: Dict[str, Any]) -> Dict[str, Any]:
            """
            MCP Tool: Retrieve tasks for a user with optional status filtering

            Expected input parameters:
            - user_id: string (required) - The ID of the user whose tasks to retrieve
            - status: string (optional) - Filter tasks by status ("all", "pending", "completed")

            Returns:
            - tasks: array of task objects with id, user_id, title, completed, created_at, updated_at
            """
            try:
                user_id = context.get("user_id")
                status = context.get("status", "all")  # Default to "all" if not specified

                if not user_id:
                    raise ValueError("user_id is required parameter")

                tasks = TaskService.get_tasks(user_id, status)

                # Convert tasks to the expected format for MCP response
                task_list = []
                for task in tasks:
                    task_list.append({
                        "id": task.id,
                        "user_id": task.user_id,
                        "title": task.title,
                        "description": task.description,
                        "completed": task.completed,
                        "created_at": task.created_at.isoformat() if hasattr(task.created_at, 'isoformat') else str(task.created_at),
                        "updated_at": task.updated_at.isoformat() if hasattr(task.updated_at, 'isoformat') else str(task.updated_at)
                    })

                return {"tasks": task_list}
            except Exception as e:
                await self.server.log_message(LoggingLevel.ERROR, f"Error in list_tasks: {str(e)}")
                raise e

        # Tool for completing a task
        @self.server.tool("complete_task", description="Mark a task as complete")
        async def complete_task_handler(context: Dict[str, Any]) -> Dict[str, Any]:
            """
            MCP Tool: Mark a task as complete

            Expected input parameters:
            - user_id: string (required) - The ID of the user who owns the task
            - task_id: integer (required) - The ID of the task to mark as complete

            Returns:
            - task_id: integer - The ID of the completed task
            - status: string - "completed"
            - title: string - The title of the completed task
            """
            try:
                user_id = context.get("user_id")
                task_id = context.get("task_id")

                if not user_id or task_id is None:
                    raise ValueError("user_id and task_id are required parameters")

                task_response = TaskService.complete_task(user_id, int(task_id))

                if not task_response:
                    raise ValueError(f"Task with ID {task_id} not found or does not belong to user {user_id}")

                return {
                    "task_id": task_response.id,
                    "status": "completed",
                    "title": task_response.title
                }
            except Exception as e:
                await self.server.log_message(LoggingLevel.ERROR, f"Error in complete_task: {str(e)}")
                raise e

        # Tool for deleting a task
        @self.server.tool("delete_task", description="Remove a task from the list")
        async def delete_task_handler(context: Dict[str, Any]) -> Dict[str, Any]:
            """
            MCP Tool: Remove a task

            Expected input parameters:
            - user_id: string (required) - The ID of the user who owns the task
            - task_id: integer (required) - The ID of the task to delete

            Returns:
            - task_id: integer - The ID of the deleted task
            - status: string - "deleted"
            - title: string - The title of the deleted task
            """
            try:
                user_id = context.get("user_id")
                task_id = context.get("task_id")

                if not user_id or task_id is None:
                    raise ValueError("user_id and task_id are required parameters")

                # Get the task first to return its title in the response
                task_response = TaskService.get_task_by_id(user_id, int(task_id))

                if not task_response:
                    raise ValueError(f"Task with ID {task_id} not found or does not belong to user {user_id}")

                success = TaskService.delete_task(user_id, int(task_id))

                if not success:
                    raise ValueError(f"Failed to delete task with ID {task_id}")

                return {
                    "task_id": int(task_id),
                    "status": "deleted",
                    "title": task_response.title
                }
            except Exception as e:
                await self.server.log_message(LoggingLevel.ERROR, f"Error in delete_task: {str(e)}")
                raise e

        # Tool for updating a task
        @self.server.tool("update_task", description="Modify task title or description")
        async def update_task_handler(context: Dict[str, Any]) -> Dict[str, Any]:
            """
            MCP Tool: Modify task properties

            Expected input parameters:
            - user_id: string (required) - The ID of the user who owns the task
            - task_id: integer (required) - The ID of the task to update
            - title: string (optional) - New title for the task
            - description: string (optional) - New description for the task

            Returns:
            - task_id: integer - The ID of the updated task
            - status: string - "updated"
            - title: string - The new title of the task
            """
            try:
                user_id = context.get("user_id")
                task_id = context.get("task_id")
                title = context.get("title")
                description = context.get("description")

                if not user_id or task_id is None:
                    raise ValueError("user_id and task_id are required parameters")

                # At least one field to update must be provided
                if title is None and description is None:
                    raise ValueError("At least one field (title or description) must be provided for update")

                # Prepare update data
                update_data = {}
                if title is not None:
                    update_data["title"] = title
                if description is not None:
                    update_data["description"] = description

                task_update = TaskUpdate(**update_data)

                task_response = TaskService.update_task(user_id, int(task_id), task_update)

                if not task_response:
                    raise ValueError(f"Task with ID {task_id} not found or does not belong to user {user_id}")

                return {
                    "task_id": task_response.id,
                    "status": "updated",
                    "title": task_response.title
                }
            except Exception as e:
                await self.server.log_message(LoggingLevel.ERROR, f"Error in update_task: {str(e)}")
                raise e

    def run_sync(self, host: str = "127.0.0.1", port: int = 3000):
        """
        Start the MCP server (synchronous/blocking call)

        This method is blocking and manages its own event loop internally.
        Use this in a separate thread to avoid blocking the main application.

        Args:
            host: Host address to bind the server to
            port: Port to run the server on
        """
        self.server.run(host=host, port=port)

    async def run(self, host: str = "127.0.0.1", port: int = 3000):
        """
        Start the MCP server (async version - deprecated, use run_sync instead)

        Args:
            host: Host address to bind the server to
            port: Port to run the server on
        """
        await self.server.run(host=host, port=port)

    def get_server(self):
        """
        Get the underlying MCP server instance for advanced configuration
        """
        return self.server


# Global server instance for use in the application
mcp_server_instance = TodoMCPServer()


def get_mcp_server():
    """
    Get the global MCP server instance
    """
    return mcp_server_instance