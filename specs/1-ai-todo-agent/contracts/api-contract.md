# API Contract: AI-Powered Conversational Todo Agent

## Endpoint: POST /api/{user_id}/chat

### Description
Processes a user message and returns an AI response with appropriate MCP tool calls.

### Request Parameters
- `user_id` (path parameter, string, required): Unique identifier for the user

### Request Body
```json
{
  "message": "string (required): The user's natural language message",
  "conversation_id": "integer (optional): ID of existing conversation, or null for new"
}
```

### Response Body
```json
{
  "conversation_id": "integer: ID of the conversation (newly created or existing)",
  "response": "string: AI-generated natural language response to the user",
  "tool_calls": "array of strings: List of MCP tools that were invoked"
}
```

### Error Responses
- `400 Bad Request`: Invalid request format
- `401 Unauthorized`: Invalid or missing user authentication
- `500 Internal Server Error`: Server error during processing

### Example Request
```json
{
  "message": "Add a task to buy groceries",
  "conversation_id": null
}
```

### Example Response
```json
{
  "conversation_id": 123,
  "response": "I've added the task 'buy groceries' to your list.",
  "tool_calls": ["add_task"]
}
```

## MCP Tool Contracts

### Tool: add_task
- **Purpose**: Create a new task
- **Parameters**:
  - `user_id` (string, required)
  - `title` (string, required)
  - `description` (string, optional)
- **Returns**:
  - `task_id` (integer)
  - `status` (string: "created")
  - `title` (string)

### Tool: list_tasks
- **Purpose**: Retrieve tasks from the list
- **Parameters**:
  - `user_id` (string, required)
  - `status` (string, optional: "all", "pending", "completed")
- **Returns**:
  - Array of task objects with id, user_id, title, completed status

### Tool: complete_task
- **Purpose**: Mark a task as complete
- **Parameters**:
  - `user_id` (string, required)
  - `task_id` (integer, required)
- **Returns**:
  - `task_id` (integer)
  - `status` (string: "completed")
  - `title` (string)

### Tool: delete_task
- **Purpose**: Remove a task from the list
- **Parameters**:
  - `user_id` (string, required)
  - `task_id` (integer, required)
- **Returns**:
  - `task_id` (integer)
  - `status` (string: "deleted")
  - `title` (string)

### Tool: update_task
- **Purpose**: Modify task title or description
- **Parameters**:
  - `user_id` (string, required)
  - `task_id` (integer, required)
  - `title` (string, optional)
  - `description` (string, optional)
- **Returns**:
  - `task_id` (integer)
  - `status` (string: "updated")
  - `title` (string)