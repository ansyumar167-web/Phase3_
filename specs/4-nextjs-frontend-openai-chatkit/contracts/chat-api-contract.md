# API Contract: Chat API Integration

## Overview
This document defines the contract between the frontend application and the backend chat API for the todo management system.

## Base URL
`http://localhost:8000` (configurable via environment variables)

## Authentication
All endpoints require authentication via JWT token in the Authorization header:
```
Authorization: Bearer {jwt_token}
```

## Endpoints

### POST /api/{user_id}/chat
Initiate a conversation with the AI assistant to manage tasks.

#### Request
**Path Parameters:**
- `user_id` (string, required): The authenticated user's ID

**Headers:**
- `Authorization` (string, required): Bearer token
- `Content-Type` (string, required): application/json

**Body:**
```json
{
  "message": "string (required)",
  "conversation_id": "number (optional)"
}
```

**Body Field Definitions:**
- `message`: The user's message to the AI assistant (natural language command)
- `conversation_id`: The ID of an existing conversation to continue (omit for new conversation)

#### Response
**Success Response (200 OK):**
```json
{
  "conversation_id": "number",
  "response": "string",
  "tool_calls": "string[]"
}
```

**Response Field Definitions:**
- `conversation_id`: The ID of the current conversation (new or existing)
- `response`: The AI assistant's response to the user's message
- `tool_calls`: Array of MCP tools that were invoked as a result of the message

**Error Responses:**
- `400 Bad Request`: Invalid request body or parameters
- `401 Unauthorized`: Missing or invalid authentication token
- `403 Forbidden`: User does not have permission to access this resource
- `404 Not Found`: User ID does not exist
- `500 Internal Server Error`: Server error processing the request

#### Examples
**Request:**
```http
POST /api/user123/chat HTTP/1.1
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
  "message": "Add a task to buy groceries",
  "conversation_id": 123
}
```

**Response:**
```json
{
  "conversation_id": 123,
  "response": "I've added the task 'buy groceries' to your list.",
  "tool_calls": ["add_task"]
}
```

### GET /api/{user_id}/conversations
Retrieve a list of conversations for the user.

#### Request
**Path Parameters:**
- `user_id` (string, required): The authenticated user's ID

**Headers:**
- `Authorization` (string, required): Bearer token

#### Response
**Success Response (200 OK):**
```json
[
  {
    "id": "number",
    "user_id": "string",
    "created_at": "string (ISO date)",
    "updated_at": "string (ISO date)",
    "message_count": "number"
  }
]
```

### GET /api/{user_id}/conversations/{conversation_id}/messages
Retrieve messages for a specific conversation.

#### Request
**Path Parameters:**
- `user_id` (string, required): The authenticated user's ID
- `conversation_id` (number, required): The conversation ID

**Headers:**
- `Authorization` (string, required): Bearer token

#### Response
**Success Response (200 OK):**
```json
[
  {
    "id": "number",
    "conversation_id": "number",
    "user_id": "string",
    "role": "string (user|assistant)",
    "content": "string",
    "created_at": "string (ISO date)"
  }
]
```

## Data Types

### Message Role
- `user`: Messages sent by the user
- `assistant`: Messages sent by the AI assistant

### Tool Calls
Possible values in the `tool_calls` array:
- `add_task`: Adding a new task
- `list_tasks`: Retrieving a list of tasks
- `complete_task`: Marking a task as complete
- `delete_task`: Deleting a task
- `update_task`: Updating a task

## Error Handling

### Standard Error Response Format
```json
{
  "error": "string",
  "status_code": "number",
  "timestamp": "string (ISO date)",
  "path": "string"
}
```

### Common Error Codes
- `400`: Bad Request - Malformed request or invalid parameters
- `401`: Unauthorized - Missing or invalid authentication
- `403`: Forbidden - Insufficient permissions
- `404`: Not Found - Requested resource does not exist
- `422`: Unprocessable Entity - Valid request format but semantic errors
- `500`: Internal Server Error - Server-side processing error

## Versioning
This API contract follows the backend API versioning scheme. Current version is v1.

## Security
- All requests must include a valid JWT token
- User ID in path parameter must match the authenticated user
- Requests from unauthorized sources will be rejected with 401/403 errors

## Rate Limiting
Requests may be subject to rate limiting. Excessive requests may result in 429 responses.

## Testing
When testing, ensure the backend server is running and accessible at the configured base URL.