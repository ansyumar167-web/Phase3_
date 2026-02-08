# API Contract: POST /api/{user_id}/chat

## Endpoint
```
POST /api/{user_id}/chat
```

## Description
Handles chat requests from authenticated users and manages conversation persistence. The endpoint authenticates the user, reconstructs conversation history from the database, processes the user's message, and persists both user and assistant messages.

## Authentication
Bearer token authentication via Better Auth. The user_id in the URL must match the authenticated user's ID.

## Request

### Path Parameters
- `user_id` (string, required): The authenticated user's identifier

### Headers
- `Authorization` (string, required): Bearer token for authentication
- `Content-Type` (string, required): application/json

### Body
```json
{
  "conversation_id": "integer (optional)",
  "message": "string (required)"
}
```

#### Fields
- `conversation_id`: Optional existing conversation ID. If omitted, a new conversation is created.
- `message`: The user's message content to be processed by the AI assistant.

## Response

### Success Response (200)
```json
{
  "conversation_id": "integer",
  "response": "string",
  "tool_calls": "array of objects (optional)"
}
```

#### Success Fields
- `conversation_id`: The conversation ID (either provided or newly created)
- `response`: The AI assistant's response to the user's message
- `tool_calls`: Optional array of tool calls executed by the AI (e.g., task operations)

### Error Responses

#### 401 Unauthorized
```json
{
  "detail": "Unauthorized"
}
```

#### 403 Forbidden
```json
{
  "detail": "Access forbidden: user_id mismatch"
}
```

#### 422 Unprocessable Entity
```json
{
  "detail": "Validation error",
  "errors": [
    {
      "field": "string",
      "message": "string"
    }
  ]
}
```

#### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

## Examples

### Request Example
```
POST /api/ziakhan/chat
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
  "conversation_id": 123,
  "message": "What tasks do I have pending?"
}
```

### Success Response Example
```json
{
  "conversation_id": 123,
  "response": "You have 3 pending tasks: Buy groceries, Call mom, Finish report",
  "tool_calls": [
    {
      "name": "list_tasks",
      "arguments": {
        "user_id": "ziakhan",
        "status": "pending"
      }
    }
  ]
}
```

## Business Logic
1. Validates that the authenticated user matches the user_id in the URL
2. If conversation_id is provided, retrieves existing conversation history
3. If no conversation_id, creates a new conversation
4. Saves the user's message to the database
5. Forwards the conversation history to the AI agent
6. AI agent processes the message and may call MCP tools
7. AI generates response based on tool results
8. Saves the assistant's response to the database
9. Returns the response and any tool calls executed