# API Reference for Todo AI Agent

## Chat Endpoint

### POST `/api/{user_id}/chat`

Processes a user message and returns an AI response with appropriate MCP tool calls.

#### Path Parameters

- `user_id` (string, required): Unique identifier for the user

#### Request Body

```json
{
  "message": "string (required): The user's natural language message",
  "conversation_id": "integer (optional): ID of existing conversation, or null for new"
}
```

#### Response Body

```json
{
  "conversation_id": "integer: ID of the conversation (newly created or existing)",
  "response": "string: AI-generated natural language response to the user",
  "tool_calls": "array of strings: List of MCP tools that were invoked"
}
```

#### Example Request

```bash
curl -X POST http://localhost:8000/api/ziakhan/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Add a task to buy groceries", "conversation_id": null}'
```

#### Example Response

```json
{
  "conversation_id": 123,
  "response": "I've added the task 'buy groceries' to your list.",
  "tool_calls": ["add_task"]
}
```

## Supported Natural Language Commands

The AI agent understands various natural language commands for todo management:

### Adding Tasks
- "Add a task to buy groceries"
- "Create a task to call mom"
- "Remember to pay bills"
- "Add a task with description: Task title - Description here"

### Listing Tasks
- "Show me all my tasks"
- "What's pending?"
- "What have I completed?"
- "List my tasks"

### Completing Tasks
- "Mark task 3 as complete"
- "Complete task 1"
- "Finish the meeting task"
- "Done with task 5"

### Updating Tasks
- "Change task 1 to 'Call mom tonight'"
- "Update task 2 description to 'More details here'"
- "Rename task 4 to 'Buy milk and eggs'"

### Deleting Tasks
- "Delete task 3"
- "Remove the shopping task"
- "Cancel task 1"

## Error Handling

The system handles various error conditions gracefully:

- **Non-existent tasks**: Returns appropriate error message when referencing a task that doesn't exist
- **Invalid input**: Provides helpful feedback for malformed commands
- **Permission errors**: Ensures users can only modify their own tasks
- **System errors**: Handles unexpected issues with appropriate fallback responses