from typing import Dict, Any


class ErrorHandler:
    """Error handling for MCP tools."""

    @staticmethod
    async def handle_task_not_found(task_id: int, user_id: str) -> Dict[str, Any]:
        """Handle case when a task is not found."""
        return {
            "error": f"Task with ID {task_id} not found for user {user_id}",
            "suggestion": "Please check the task ID or list your tasks to see available options",
            "task_id": task_id
        }

    @staticmethod
    async def handle_invalid_input(message: str) -> Dict[str, Any]:
        """Handle case when input is invalid."""
        return {
            "error": f"Invalid input: {message}",
            "suggestion": "Please check your command and try again"
        }

    @staticmethod
    async def handle_general_error(error: str) -> Dict[str, Any]:
        """Handle general errors."""
        return {
            "error": f"An error occurred: {error}",
            "suggestion": "Please try again or contact support if the problem persists"
        }

    @staticmethod
    async def handle_permission_denied(task_id: int, user_id: str) -> Dict[str, Any]:
        """Handle case when user doesn't have permission for a task."""
        return {
            "error": f"Permission denied: Task {task_id} does not belong to user {user_id}",
            "suggestion": "You can only manage your own tasks"
        }


# Global error handler instance
error_handler = ErrorHandler()