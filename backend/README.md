# AI-Powered Todo Chatbot Backend

This is a FastAPI-based backend for an AI-powered todo management application that uses natural language processing to manage tasks through an intelligent chat interface.

## Features

- **Natural Language Processing**: Interact with your todo list using natural language
- **Secure Authentication**: JWT-based authentication with Better Auth integration
- **Database Persistence**: Neon Serverless PostgreSQL with SQLModel ORM
- **Stateless Architecture**: Conversation state stored in database, no in-memory state
- **Rate Limiting**: Built-in rate limiting to prevent abuse
- **Comprehensive Logging**: Detailed logging for audit trails and debugging
- **Error Handling**: Robust error handling with appropriate HTTP status codes
- **Health Checks**: Health check endpoint for monitoring

## Tech Stack

- **Backend**: FastAPI
- **Database**: Neon Serverless PostgreSQL with SQLModel
- **Authentication**: Better Auth
- **AI Integration**: OpenAI API with function calling
- **Model Context Protocol**: MCP for AI tool integration
- **Async Support**: Full async/await support

## Setup

### Prerequisites

- Python 3.9+
- PostgreSQL database (or Neon account)

### Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables in `.env`:
   ```env
   # Database settings
   DATABASE_URL=postgresql://username:password@host:port/database_name

   # Authentication
   SECRET_KEY=your-super-secret-key-here
   ALGORITHM=HS256

   # OpenAI settings
   OPENAI_API_KEY=your-openai-api-key
   OPENAI_MODEL=gpt-4-turbo-preview

   # Application settings
   APP_NAME=Todo AI Agent
   VERSION=0.1.0
   DEBUG=true
   ```

4. Initialize the database:
   ```bash
   python -m src.database.init
   ```

5. Run the application:
   ```bash
   uvicorn src.api.chat_endpoint:app --reload
   ```

## API Endpoints

### Chat Endpoint
- `POST /api/{user_id}/chat` - Process natural language messages and manage tasks

**Request Body:**
```json
{
  "message": "string (required)",
  "conversation_id": "integer (optional)"
}
```

**Response:**
```json
{
  "conversation_id": "integer",
  "response": "string",
  "tool_calls": "array of strings"
}
```

### Health Check
- `GET /api/health` - Check if the API is running

## Authentication

All API endpoints require authentication using JWT tokens in the Authorization header:
```
Authorization: Bearer <jwt_token>
```

The user_id in the URL path must match the authenticated user's ID, or a 403 Forbidden error will be returned.

## Rate Limiting

The API implements rate limiting:
- 60 requests per minute per user per endpoint
- 1000 requests per hour per user per endpoint

Exceeding these limits will result in a 429 Too Many Requests response.

## Error Handling

The API returns appropriate HTTP status codes:
- `200` - Success
- `400` - Bad Request
- `401` - Unauthorized (missing or invalid token)
- `403` - Forbidden (user_id mismatch)
- `404` - Not Found
- `422` - Unprocessable Entity (validation error)
- `429` - Too Many Requests (rate limit exceeded)
- `500` - Internal Server Error

## Logging

All API requests and errors are logged for audit and debugging purposes:
- API request logs include user_id, endpoint, and status
- Error logs include detailed exception information
- Audit logs track user actions

## Architecture

The application follows a stateless architecture:
1. Each request reconstructs conversation history from the database
2. User messages are stored in the database
3. AI responses are stored in the database
4. No in-memory state is maintained between requests

## Development

To run tests:
```bash
pytest
```

To format code:
```bash
black .
```

To lint code:
```bash
flake8 .
```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `DATABASE_URL` | Database connection string | Yes |
| `SECRET_KEY` | Secret key for JWT signing | Yes |
| `OPENAI_API_KEY` | OpenAI API key | Yes |
| `OPENAI_MODEL` | OpenAI model to use | No (default: gpt-4-turbo-preview) |
| `DEBUG` | Enable debug mode | No (default: false) |

## Production Deployment

For production deployment:
1. Set `DEBUG=false`
2. Use a strong `SECRET_KEY`
3. Set up proper logging aggregation
4. Configure a reverse proxy (nginx, Apache)
5. Set up SSL certificates
6. Monitor rate limits and adjust as needed
