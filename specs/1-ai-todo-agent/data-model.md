# Data Model: AI-Powered Conversational Todo Agent

## Entity: Task
**Fields**:
- `id` (integer, primary key, auto-increment)
- `user_id` (string, required) - Identifier for the user who owns the task
- `title` (string, required, max 255 chars) - Brief description of the task
- `description` (string, optional, max 1000 chars) - Additional details about the task
- `completed` (boolean, default false) - Status indicating if the task is completed
- `created_at` (timestamp, required) - When the task was created
- `updated_at` (timestamp, required) - When the task was last updated

**Validation rules**:
- Title must not be empty
- Title must be less than 255 characters
- User_id must exist and be valid

**State transitions**:
- `pending` → `completed` (via complete_task MCP tool)
- `completed` → `pending` (via update_task MCP tool with completed=false)

## Entity: Conversation
**Fields**:
- `id` (integer, primary key, auto-increment)
- `user_id` (string, required) - Identifier for the user who owns the conversation
- `created_at` (timestamp, required) - When the conversation was started
- `updated_at` (timestamp, required) - When the conversation was last updated

**Validation rules**:
- User_id must exist and be valid
- Created_at must be before updated_at

## Entity: Message
**Fields**:
- `id` (integer, primary key, auto-increment)
- `user_id` (string, required) - Identifier for the user who sent the message
- `conversation_id` (integer, required, foreign key to Conversation) - Links to the conversation
- `role` (string, required) - Either "user" or "assistant"
- `content` (string, required, max 10000 chars) - The content of the message
- `created_at` (timestamp, required) - When the message was created

**Validation rules**:
- Role must be either "user" or "assistant"
- Content must not be empty
- Conversation_id must reference an existing conversation
- User_id must match the conversation owner

## Relationships
- **Conversation → Messages**: One-to-many relationship (one conversation contains many messages)
- **User → Tasks**: One-to-many relationship (one user has many tasks)
- **User → Conversations**: One-to-many relationship (one user has many conversations)
- **Conversation → Messages**: One-to-many relationship (one conversation has many messages)