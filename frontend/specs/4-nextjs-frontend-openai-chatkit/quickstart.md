# Quickstart Guide: Frontend — Next.js 16 + OpenAI ChatKit

## Prerequisites

- Node.js v18 or higher
- npm or yarn package manager
- Access to FastAPI backend at `http://localhost:8000`
- Better Auth configured on the backend

## Setup Instructions

### 1. Clone and Initialize the Project

```bash
# Navigate to the frontend directory
cd frontend

# Install dependencies
npm install
```

### 2. Configure Environment Variables

Create a `.env.local` file in the project root:

```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
NEXT_PUBLIC_CHAT_ENDPOINT=/api
AUTH_URL=http://localhost:8000
```

### 3. Run the Development Server

```bash
npm run dev
```

The application will be available at `http://localhost:3000`

## Key Files

### Authentication
- `app/login/page.tsx` — Login form with Better Auth integration
- `contexts/auth-context.tsx` — Authentication state management

### Chat Interface
- `app/chat/page.tsx` — Main chat interface with OpenAI ChatKit
- `contexts/chat-context.tsx` — Chat state management
- `components/chat/ChatInterface.tsx` — OpenAI ChatKit wrapper

### API Integration
- `utils/api.ts` — API service functions
- `app/api/auth/login/route.ts` — Authentication API route
- `app/api/chat/route.ts` — Chat API route

## API Endpoints Used

### Chat Endpoint
- **Method**: POST
- **URL**: `/api/{user_id}/chat`
- **Request Body**:
  ```json
  {
    "message": "string",
    "conversation_id": "number (optional)"
  }
  ```
- **Response**:
  ```json
  {
    "conversation_id": "number",
    "response": "string",
    "tool_calls": "string[]"
  }
  ```

### Authentication Endpoints
- Login: `POST /api/login`
- Register: `POST /api/register`
- Get Current User: `GET /api/me`

## Running in Production

```bash
# Build the application
npm run build

# Run the production server
npm run start
```

## Testing

```bash
# Run tests
npm test

# Run linting
npm run lint
```

## Common Commands

```bash
# Development server
npm run dev

# Build for production
npm run build

# Run production server
npm run start

# Run tests
npm test

# Run linter
npm run lint

# Run type checker
npm run type-check
```

## Troubleshooting

### Common Issues

1. **Authentication not working**
   - Verify backend authentication endpoints are accessible
   - Check environment variables are properly set

2. **ChatKit not loading**
   - Verify OpenAI ChatKit dependencies are properly installed
   - Check network connectivity to OpenAI services

3. **API connection errors**
   - Confirm backend server is running at specified URL
   - Check CORS settings on the backend

### Development Tips

- Use `console.log` statements to debug API communication
- Check browser developer tools for network errors
- Verify that all required environment variables are set
- Ensure backend server is running before starting frontend

### Getting Help

- Check the main README for detailed setup instructions
- Review the API documentation for backend endpoints
- Consult the Next.js documentation for framework-specific issues