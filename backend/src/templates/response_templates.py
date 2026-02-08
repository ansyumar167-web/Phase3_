from typing import Dict, Any


class ResponseTemplates:
    """Templates for consistent AI responses."""

    @staticmethod
    def success_task_created(task_title: str) -> str:
        """Template for successful task creation."""
        return f"I've added the task '{task_title}' to your list."

    @staticmethod
    def success_task_completed(task_title: str) -> str:
        """Template for successful task completion."""
        return f"I've marked '{task_title}' as completed."

    @staticmethod
    def success_task_deleted(task_title: str) -> str:
        """Template for successful task deletion."""
        return f"I've removed '{task_title}' from your list."

    @staticmethod
    def success_task_updated(task_title: str) -> str:
        """Template for successful task update."""
        return f"I've updated the task to '{task_title}'."

    @staticmethod
    def success_tasks_list(count: int, status_filter: str = None) -> str:
        """Template for successful task listing."""
        if status_filter:
            return f"You have {count} {status_filter} tasks."
        else:
            return f"You have {count} tasks in your list."

    @staticmethod
    def error_task_not_found(task_id: int = None) -> str:
        """Template for task not found error."""
        if task_id:
            return f"I couldn't find a task with ID {task_id}. Please check the ID or ask me to show you your tasks."
        else:
            return "I couldn't find the specified task. Please check the ID or ask me to show you your tasks."

    @staticmethod
    def error_generic() -> str:
        """Template for generic errors."""
        return "I'm sorry, but I encountered an issue processing your request. Could you please try again?"

    @staticmethod
    def error_permission_denied() -> str:
        """Template for permission denied error."""
        return "You don't have permission to modify that task. You can only manage your own tasks."

    @staticmethod
    def clarification_needed() -> str:
        """Template for when clarification is needed."""
        return "I need a bit more information to help you with that. Could you please specify which task you mean?"

    @staticmethod
    def welcome_message() -> str:
        """Template for welcome message."""
        return "Hello! I'm your AI assistant for managing your todo list. You can ask me to add, list, complete, update, or delete tasks."

    @staticmethod
    def help_message() -> str:
        """Template for help message."""
        return (
            "I can help you manage your todo list. Try saying things like:\n"
            "- 'Add a task to buy groceries'\n"
            "- 'Show me all my tasks'\n"
            "- 'What's pending?'\n"
            "- 'Mark task 3 as complete'\n"
            "- 'Delete the meeting task'\n"
            "- 'Change task 1 to call mom tonight'"
        )


# Global instance of response templates
response_templates = ResponseTemplates()