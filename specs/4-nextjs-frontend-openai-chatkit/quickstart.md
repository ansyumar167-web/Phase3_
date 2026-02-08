# Quickstart Guide: Frontend — Next.js 16 + OpenAI ChatKit

## Prerequisites

- Node.js v18 or higher
- npm or yarn package manager
- Access to FastAPI backend at `http://localhost:8000`
- Better Auth configured on the backend

## Setup Instructions

### 1. Clone and Initialize the Project

```bash
# Create frontend directory
mkdir frontend
cd frontend

# Initialize Next.js project
npx create-next-app@latest . --typescript --tailwind --eslint --app --src-dir --import-alias "@/*"
```

### 2. Install Required Dependencies

```bash
# Install core dependencies
npm install @openai/chatkit-react
npm install better-auth
npm install @better-auth/react

# Install additional utilities if needed
npm install zustand  # For state management (optional)
npm install axios   # For API calls (optional)
```

### 3. Configure Environment Variables

Create a `.env.local` file in the project root:

```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
NEXT_PUBLIC_CHAT_ENDPOINT=/api
AUTH_URL=http://localhost:8000
```

### 4. Set Up Authentication

Create `src/lib/auth.ts`:

```typescript
import { createAuth } from "@better-auth/react";

export const auth = createAuth({
  baseURL: process.env.AUTH_URL || "http://localhost:8000",
  // Add your auth configuration here
});
```

### 5. Create Directory Structure

```bash
# Create necessary directories
mkdir -p src/app/{login,chat,components,lib,styles,types,utils}
mkdir -p src/app/chat/components
```

### 6. Run the Development Server

```bash
npm run dev
```

The application will be available at `http://localhost:3000`

## Key Files to Implement

### 1. Authentication Provider
- Location: `src/providers/AuthProvider.tsx`
- Purpose: Wrap application with authentication context

### 2. Main Layout
- Location: `src/app/layout.tsx`
- Purpose: Root layout with global styles and providers

### 3. Login Page
- Location: `src/app/login/page.tsx`
- Purpose: User authentication interface

### 4. Chat Interface
- Location: `src/app/chat/page.tsx`
- Purpose: Main chatbot interface with OpenAI ChatKit

### 5. Chat Components
- Location: `src/app/chat/components/`
- Purpose: Reusable chat interface components

## API Integration

### Chat Endpoint
- Method: `POST`
- URL: `/api/{user_id}/chat`
- Request Body:
  ```json
  {
    "message": "string",
    "conversation_id": "number (optional)"
  }
  ```
- Response:
  ```json
  {
    "conversation_id": "number",
    "response": "string",
    "tool_calls": "string[]"
  }
  ```

## Common Commands

```bash
# Run development server
npm run dev

# Build for production
npm run build

# Run production build locally
npm run start

# Run tests
npm run test

# Lint code
npm run lint
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

### Getting Help

- Check the main README for detailed setup instructions
- Review the API documentation for backend endpoints
- Consult the Next.js documentation for framework-specific issues