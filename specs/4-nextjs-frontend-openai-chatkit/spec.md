# Spec 4: Frontend — Next.js 16 + OpenAI ChatKit

## Objective
Build a production-ready frontend using **Next.js 16** that provides a conversational chatbot UI powered by **OpenAI ChatKit**, fully integrated with the FastAPI backend. The frontend must allow authenticated users to manage todos through natural language while preserving conversation continuity via backend persistence.

## Summary
Create a modern Next.js 16 application with OpenAI ChatKit integration that serves as the frontend for the AI-powered todo chatbot. The application will include authentication via Better Auth and provide a seamless conversational interface for task management.

## Context
The backend system is already implemented with FastAPI, MCP tools, and database persistence. The frontend will serve as the primary user interface, enabling users to interact with the AI agent through natural language commands to manage their todo lists.

## Scope
### In Scope
- Next.js 16 application with App Router
- OpenAI ChatKit integration for chat interface
- Better Auth integration for user authentication
- API integration with FastAPI backend endpoints
- Conversation continuity with client-side conversation ID persistence
- Protected routes for authenticated users only
- Error handling and loading states
- Responsive design for multiple device sizes

### Out of Scope
- Backend implementation (already exists)
- Database design (already implemented)
- MCP server implementation (already exists)
- Direct database access from frontend
- Custom chat UI (using OpenAI ChatKit)

## Assumptions
- FastAPI backend is running at `http://localhost:8000`
- Chat endpoint is available at `/api/{user_id}/chat`
- Authentication endpoints are available via Better Auth
- Backend handles all task business logic through MCP tools
- User ID is available through authentication context

## Success Criteria
- Frontend is built using **Next.js 16** with App Router
- OpenAI ChatKit is used for all chat interactions
- Frontend communicates correctly with the FastAPI chat endpoint
- Conversations resume correctly after refresh
- Todos are fully manageable via natural language
- All pages are responsive and work on different screen sizes
- Authentication flow works correctly with Better Auth
- Error handling is user-friendly and informative
- Page load times are under 3 seconds
- 95% of user tasks complete successfully without errors

## Key Entities
- **User**: Authenticated user with unique ID
- **Conversation**: Chat session with unique identifier
- **Message**: Individual chat message (user or assistant)
- **Task**: Todo item managed through natural language

## Functional Requirements

### FR1: Authentication System
**Requirement**: The application must integrate Better Auth for user authentication.
- **Acceptance Criteria**:
  - Users can access `/login` page to authenticate
  - Unauthenticated users are redirected from `/chat` to `/login`
  - Authenticated users can access the `/chat` page
  - User authentication state persists across browser sessions
  - Logout functionality is available

### FR2: Chat Interface
**Requirement**: The application must use OpenAI ChatKit for the primary chat UI.
- **Acceptance Criteria**:
  - User messages are displayed in the chat interface
  - Assistant responses are displayed in the chat interface
  - Messages are properly formatted and distinguishable
  - Chat history is visible during the session
  - Input field is available for new messages

### FR3: Natural Language Task Commands
**Requirement**: The chat interface must support natural language task commands.
- **Acceptance Criteria**:
  - Users can add tasks using phrases like "Add a task to buy groceries"
  - Users can list tasks using phrases like "Show me my tasks"
  - Users can complete tasks using phrases like "Mark task 1 as complete"
  - Users can delete tasks using phrases like "Delete the meeting task"
  - System confirms task actions appropriately

### FR4: API Integration
**Requirement**: The frontend must communicate with the FastAPI backend.
- **Acceptance Criteria**:
  - Chat messages are sent to the backend API endpoint
  - User ID is correctly passed in API calls
  - Conversation ID is persisted and included in requests
  - Responses from backend are properly displayed
  - Error responses from backend are handled gracefully

### FR5: Conversation Continuity
**Requirement**: The application must maintain conversation context.
- **Acceptance Criteria**:
  - Conversation ID is stored client-side (localStorage/sessionStorage)
  - Same conversation is resumed after page refresh
  - Chat history persists during the same session
  - New conversations start with a new conversation ID
  - Backend remains the single source of truth for conversation data

### FR6: Loading and Error States
**Requirement**: The application must handle loading and error states appropriately.
- **Acceptance Criteria**:
  - Loading indicators appear while waiting for AI response
  - Input field is disabled during AI processing
  - Clear error messages are displayed for HTTP errors
  - Users can retry failed operations
  - Network errors are handled gracefully

### FR7: Protected Routes
**Requirement**: The application must protect certain routes based on authentication.
- **Acceptance Criteria**:
  - `/chat` route requires authentication
  - Unauthenticated users are redirected to `/login`
  - Authenticated users can access protected routes
  - Authentication state is checked before rendering protected content

## User Scenarios & Testing

### Scenario 1: New User Registration and Task Creation
**Actor**: New user
**Goal**: Create account and add first task using natural language
1. User navigates to `/login` page
2. User registers with email and password
3. User is redirected to `/chat` page after successful registration
4. User types "Add a task to buy groceries" in the chat input
5. Message is sent to backend and displayed in chat
6. AI responds confirming the task was added
7. User sees confirmation that task was created

### Scenario 2: Returning User Continuing Conversation
**Actor**: Returning user
**Goal**: Continue previous conversation after browser refresh
1. User opens browser and visits `/chat`
2. User authentication is validated automatically
3. Previous conversation is resumed with same conversation ID
4. User can continue the conversation from where they left off
5. New messages are appended to the existing conversation

### Scenario 3: Task Management with Natural Language
**Actor**: Authenticated user
**Goal**: Manage multiple tasks using natural language commands
1. User accesses `/chat` page
2. User types "Add a task to call mom"
3. AI confirms task was added
4. User types "Show me all my tasks"
5. AI lists all tasks including the newly added one
6. User types "Mark the call mom task as complete"
7. AI confirms the task is marked as complete
8. User types "Delete the call mom task"
9. AI confirms the task was deleted

### Scenario 4: Error Handling
**Actor**: Authenticated user
**Goal**: Recover from network errors during chat
1. User is chatting and submits a message
2. Network error occurs preventing API call
3. User sees friendly error message
4. User has option to retry the operation
5. Upon network restoration, user can continue chatting

## Non-Functional Requirements

### Performance
- Page load time under 3 seconds on average connection
- Chat response time under 5 seconds for typical requests
- Minimal delay between user input and message display

### Usability
- Intuitive natural language interface
- Clear feedback for all user actions
- Mobile-responsive design for all screen sizes
- Keyboard navigation support

### Security
- User authentication required for all features
- No sensitive information exposed in client code
- Proper validation of backend responses
- Secure transmission of all data

### Compatibility
- Modern browsers (Chrome, Firefox, Safari, Edge)
- Mobile and desktop devices
- Screen reader accessibility support