from typing import Dict, Any, List
from openai import AsyncOpenAI
from pydantic import BaseModel
from ..config import settings
import json
import asyncio

# ---- AI Response Model ----
class AIResponse(BaseModel):
    """Response from the AI agent."""
    content: str
    tool_calls: List[str]

# ---- Async MCP Client Helper ----
from .mcp_client import get_mcp_client

_mcp_lock = asyncio.Lock()  # Ensure single async initialization

async def get_connected_mcp_client():
    """Get MCP client and connect if needed (thread-safe)."""
    mcp_client = get_mcp_client()
    async with _mcp_lock:
        if not mcp_client.connected:
            await mcp_client.connect()
    return mcp_client

# ---- AI Agent ----
class AIAgent:
    """AI Agent that processes natural language and uses MCP tools."""

    def __init__(self):
        """Initialize the AI Agent."""
        self.client = AsyncOpenAI(
            api_key=settings.openai_api_key or "fake-key-for-local-testing",
            base_url=settings.openrouter_base_url
        )
        self.model = getattr(settings, 'openai_model', 'gpt-4-turbo-preview')

        # Define MCP-compatible tools
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "add_task",
                    "description": "Create a new task",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string"},
                            "title": {"type": "string"},
                            "description": {"type": "string"}
                        },
                        "required": ["user_id", "title"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_tasks",
                    "description": "Retrieve tasks from the list",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string"},
                            "status": {"type": "string"}
                        },
                        "required": ["user_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "complete_task",
                    "description": "Mark a task as complete",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string"},
                            "task_id": {"type": "integer"}
                        },
                        "required": ["user_id", "task_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "delete_task",
                    "description": "Remove a task",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string"},
                            "task_id": {"type": "integer"}
                        },
                        "required": ["user_id", "task_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "update_task",
                    "description": "Modify task title or description",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string"},
                            "task_id": {"type": "integer"},
                            "title": {"type": "string"},
                            "description": {"type": "string"}
                        },
                        "required": ["user_id", "task_id"]
                    }
                }
            }
        ]

    # ---- Tool Execution ----
    async def _execute_tool_call(self, function_name: str, arguments: dict) -> dict:
        """Execute a tool call via direct DB operations (bypassing MCP for reliability)."""
        from .task_service import TaskService
        from ..models.task import TaskCreate, TaskUpdate

        try:
            # Use TaskService directly for reliability
            if function_name == "add_task":
                task = TaskService.create_task(TaskCreate(**arguments))
                return {"task_id": task.id, "status": "created", "title": task.title}

            elif function_name == "list_tasks":
                status = arguments.get("status", "all")
                tasks = TaskService.get_tasks(user_id=arguments["user_id"], status=status)
                return {"tasks": [
                    {
                        "id": t.id,
                        "user_id": t.user_id,
                        "title": t.title,
                        "description": t.description,
                        "completed": t.completed,
                        "created_at": t.created_at.isoformat(),
                        "updated_at": t.updated_at.isoformat()
                    } for t in tasks
                ]}

            elif function_name == "complete_task":
                task = TaskService.complete_task(user_id=arguments["user_id"], task_id=int(arguments["task_id"]))
                return {"task_id": task.id, "status": "completed", "title": task.title} if task else {"error": "Task not found"}

            elif function_name == "delete_task":
                task = TaskService.get_task_by_id(user_id=arguments["user_id"], task_id=int(arguments["task_id"]))
                if not task:
                    return {"error": "Task not found"}
                success = TaskService.delete_task(user_id=arguments["user_id"], task_id=int(arguments["task_id"]))
                return {"task_id": task.id, "status": "deleted", "title": task.title} if success else {"error": "Delete failed"}

            elif function_name == "update_task":
                # Prepare update data excluding user_id and task_id which aren't part of TaskUpdate
                update_data = {k: v for k, v in arguments.items() if k in ["title", "description"] and v is not None}
                task_update = TaskUpdate(**update_data)
                task = TaskService.update_task(user_id=arguments["user_id"], task_id=int(arguments["task_id"]), task_update=task_update)
                return {"task_id": task.id, "status": "updated", "title": task.title} if task else {"error": "Update failed"}

            else:
                return {"error": f"Unknown function: {function_name}"}

        except Exception as e:
            # Return a safe error message
            print(f"Tool execution error: {e}")
            import traceback
            traceback.print_exc()
            return {"error": f"Failed to execute {function_name}: {str(e)}"}

    # ---- Process Message ----
    async def process_message(
        self,
        user_id: str,
        message: str,
        conversation_history: List[Dict[str, str]]
    ) -> AIResponse:
        """Process user message and handle AI tool calls."""
        system_prompt = f"""
        You are a helpful assistant that manages todo lists using natural language.
        You can add, list, complete, delete, and update tasks.

        CRITICAL RULES:
        1. The user is already authenticated. Their user_id is: {user_id}
        2. NEVER ask the user for their user_id - it's automatically provided
        3. When user says "add a task", immediately add it without asking for ID
        4. When listing tasks, ALWAYS show the task ID number like "Task #15"
        5. When user asks to delete/complete/update, use the task ID from the list
        6. If user says "delete this task" without ID, first list tasks to show IDs
        7. Always respond in a friendly, helpful manner
        8. Format task lists clearly with IDs like: "Task #1: Buy milk"

        Example conversations:
        User: "Add a task to buy groceries"
        You: Call add_task tool immediately (user_id is auto-provided)

        User: "Show my tasks"
        You: Call list_tasks tool and show with IDs

        User: "Delete task 5"
        You: Call delete_task with task_id=5
        """

        formatted_history = [{"role": m["role"], "content": m["content"]} for m in conversation_history]
        formatted_history.append({"role": "user", "content": message})
        messages = [{"role": "system", "content": system_prompt}] + formatted_history

        try:
            # Estimate max tokens to avoid 402 errors
            prompt_token_estimate = sum(len(m.get("content",""))//4 for m in messages)
            max_tokens_for_completion = min(2048, 4096 - prompt_token_estimate)

            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=self.tools,
                tool_choice="auto",
                max_tokens=max_tokens_for_completion,
                stream=False,
                timeout=30
            )

            ai_message = response.choices[0].message

            tool_calls = []
            tool_responses = []

            if getattr(ai_message, "tool_calls", None):
                for tool_call in ai_message.tool_calls:
                    function_name = tool_call.function.name
                    arguments = json.loads(tool_call.function.arguments)
                    if "user_id" not in arguments:
                        arguments["user_id"] = user_id
                    result = await self._execute_tool_call(function_name, arguments)
                    tool_responses.append({
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": json.dumps(result)
                    })
                    tool_calls.append(function_name if "error" not in result else f"{function_name}_error")

            # If there are tool responses, format them into a user-friendly message
            final_content = ai_message.content

            if tool_responses:
                # Process each tool response and format appropriately
                formatted_results = []

                for tool_response in tool_responses:
                    result = json.loads(tool_response["content"])

                    # Format based on the tool that was called
                    if tool_response["name"] == "list_tasks":
                        if "tasks" in result and result["tasks"]:
                            task_list = "\n".join([
                                f"- {'[x]' if task['completed'] else '[ ]'} Task #{task['id']}: {task['title']}"
                                for task in result["tasks"]
                            ])
                            formatted_results.append(f"Here are your tasks:\n{task_list}")
                        else:
                            formatted_results.append("You have no tasks.")

                    elif tool_response["name"] == "add_task":
                        if "error" not in result:
                            formatted_results.append(f"✅ Added task #{result.get('task_id', '?')}: {result.get('title', 'Untitled task')}")
                        else:
                            formatted_results.append(f"Error adding task: {result['error']}")

                    elif tool_response["name"] == "complete_task":
                        if "error" not in result:
                            formatted_results.append(f"✅ Completed task #{result.get('task_id', '?')}: {result.get('title', 'Untitled task')}")
                        else:
                            formatted_results.append(f"Error completing task: {result['error']}")

                    elif tool_response["name"] == "delete_task":
                        if "error" not in result:
                            formatted_results.append(f"🗑️ Deleted task #{result.get('task_id', '?')}: {result.get('title', 'Untitled task')}")
                        else:
                            formatted_results.append(f"Error deleting task: {result['error']}")

                    elif tool_response["name"] == "update_task":
                        if "error" not in result:
                            formatted_results.append(f"✏️ Updated task #{result.get('task_id', '?')}: {result.get('title', 'Untitled task')}")
                        else:
                            formatted_results.append(f"Error updating task: {result['error']}")

                # If the AI didn't generate content, use our formatted results
                if not final_content or final_content.strip() == "":
                    final_content = "\n\n".join(formatted_results)
                else:
                    # Otherwise, append our results to the AI's response
                    final_content += "\n\n" + "\n\n".join(formatted_results)

            # Ensure AI content is never empty
            if not final_content or final_content.strip() == "":
                final_content = "Tool executed successfully." if tool_responses else "I'm here but I have no response to show."

            return AIResponse(content=final_content, tool_calls=tool_calls)

        except Exception as e:
            return AIResponse(content=f"I'm sorry, I encountered an error: {e}", tool_calls=[])

    async def process_simple_message(self, user_id: str, message: str) -> AIResponse:
        """Process a simple message without conversation history."""
        return await self.process_message(user_id, message, [])
