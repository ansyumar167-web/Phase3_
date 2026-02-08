# Implementation Plan: Backend API, Database, Stateless Chat, and Authentication

**Feature**: 2-backend-api-auth
**Created**: 2026-01-16
**Status**: Draft

## Technical Context

This plan implements a stateless chat API with authentication using FastAPI, Neon PostgreSQL with SQLModel, and Better Auth. The system will provide a POST /api/{user_id}/chat endpoint that authenticates users, reconstructs conversation history from the database, and persists messages without storing any state in memory.

### Architecture Overview

- **Backend**: Python FastAPI application
- **Database**: Neon Serverless PostgreSQL with SQLModel ORM
- **Authentication**: Better Auth integration
- **State Management**: Stateless - all state stored in database
- **API Contract**: POST /api/{user_id}/chat with conversation persistence

### Components to Implement

1. **Database Layer**: SQLModel schemas for User, Conversation, and Message entities
2. **Authentication Layer**: Better Auth integration with FastAPI
3. **API Layer**: Stateless chat endpoint with conversation reconstruction
4. **Data Access Layer**: Repository patterns for database operations
5. **Error Handling**: Proper error responses for edge cases

## Constitution Check

### Compliance Verification

- ✅ **Stateless Architecture**: Plan ensures no in-memory state storage - all conversation context retrieved from database
- ✅ **Database-Backed Persistence**: All state stored in Neon PostgreSQL with SQLModel
- ✅ **Technology Stack**: Uses required technologies (FastAPI, SQLModel, Neon, Better Auth)
- ✅ **MCP Tool Compatibility**: Designed to integrate with MCP tools for AI agent interactions
- ✅ **Auditability**: All operations will be logged for traceability

### Gate Requirements

- [ ] Authentication enforced on all endpoints
- [ ] User ID validation to prevent cross-user access
- [ ] Database transactions for atomic operations
- [ ] Proper error handling for edge cases
- [ ] Stateless operation verified

## Phase 0: Research & Discovery

### Research Tasks

1. **Better Auth Integration with FastAPI**
   - Best practices for integrating Better Auth with FastAPI
   - Middleware patterns for authentication
   - Token validation approaches

2. **SQLModel Schema Design Patterns**
   - Optimal schema design for conversation and message entities
   - Relationship definitions between entities
   - Indexing strategies for performance

3. **Stateless Conversation Handling**
   - Efficient methods for reconstructing conversation history
   - Caching considerations (if any) for conversation data
   - Performance optimization for large conversation histories

### Assumptions Resolved

- **Database Connection**: Will use async database connections with Neon PostgreSQL
- **Session Management**: Will leverage FastAPI's dependency injection for database sessions
- **Authentication Method**: Will use Better Auth's middleware approach with token validation
- **Request/Response Format**: Will follow standard JSON API patterns with proper error responses

## Phase 1: Design & Contracts

### Data Model: data-model.md

#### Entity: User
- **Fields**:
  - id (str): Unique user identifier from Better Auth
  - created_at (datetime): Timestamp of user creation
  - updated_at (datetime): Timestamp of last update

#### Entity: Conversation
- **Fields**:
  - id (int): Auto-incrementing primary key
  - user_id (str): Foreign key linking to User.id
  - created_at (datetime): Timestamp of conversation creation
  - updated_at (datetime): Timestamp of last activity

#### Entity: Message
- **Fields**:
  - id (int): Auto-incrementing primary key
  - user_id (str): Foreign key linking to User.id
  - conversation_id (int): Foreign key linking to Conversation.id
  - role (str): Enum of 'user' or 'assistant'
  - content (str): Message content (text)
  - created_at (datetime): Timestamp of message creation

### API Contracts: contracts/

#### Endpoint: POST /api/{user_id}/chat

**Description**: Handles chat requests from authenticated users and manages conversation persistence.

**Request**:
- Path Parameter: `user_id` (string) - Authenticated user identifier
- Body:
  ```json
  {
    "conversation_id": "optional integer",
    "message": "required string"
  }
  ```

**Response (Success)**:
```json
{
  "conversation_id": "integer",
  "response": "string",
  "tool_calls": "array of objects (optional)"
}
```

**Response (Error)**:
- 401: Unauthorized (invalid/missing authentication)
- 403: Forbidden (user_id mismatch)
- 422: Unprocessable Entity (validation error)
- 500: Internal Server Error (database connectivity issues)

**Authentication**: Bearer token via Better Auth

### Quickstart Guide: quickstart.md

#### Setup Instructions

1. **Environment Setup**
   ```bash
   # Install dependencies
   pip install fastapi uvicorn sqlmodel python-multipart

   # Install Better Auth
   pip install better-fastapi

   # Install async database driver
   pip install asyncpg
   ```

2. **Database Configuration**
   ```python
   # Configure database URL for Neon
   DATABASE_URL = "postgresql+asyncpg://..."

   # Initialize SQLModel engine
   engine = create_async_engine(DATABASE_URL)
   ```

3. **Better Auth Configuration**
   ```python
   from better_auth import Auth, User

   # Initialize auth with Neon database
   auth = Auth(
       secret="your-secret-key",
       db_url=DATABASE_URL
   )
   ```

4. **Run Application**
   ```bash
   uvicorn main:app --reload
   ```

## Phase 2: Implementation Plan

### Week 1: Database Layer & Models

**Tasks**:
- [ ] Create SQLModel entity definitions
- [ ] Implement database session management
- [ ] Set up database initialization and migrations
- [ ] Write basic CRUD operations for entities

**Deliverables**:
- database/models.py
- database/session.py
- database/init.py
- database/crud.py

### Week 2: Authentication Layer

**Tasks**:
- [ ] Integrate Better Auth with FastAPI
- [ ] Implement authentication middleware
- [ ] Create user validation utilities
- [ ] Test authentication flows

**Deliverables**:
- auth/middleware.py
- auth/utils.py
- auth/schemas.py

### Week 3: API Layer & Business Logic

**Tasks**:
- [ ] Implement POST /api/{user_id}/chat endpoint
- [ ] Create conversation history reconstruction logic
- [ ] Implement message persistence logic
- [ ] Add error handling for edge cases

**Deliverables**:
- api/v1/chat.py
- services/conversation_service.py
- services/message_service.py

### Week 4: Testing & Integration

**Tasks**:
- [ ] Write unit tests for all components
- [ ] Create integration tests for the API
- [ ] Test stateless behavior across server restarts
- [ ] Performance testing for conversation retrieval

**Deliverables**:
- tests/test_chat_api.py
- tests/test_authentication.py
- tests/test_conversation_persistence.py

## Risk Assessment

### High-Risk Areas
- **Database Performance**: Large conversation histories could impact retrieval performance
- **Authentication Security**: Ensuring user_id validation to prevent cross-user access
- **Stateless Operation**: Verifying no session state is maintained between requests

### Mitigation Strategies
- **Indexing**: Proper database indexes on foreign keys and timestamps
- **Validation**: Strict user_id validation in all endpoints
- **Testing**: Comprehensive testing to verify stateless behavior

## Success Metrics

- [ ] All authenticated requests processed successfully (SC-001)
- [ ] Unauthorized requests rejected with 401 (SC-002)
- [ ] Conversation history reconstructed for all requests (SC-003)
- [ ] Message persistence achieves 99.9% success rate (SC-004)
- [ ] Conversations survive server restarts (SC-005)
- [ ] API format compliance verified (SC-006)
- [ ] Stateless operation confirmed (SC-007)