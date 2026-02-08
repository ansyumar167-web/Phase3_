# Quickstart Guide: MCP Server and Task Management Tools

## Setup

1. **Environment Requirements**:
   - Python 3.11+
   - Poetry or pip for dependency management
   - Access to Neon PostgreSQL database instance
   - Official MCP SDK

2. **Installation**:
   ```bash
   # Clone the repository
   git clone [repo-url]
   cd [repo-name]/backend

   # Install dependencies
   poetry install  # or pip install -r requirements.txt

   # Set up environment variables
   cp .env.example .env
   # Edit .env with your database connection and other settings
   ```

3. **Database Setup**:
   ```bash
   # Run database migrations
   python -m src.database.migrate
   ```

## Running the MCP Server

1. **Start the MCP Server**:
   ```bash
   python -m src.services.mcp_server
   ```

2. **Verify the server is running**:
   The server will register all five task management tools:
   - `add_task`
   - `list_tasks`
   - `complete_task`
   - `delete_task`
   - `update_task`

## Using the Tools

Each tool follows a standard pattern for input and output:

### add_task
**Input**:
```json
{
  "user_id": "string (required): User identifier",
  "title": "string (required): Task title",
  "description": "string (optional): Task description"
}
```

**Output**:
```json
{
  "task_id": "integer: ID of the created task",
  "status": "string: 'created'",
  "title": "string: Title of the created task"
}
```

### list_tasks
**Input**:
```json
{
  "user_id": "string (required): User identifier",
  "status": "string (optional): Filter by status ('all', 'pending', 'completed')"
}
```

**Output**:
```json
[
  {
    "id": "integer: Task ID",
    "user_id": "string: User ID",
    "title": "string: Task title",
    "completed": "boolean: Completion status",
    "created_at": "string: Creation timestamp",
    "updated_at": "string: Last update timestamp"
  }
  ...
]
```

### complete_task
**Input**:
```json
{
  "user_id": "string (required): User identifier",
  "task_id": "integer (required): ID of the task to complete"
}
```

**Output**:
```json
{
  "task_id": "integer: ID of the completed task",
  "status": "string: 'completed'",
  "title": "string: Title of the completed task"
}
```

### delete_task
**Input**:
```json
{
  "user_id": "string (required): User identifier",
  "task_id": "integer (required): ID of the task to delete"
}
```

**Output**:
```json
{
  "task_id": "integer: ID of the deleted task",
  "status": "string: 'deleted'",
  "title": "string: Title of the deleted task"
}
```

### update_task
**Input**:
```json
{
  "user_id": "string (required): User identifier",
  "task_id": "integer (required): ID of the task to update",
  "title": "string (optional): New title",
  "description": "string (optional): New description"
}
```

**Output**:
```json
{
  "task_id": "integer: ID of the updated task",
  "status": "string: 'updated'",
  "title": "string: Updated title"
}
```

## Error Handling

All tools return consistent error responses:

```json
{
  "error": "string: Descriptive error message",
  "code": "string: Error code for programmatic handling"
}
```

## Testing the Server

1. **Run unit tests**:
   ```bash
   pytest tests/unit/
   ```

2. **Run integration tests**:
   ```bash
   pytest tests/integration/
   ```

3. **Verify stateless operation**:
   The server should handle concurrent requests without retaining any state between requests.