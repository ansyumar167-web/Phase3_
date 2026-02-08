# Data Model: MCP Server and Task Management Tools

## Entity: Task
**Fields**:
- `id` (integer, primary key, auto-increment)
- `user_id` (string, required) - Identifier for the user who owns the task
- `title` (string, required, max 255 chars) - Brief description of the task
- `description` (string, optional, max 1000 chars) - Additional details about the task
- `completed` (boolean, default false) - Status indicating if the task is completed
- `created_at` (datetime, required) - When the task was created
- `updated_at` (datetime, required) - When the task was last updated

**Validation rules**:
- Title must not be empty
- Title must be less than 255 characters
- User_id must exist and be valid
- User_id cannot be changed after creation

**State transitions**:
- `pending` → `completed` (via complete_task tool)
- `completed` → `pending` (via update_task tool with completed=false)

## Entity: ToolInvocation (for audit trail)
**Fields**:
- `id` (integer, primary key, auto-increment)
- `tool_name` (string, required) - Name of the tool invoked
- `user_id` (string, required) - User who initiated the tool call
- `parameters` (JSON, required) - Input parameters passed to the tool
- `result` (JSON, optional) - Output returned by the tool
- `error` (string, optional) - Error message if the tool failed
- `created_at` (datetime, required) - When the tool was invoked

**Validation rules**:
- Tool_name must be one of the valid task management tools
- Parameters must match the expected schema for the tool
- Either result or error must be present, but not both

## Relationships
- **User → Tasks**: One-to-many relationship (one user has many tasks)
- **ToolInvocation**: Tracks all tool usage for audit and debugging purposes

## Indexes
- Index on `user_id` for efficient user-specific queries
- Index on `(user_id, completed)` for filtered queries
- Index on `created_at` for chronological ordering