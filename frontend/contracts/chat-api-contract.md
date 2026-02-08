# API Contract: Chat API Integration

## Overview
This document defines the contract between the frontend application and the backend chat API for the task management system.

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