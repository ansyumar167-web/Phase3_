# API Contract: Authentication API Integration

## Overview
This document defines the contract between the frontend application and the backend authentication API for the todo management system.

## Base URL
`http://localhost:8000` (configurable via environment variables)

## Authentication
Most endpoints require authentication via JWT token in the Authorization header:
```
Authorization: Bearer {jwt_token}
```
Authentication endpoints (login, register) do not require tokens.

## Endpoints

### POST /api/login
Authenticate a user with email and password.

#### Request
**Headers:**
- `Content-Type` (string, required): application/json

**Body:**
```json
{
  "email": "string (required)",
  "password": "string (required)"
}
```

**Body Field Definitions:**
- `email`: The user's email address for authentication
- `password`: The user's password (will be hashed on server)

#### Response
**Success Response (200 OK):**
```json
{
  "access_token": "string",
  "token_type": "string",
  "user": {
    "id": "string",
    "email": "string",
    "username": "string"
  }
}
```

**Response Field Definitions:**
- `access_token`: JWT token for subsequent authenticated requests
- `token_type`: Type of token (usually "bearer")
- `user.id`: Unique identifier for the authenticated user
- `user.email`: User's email address
- `user.username`: User's chosen username

**Error Responses:**
- `400 Bad Request`: Invalid request body or parameters
- `401 Unauthorized`: Invalid email or password
- `500 Internal Server Error`: Server error processing the request

#### Examples
**Request:**
```http
POST /api/login HTTP/1.1
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": "user123",
    "email": "user@example.com",
    "username": "example_user"
  }
}
```

### POST /api/register
Register a new user account.

#### Request
**Headers:**
- `Content-Type` (string, required): application/json

**Body:**
```json
{
  "email": "string (required)",
  "username": "string (required)",
  "password": "string (required)"
}
```

**Body Field Definitions:**
- `email`: The user's email address for account creation
- `username`: The user's chosen username
- `password`: The user's chosen password (will be hashed on server)

#### Response
**Success Response (201 Created):**
```json
{
  "id": "string",
  "email": "string",
  "username": "string"
}
```

**Response Field Definitions:**
- `id`: Unique identifier for the created user
- `email`: User's email address
- `username`: User's chosen username

**Error Responses:**
- `400 Bad Request`: Invalid request body or parameters
- `409 Conflict`: Email or username already exists
- `500 Internal Server Error`: Server error processing the request

### GET /api/auth/me
Retrieve information about the currently authenticated user.

#### Request
**Headers:**
- `Authorization` (string, required): Bearer token

#### Response
**Success Response (200 OK):**
```json
{
  "id": "string",
  "email": "string",
  "username": "string",
  "created_at": "string (ISO date)",
  "updated_at": "string (ISO date)"
}
```

**Response Field Definitions:**
- `id`: Unique identifier for the user
- `email`: User's email address
- `username`: User's chosen username
- `created_at`: ISO date string of when the account was created
- `updated_at`: ISO date string of when the account was last updated

**Error Responses:**
- `401 Unauthorized`: Missing or invalid authentication token
- `500 Internal Server Error`: Server error processing the request

### POST /api/auth/logout
Logout the current user and invalidate the session.

#### Request
**Headers:**
- `Authorization` (string, required): Bearer token
- `Content-Type` (string, required): application/json

#### Response
**Success Response (200 OK):**
```json
{
  "message": "string"
}
```

**Response Field Definitions:**
- `message`: Confirmation message of successful logout

**Error Responses:**
- `401 Unauthorized`: Missing or invalid authentication token
- `500 Internal Server Error`: Server error processing the request

## Data Types

### User Object
- `id` (string): Unique identifier for the user
- `email` (string): User's email address
- `username` (string): User's chosen username
- `created_at` (string): ISO 8601 date string
- `updated_at` (string): ISO 8601 date string

### Login Request
- `email` (string): User's email address
- `password` (string): User's password

### Login Response
- `access_token` (string): JWT token for authenticated requests
- `token_type` (string): Type of token (usually "bearer")
- `user` (object): User object as defined above

### Register Request
- `email` (string): User's email address
- `username` (string): Desired username
- `password` (string): Desired password

### Register Response
- `id` (string): Unique identifier for the created user
- `email` (string): User's email address
- `username` (string): User's chosen username

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
- `409`: Conflict - Resource already exists (e.g., duplicate email/username)
- `422`: Unprocessable Entity - Valid request format but semantic errors
- `500`: Internal Server Error - Server-side processing error

## Security
- Passwords must be transmitted over HTTPS only
- JWT tokens should have appropriate expiration times
- All sensitive authentication data must be properly encrypted
- Authentication endpoints should implement rate limiting

## Rate Limiting
Authentication endpoints may be subject to rate limiting to prevent brute force attacks.

## Testing
When testing, ensure the backend authentication service is running and accessible at the configured base URL.