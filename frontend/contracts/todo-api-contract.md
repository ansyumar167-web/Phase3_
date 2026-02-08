# API Contract: Todo Management API

## Overview
This document defines the contract between the frontend application and the backend todo management API for the task management system.

## Base URL
`http://localhost:8000` (configurable via environment variables)

## Authentication
All endpoints (except authentication endpoints) require authentication via JWT token in the Authorization header:
```
Authorization: Bearer {jwt_token}
```

## Endpoints

### POST /api/{user_id}/chat
Send a message to the AI assistant to manage tasks.

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
- `message`: The user's natural language message to the AI assistant
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

### GET /api/{user_id}/tasks
Retrieve all tasks for a specific user.

#### Request
**Path Parameters:**
- `user_id` (string, required): The authenticated user's ID

**Headers:**
- `Authorization` (string, required): Bearer token

#### Response
**Success Response (200 OK):**
```json
{
  "tasks": [
    {
      "id": "number",
      "user_id": "string",
      "title": "string",
      "description": "string (nullable)",
      "completed": "boolean",
      "created_at": "string (ISO date)",
      "updated_at": "string (ISO date)"
    }
  ]
}
```

**Response Field Definitions:**
- `tasks`: Array of task objects
  - `id`: Unique identifier for the task
  - `user_id`: The ID of the user who owns the task
  - `title`: The title of the task
  - `description`: Optional description of the task (can be null)
  - `completed`: Whether the task has been completed
  - `created_at`: ISO date string of when the task was created
  - `updated_at`: ISO date string of when the task was last updated

**Error Responses:**
- `401 Unauthorized`: Missing or invalid authentication token
- `403 Forbidden`: User does not have permission to access this resource
- `404 Not Found`: User ID does not exist
- `500 Internal Server Error`: Server error processing the request

### POST /api/{user_id}/tasks
Create a new task for a user.

#### Request
**Path Parameters:**
- `user_id` (string, required): The authenticated user's ID

**Headers:**
- `Authorization` (string, required): Bearer token
- `Content-Type` (string, required): application/json

**Body:**
```json
{
  "title": "string (required)",
  "description": "string (optional)",
  "completed": "boolean (optional, default: false)"
}
```

**Body Field Definitions:**
- `title`: The title of the task (required)
- `description`: Optional description of the task
- `completed`: Whether the task is initially completed (defaults to false)

#### Response
**Success Response (201 Created):**
```json
{
  "id": "number",
  "user_id": "string",
  "title": "string",
  "description": "string (nullable)",
  "completed": "boolean",
  "created_at": "string (ISO date)",
  "updated_at": "string (ISO date)"
}
```

**Error Responses:**
- `400 Bad Request`: Invalid request body or parameters
- `401 Unauthorized`: Missing or invalid authentication token
- `403 Forbidden`: User does not have permission to access this resource
- `500 Internal Server Error`: Server error processing the request

### PUT /api/{user_id}/tasks/{task_id}
Update an existing task.

#### Request
**Path Parameters:**
- `user_id` (string, required): The authenticated user's ID
- `task_id` (number, required): The ID of the task to update

**Headers:**
- `Authorization` (string, required): Bearer token
- `Content-Type` (string, required): application/json

**Body:**
```json
{
  "title": "string (optional)",
  "description": "string (optional)",
  "completed": "boolean (optional)"
}
```

**Body Field Definitions:**
- `title`: New title for the task (optional)
- `description`: New description for the task (optional)
- `completed`: New completion status for the task (optional)

#### Response
**Success Response (200 OK):**
```json
{
  "id": "number",
  "user_id": "string",
  "title": "string",
  "description": "string (nullable)",
  "completed": "boolean",
  "created_at": "string (ISO date)",
  "updated_at": "string (ISO date)"
}
```

**Error Responses:**
- `400 Bad Request`: Invalid request body or parameters
- `401 Unauthorized`: Missing or invalid authentication token
- `403 Forbidden`: User does not have permission to access this resource
- `404 Not Found`: Task ID does not exist or does not belong to user
- `500 Internal Server Error`: Server error processing the request

### DELETE /api/{user_id}/tasks/{task_id}
Delete a task.

#### Request
**Path Parameters:**
- `user_id` (string, required): The authenticated user's ID
- `task_id` (number, required): The ID of the task to delete

**Headers:**
- `Authorization` (string, required): Bearer token

#### Response
**Success Response (204 No Content):**
- Empty response body

**Error Responses:**
- `401 Unauthorized`: Missing or invalid authentication token
- `403 Forbidden`: User does not have permission to access this resource
- `404 Not Found`: Task ID does not exist or does not belong to user
- `500 Internal Server Error`: Server error processing the request

### GET /api/{user_id}/conversations
Retrieve all conversations for a user.

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
    "updated_at": "string (ISO date)"
  }
]
```

**Response Field Definitions:**
- `id`: Unique identifier for the conversation
- `user_id`: The ID of the user who owns the conversation
- `created_at`: ISO date string of when the conversation was created
- `updated_at`: ISO date string of when the conversation was last updated

**Error Responses:**
- `401 Unauthorized`: Missing or invalid authentication token
- `403 Forbidden`: User does not have permission to access this resource
- `404 Not Found`: User ID does not exist
- `500 Internal Server Error`: Server error processing the request

### GET /api/{user_id}/conversations/{conversation_id}/messages
Retrieve messages for a specific conversation.

#### Request
**Path Parameters:**
- `user_id` (string, required): The authenticated user's ID
- `conversation_id` (number, required): The ID of the conversation

**Headers:**
- `Authorization` (string, required): Bearer token

#### Response
**Success Response (200 OK):**
```json
[
  {
    "id": "string",
    "conversation_id": "number",
    "role": "'user' | 'assistant'",
    "content": "string",
    "timestamp": "string (ISO date)"
  }
]
```

**Response Field Definitions:**
- `id`: Unique identifier for the message
- `conversation_id`: The ID of the conversation this message belongs to
- `role`: The role of the message sender ('user' or 'assistant')
- `content`: The content of the message
- `timestamp`: ISO date string of when the message was created

**Error Responses:**
- `401 Unauthorized`: Missing or invalid authentication token
- `403 Forbidden`: User does not have permission to access this resource
- `404 Not Found`: Conversation ID does not exist or does not belong to user
- `500 Internal Server Error`: Server error processing the request

## Data Types

### Task Object
- `id` (number): Unique identifier for the task
- `user_id` (string): The ID of the user who owns the task
- `title` (string): The title of the task
- `description` (string | null): Optional description of the task
- `completed` (boolean): Whether the task has been completed
- `created_at` (string): ISO 8601 date string
- `updated_at` (string): ISO 8601 date string

### Message Object
- `id` (string): Unique identifier for the message
- `conversation_id` (number): The ID of the conversation
- `role` (string): Either 'user' or 'assistant'
- `content` (string): The message content
- `timestamp` (string): ISO 8601 date string

### Chat Response
- `conversation_id` (number): The ID of the conversation
- `response` (string): The AI assistant's response
- `tool_calls` (string[]): Array of tools that were called

## Error Handling

### Standard Error Response Format
```json
{
  "detail": "string"
}
```

### Common Error Codes
- `400`: Bad Request - Malformed request or invalid parameters
- `401`: Unauthorized - Missing or invalid authentication
- `403`: Forbidden - Insufficient permissions
- `404`: Not Found - Requested resource does not exist
- `422`: Unprocessable Entity - Valid request format but semantic errors
- `500`: Internal Server Error - Server-side processing error

## Security
- All sensitive data must be transmitted over HTTPS
- JWT tokens should have appropriate expiration times
- All endpoints require valid authentication except for login/register
- User data is isolated by user ID

## Rate Limiting
Requests may be subject to rate limiting. Excessive requests may result in 429 responses.

## Testing
When testing, ensure the backend server is running and accessible at the configured base URL.