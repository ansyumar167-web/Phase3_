# Implementation Plan: Frontend — Next.js 16 + OpenAI ChatKit

## Feature Specification
**Spec File:** C:\Users\SS Computer\Desktop\hackhathon_2\specs\4-nextjs-frontend-openai-chatkit\spec.md

## Technical Context

### Architecture Overview
- **Frontend Framework**: Next.js 16 with App Router
- **Chat UI**: OpenAI ChatKit
- **Authentication**: Better Auth integration
- **Styling**: Tailwind CSS
- **Build Tool**: Next.js default tooling only
- **Backend Integration**: FastAPI endpoints for chat functionality

### Dependencies
- Next.js 16
- OpenAI ChatKit
- Better Auth SDK
- Tailwind CSS
- React (v18+)
- Node.js (v18+)

### Integration Points
- **Backend API**: FastAPI chat endpoint at `/api/{user_id}/chat`
- **Authentication**: Better Auth endpoints for login/logout
- **Database**: Indirect access through backend MCP tools

### Known Constraints
- Must use Next.js App Router (not Pages Router)
- Chat UI must be implemented in Client Component
- No Vite or alternative bundlers allowed
- Frontend must not store authoritative chat state
- All task operations must go through backend MCP tools

## Constitution Check

### Architecture Principles
- ✅ **Separation of Concerns**: Frontend handles UI, backend handles business logic
- ✅ **API-First Design**: All data operations through backend APIs
- ✅ **Security First**: Authentication handled through proper channels
- ✅ **Responsive Design**: Mobile-first approach with Tailwind CSS

### Technical Principles
- ✅ **Client-Side Rendering**: For interactive chat components
- ✅ **Type Safety**: Use TypeScript for better development experience
- ✅ **Performance**: Optimized bundle sizes and loading states
- ✅ **Accessibility**: Proper ARIA labels and keyboard navigation

### Compliance Check
- ✅ **No Direct Database Access**: All operations through backend
- ✅ **State Management**: Backend remains source of truth
- ✅ **Authentication**: Proper integration with Better Auth
- ✅ **Error Handling**: User-friendly error messages

## Gates

### Gate 1: Architecture Feasibility
- **Status**: ✅ PASS
- **Verification**: Next.js 16 with App Router supports required features
- **Dependencies**: All required packages are available and compatible

### Gate 2: Integration Feasibility
- **Status**: ✅ PASS
- **Verification**: FastAPI backend endpoints are documented and accessible
- **Dependencies**: Backend authentication and chat endpoints are available

### Gate 3: Security Review
- **Status**: ✅ PASS
- **Verification**: No sensitive data stored on frontend, proper auth flow
- **Dependencies**: Better Auth provides secure authentication mechanism

### Gate 4: Performance Considerations
- **Status**: ✅ PASS
- **Verification**: Client-side chat interface will provide responsive experience
- **Dependencies**: Backend API response times are acceptable for chat experience

## Phase 0: Research & Requirements Resolution

### Research Task 1: Next.js 16 App Router Implementation
**Objective**: Determine best practices for implementing authentication guards in Next.js 16 App Router
**Outcome**: Use `auth.js` middleware for route protection and React Context for auth state management

### Research Task 2: OpenAI ChatKit Integration
**Objective**: Research how to properly integrate OpenAI ChatKit with Next.js 16 and TypeScript
**Outcome**: ChatKit components work well with Client Components; proper props and event handling needed

### Research Task 3: Better Auth Integration Patterns
**Objective**: Determine optimal patterns for integrating Better Auth with Next.js App Router
**Outcome**: Use Better Auth's React hooks for client-side auth state management with server-side validation

### Research Task 4: Conversation State Management
**Objective**: Determine best practices for persisting conversation ID across page refreshes
**Outcome**: Use localStorage for client-side conversation ID persistence while backend remains authoritative

## Phase 1: Design & Contracts

### Data Model: Frontend State Management
```typescript
// User authentication state
interface AuthState {
  user: User | null;
  isLoading: boolean;
  isAuthenticated: boolean;
}

// Chat conversation state
interface ChatState {
  messages: Message[];
  conversationId: number | null;
  isLoading: boolean;
  error: string | null;
}

// Message structure
interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: string; // Using string to avoid serialization issues
}
```

### API Contracts: Frontend-Backend Communication
```typescript
// Request to backend chat endpoint
interface ChatRequest {
  message: string;
  conversation_id?: number;
}

// Response from backend chat endpoint
interface ChatResponse {
  conversation_id: number;
  response: string;
  tool_calls: string[];
}

// Error response structure
interface ErrorResponse {
  error: string;
  status: number;
}
```

### Component Architecture
```
app/
├── layout.tsx              // Root layout with global styles
├── page.tsx               // Redirect to /login or /chat based on auth
├── login/                 // Authentication pages
│   ├── page.tsx           // Login form
│   └── layout.tsx         // Login-specific layout
└── chat/                  // Chat application
    ├── page.tsx           // Main chat interface
    ├── layout.tsx         // Chat-specific layout
    └── components/        // Chat-related components
        ├── ChatInterface.tsx    // OpenAI ChatKit wrapper
        ├── MessageHistory.tsx   // Message display component
        └── TaskConfirmation.tsx // Task action confirmations
```

### Quickstart Guide
1. Clone the repository
2. Install dependencies: `npm install`
3. Set environment variables for backend API URL
4. Run development server: `npm run dev`
5. Access application at `http://localhost:3000`

## Phase 2: Implementation Approach

### Sprint 1: Project Setup and Authentication
- Initialize Next.js 16 project with App Router
- Install and configure Tailwind CSS
- Set up Better Auth integration
- Create protected route middleware
- Implement login page

### Sprint 2: Chat Interface Foundation
- Create Client Component for ChatKit integration
- Implement basic message sending/receiving
- Connect to backend chat API
- Handle loading and error states

### Sprint 3: Conversation Continuity
- Implement conversation ID persistence
- Add page refresh recovery
- Ensure backend remains authoritative
- Add proper error handling for network issues

### Sprint 4: Task Action Handling
- Implement natural language command recognition
- Add task action confirmations
- Create user feedback mechanisms
- Polish UI/UX experience

### Sprint 5: Testing and Optimization
- Test all user scenarios
- Optimize performance
- Add accessibility features
- Final polish and documentation