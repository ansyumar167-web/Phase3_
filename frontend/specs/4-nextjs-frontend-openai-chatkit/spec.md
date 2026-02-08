# Spec 4: Frontend — Next.js 16 + OpenAI ChatKit

## Objective
Build a production-ready frontend using **Next.js 16** that provides a conversational chatbot UI powered by **OpenAI ChatKit**, fully integrated with the FastAPI backend. The frontend must allow authenticated users to manage todos through natural language while preserving conversation continuity via backend persistence.

---

## Technology Stack (Strict)

- **Framework:** Next.js 16
  - App Router
  - React Server Components supported
  - Chat UI implemented using **Client Components**
- **Chat UI:** OpenAI ChatKit
- **Authentication:** Better Auth (frontend integration)
- **Styling:** Optional (Tailwind CSS recommended)
- **Build Tool:** Next.js default tooling only
  - ❌ Vite is NOT allowed
  - ❌ Any alternative bundler is NOT allowed

---

## Application Routes

### Required Pages
- `/login` — Authentication page
- `/chat` — Main chatbot interface (protected route)

---

## API Integration

### Chat Endpoint

**Endpoint**

**Request Body**
- `message` (string, required): User's natural language message
- `conversation_id` (number, optional): Existing conversation identifier

**Response Body**
- `conversation_id` (number): Active conversation ID
- `response` (string): AI assistant reply
- `tool_calls` (array): MCP tools invoked (if any)

---

## Functional Requirements

### 1. Chat Interface
- Use **OpenAI ChatKit** as the primary chat UI
- Render:
  - User messages
  - Assistant messages
- Support natural language task commands
- Display confirmations for task actions (add, update, complete, delete)

---

### 2. Authentication Handling
- Integrate Better Auth on the frontend
- Ensure:
  - Only authenticated users can access `/chat`
  - Correct `user_id` is used for all API calls
- Handle authentication states:
  - Loading
  - Unauthenticated (redirect to `/login`)
  - Authenticated

---

### 3. Conversation Continuity
- Persist `conversation_id` on the client
- Include `conversation_id` in subsequent chat requests
- Resume conversations after:
  - Page refresh
  - Browser reload
- Backend database remains the **single source of truth**

---

### 4. State Management Constraints
- Frontend must NOT store authoritative chat state
- Frontend must NOT implement task business logic
- Frontend must NOT replicate backend rules
- All task operations must occur through backend MCP tools

---

### 5. UX Requirements
- Disable input while waiting for AI response
- Show loading indicators during processing
- Display clear success confirmations
- Display clear, user-friendly error messages

---

## Error Handling

### Frontend Behavior
- Handle HTTP errors gracefully:
  - `401` → redirect to login
  - `403` → show access denied
  - `500` → show retry option
- Do NOT expose internal backend or agent errors directly to the user

---

## Security Requirements
- Never expose API keys on the frontend
- Do not allow manual manipulation of `user_id`
- Validate backend responses before rendering

---

## Non-Goals (Explicit)
- ❌ Using Vite or any custom bundler
- ❌ Replacing ChatKit with a custom chat UI
- ❌ Frontend-side task persistence
- ❌ Direct database access from frontend

---

## Success Criteria
- Frontend is built using **Next.js 16**
- OpenAI ChatKit is used for all chat interactions
- Frontend communicates correctly with the FastAPI chat endpoint
- Conversations resume correctly after refresh
- Todos are fully manageable via natural language
- No Vite usage exists anywhere in the frontend