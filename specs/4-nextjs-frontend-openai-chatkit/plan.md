# Implementation Plan: Frontend — Next.js 16 + OpenAI ChatKit

**Branch**: `4-nextjs-frontend-openai-chatkit` | **Date**: 2026-01-18 | **Spec**: [link]
**Input**: Feature specification from `/specs/4-nextjs-frontend-openai-chatkit/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Build a production-ready frontend using **Next.js 16** that provides a conversational chatbot UI powered by **OpenAI ChatKit**, fully integrated with the FastAPI backend. The frontend will allow authenticated users to manage todos through natural language while preserving conversation continuity via backend persistence.

## Technical Context

**Language/Version**: TypeScript with React 18, Next.js 16
**Primary Dependencies**: Next.js 16, OpenAI ChatKit, Better Auth, Tailwind CSS
**Storage**: Client-side (localStorage/sessionStorage) for conversation continuity, backend database authoritative
**Testing**: Jest, React Testing Library
**Target Platform**: Web application, responsive for desktop and mobile
**Project Type**: Web - frontend application with backend integration
**Performance Goals**: Page load time under 3 seconds, chat response time under 5 seconds
**Constraints**: Must use Next.js App Router, Chat UI in Client Components, no Vite bundler, backend remains authoritative for data
**Scale/Scope**: Individual user task management, multiple concurrent users supported by backend

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

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

## Project Structure

### Documentation (this feature)

```text
specs/4-nextjs-frontend-openai-chatkit/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
frontend/
├── app/
│   ├── layout.tsx              # Root layout with global styles
│   ├── page.tsx                # Redirect to /login or /chat based on auth
│   ├── login/                  # Authentication pages
│   │   ├── page.tsx            # Login form
│   │   └── layout.tsx          # Login-specific layout
│   └── chat/                   # Chat application
│       ├── page.tsx            # Main chat interface
│       ├── layout.tsx          # Chat-specific layout
│       └── components/         # Chat-related components
│           ├── ChatInterface.tsx       # OpenAI ChatKit wrapper
│           ├── MessageHistory.tsx      # Message display component
│           └── TaskConfirmation.tsx    # Task action confirmations
├── components/                 # Reusable UI components
├── lib/                       # Utilities and shared functions
├── styles/                    # Global styles and Tailwind configuration
├── types/                     # TypeScript type definitions
└── public/                    # Static assets
```

**Structure Decision**: Web application structure with Next.js App Router, separating authentication and chat functionality into distinct route groups.

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

## Phase 1: Implementation Plan

### 1. Project Setup
- Initialize Next.js 16 project
- Install dependencies:
  - OpenAI ChatKit
  - Tailwind CSS (optional)
  - Better Auth SDK

### 2. Authentication Integration
- Implement login page with Better Auth
- Protect `/chat` route
- Attach `user_id` to all API requests

### 3. Chat UI Implementation
- Create ChatKit component in **Client Component**
- Render user messages and assistant responses
- Show confirmations for task actions (add, update, complete, delete)
- Handle loading and error states

### 4. Backend Connection
- Connect ChatKit input to:
  - Send:
    - `message`
    - Optional `conversation_id`
  - Receive and render:
    - AI response
    - Updated `conversation_id`
    - MCP tool calls

### 5. Conversation Continuity
- Persist `conversation_id` on client
- Resume conversation after refresh/reload
- Ensure backend database remains authoritative

### 6. UX & Error Handling
- Disable input while waiting for AI response
- Show loading indicators
- Display success confirmations for tasks
- Display clear, user-friendly error messages

### 7. Testing & Verification
- Test all natural language commands:
  - Add, list, complete, update, delete tasks
- Verify conversation continuity
- Validate integration with FastAPI backend
- Confirm no Vite usage or frontend-only state

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
