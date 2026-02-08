<!-- SYNC IMPACT REPORT:
Version change: 1.0.0 → 1.1.0
Modified principles: Updated all core principles to reflect enhanced requirements
Added sections: None
Removed sections: None
Templates requiring updates: ⚠ pending review of .specify/templates/plan-template.md, .specify/templates/spec-template.md, .specify/templates/tasks-template.md
Follow-up TODOs: None
-->
# Odo AI Chatbot Constitution
<!-- MCP-based Agentic Todo Management System -->

## Core Principles

### I. Spec-Driven Development
Spec-driven development (spec → plan → tasks → code) is mandatory. All system behavior must be defined in written specifications before implementation. This ensures clarity, testability, and alignment with requirements. All implementation must be generated from specifications, with no manual coding without prior specification.

### II. Stateless Architecture
All system components must maintain stateless architecture with persistent database state. Backend servers must not store conversational state in memory. Conversation context must be persisted in the database for stateless behavior across server restarts. Database-backed persistence is mandatory for all state, and conversation context must be retrievable from the database.

### III. Deterministic AI Behavior
AI behavior must be deterministic through explicit tool contracts. Natural language commands must map deterministically to MCP tool calls. AI agents may only modify data via MCP tools, ensuring auditability and consistency. MCP tools must be stateless and idempotent, and all agent actions must be auditable with every tool invocation logged and traceable.

### IV. Clear Separation of Concerns
Maintain clear separation of concerns across system components. Each component (frontend, backend, database, authentication) must have well-defined responsibilities and interfaces. The technology stack requirements mandate specific technologies: Frontend (OpenAI ChatKit), Backend (Python FastAPI), AI Framework (OpenAI Agents SDK), MCP Server (Official MCP SDK), Database (Neon Serverless PostgreSQL with SQLModel ORM), and Authentication (Better Auth).

### V. Auditability
All agent actions and system behavior must be auditable. Every MCP tool invocation, database operation, and system decision must be logged and traceable for debugging and compliance purposes. Errors must be handled gracefully and consistently with user-friendly messages.

## Key Standards

### Technology Stack Requirements
- **Frontend**: OpenAI ChatKit for conversational UI
- **Backend**: Python FastAPI for API endpoints
- **AI Framework**: OpenAI Agents SDK for AI logic
- **MCP Server**: Official MCP SDK for tool implementation
- **Database**: Neon Serverless PostgreSQL with SQLModel ORM
- **Authentication**: Better Auth for user management

### Development Process
- All implementation must be generated from specifications
- No manual coding without prior specification
- Follow Red-Green-Refactor cycle for all changes
- Maintain comprehensive test coverage
- Natural language commands must map deterministically to tool calls

## Constraints

### Implementation Constraints
- No manual coding; all implementation generated from specs
- Official MCP SDK must be used for tool implementation
- FastAPI backend with OpenAI Agents SDK integration
- SQLModel with Neon Serverless PostgreSQL database
- ChatKit-based frontend UI
- Authentication via Better Auth

### Architectural Constraints
- Stateless server architecture mandatory
- Database-backed persistence for all state
- MCP tools must be stateless and idempotent
- Conversation context must be retrievable from database
- Error handling must be graceful and consistent
- Backend servers must not store conversational state in memory

## Success Criteria

### Functional Requirements
- AI chatbot can manage todos entirely through natural language
- All MCP tools (add_task, list_tasks, complete_task, delete_task, update_task) work correctly
- Natural language commands map to appropriate tool calls
- System handles errors gracefully with user-friendly messages
- AI agents may only modify data via MCP tools

### Technical Requirements
- Stateless behavior verified across server restarts
- Conversation context correctly persisted in database
- MCP tools invoked correctly for user intents
- System passes hackathon technical and architectural review
- All database models (Task, Conversation, Message) implemented correctly
- API endpoints follow specified contracts
- Conversation context correctly persisted in database across server restarts

## Governance

### Constitution Compliance
This constitution supersedes all other practices and guidelines. All system components, development processes, and architectural decisions must comply with these principles. All system behavior must be defined in written specifications, and AI behavior must follow deterministic patterns through explicit tool contracts.

### Amendment Process
- Amendments require documentation of changes
- Version bump according to semantic versioning rules
- Migration plan for breaking changes
- Approval from project architect

### Review Requirements
- All PRs and code reviews must verify compliance
- Complexity must be justified and documented
- Use constitution as primary guidance for development decisions
- Verify that all agent actions and system behavior remain auditable

**Version**: 1.1.0 | **Ratified**: 2026-01-15 | **Last Amended**: 2026-01-15
