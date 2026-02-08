# MCP Tool Contracts: Task Management Tools

## Tool: add_task

### Purpose
Create a new task for a user.

### Parameters
- `user_id` (string, required): User identifier
- `title` (string, required): Task title (max 255 chars)
- `description` (string, optional): Task description (max 1000 chars)

### Returns
```json
{
  "task_id": "integer: ID of the created task",
  "status": "string: 'created'",
  "title": "string: Title of the created task"
}
```

### Validation
- `user_id` must be a valid string
- `title` must be present and not empty
- `title` must be less than 255 characters
- `description` if provided must be less than 1000 characters

### Error Cases
- Invalid parameters: Returns error object
- Database failure: Returns error object

### Examples
**Input**:
```json
{
  "user_id": "user123",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread"
}
```

**Output**:
```json
{
  "task_id": 1,
  "status": "created",
  "title": "Buy groceries"
}
```

---

## Tool: list_tasks

### Purpose
Retrieve tasks for a user with optional filtering.

### Parameters
- `user_id` (string, required): User identifier
- `status` (string, optional): Filter by status ("all", "pending", "completed")

### Returns
Array of task objects:
```json
[
  {
    "id": "integer: Task ID",
    "user_id": "string: User ID",
    "title": "string: Task title",
    "completed": "boolean: Completion status",
    "created_at": "string: ISO 8601 timestamp",
    "updated_at": "string: ISO 8601 timestamp"
  }
  ...
]
```

### Validation
- `user_id` must be a valid string
- `status` if provided must be one of "all", "pending", "completed"

### Error Cases
- Invalid user_id: Returns error object
- Database failure: Returns error object

### Examples
**Input**:
```json
{
  "user_id": "user123",
  "status": "pending"
}
```

**Output**:
```json
[
  {
    "id": 1,
    "user_id": "user123",
    "title": "Buy groceries",
    "completed": false,
    "created_at": "2023-01-01T10:00:00Z",
    "updated_at": "2023-01-01T10:00:00Z"
  }
]
```

---

## Tool: complete_task

### Purpose
Mark a task as complete.

### Parameters
- `user_id` (string, required): User identifier
- `task_id` (integer, required): ID of the task to complete

### Returns
```json
{
  "task_id": "integer: ID of the completed task",
  "status": "string: 'completed'",
  "title": "string: Title of the completed task"
}
```

### Validation
- `user_id` must be a valid string
- `task_id` must be a positive integer
- Task must exist and belong to the user

### Error Cases
- Task not found: Returns error object
- Permission denied: Returns error object
- Invalid parameters: Returns error object

### Examples
**Input**:
```json
{
  "user_id": "user123",
  "task_id": 1
}
```

**Output**:
```json
{
  "task_id": 1,
  "status": "completed",
  "title": "Buy groceries"
}
```

---

## Tool: delete_task

### Purpose
Remove a task from the user's list.

### Parameters
- `user_id` (string, required): User identifier
- `task_id` (integer, required): ID of the task to delete

### Returns
```json
{
  "task_id": "integer: ID of the deleted task",
  "status": "string: 'deleted'",
  "title": "string: Title of the deleted task"
}
```

### Validation
- `user_id` must be a valid string
- `task_id` must be a positive integer
- Task must exist and belong to the user

### Error Cases
- Task not found: Returns error object
- Permission denied: Returns error object
- Invalid parameters: Returns error object

### Examples
**Input**:
```json
{
  "user_id": "user123",
  "task_id": 1
}
```

**Output**:
```json
{
  "task_id": 1,
  "status": "deleted",
  "title": "Buy groceries"
}
```

---

## Tool: update_task

### Purpose
Modify task title or description.

### Parameters
- `user_id` (string, required): User identifier
- `task_id` (integer, required): ID of the task to update
- `title` (string, optional): New task title
- `description` (string, optional): New task description

### Returns
```json
{
  "task_id": "integer: ID of the updated task",
  "status": "string: 'updated'",
  "title": "string: Updated task title"
}
```

### Validation
- `user_id` must be a valid string
- `task_id` must be a positive integer
- If `title` is provided, it must be less than 255 characters
- If `description` is provided, it must be less than 1000 characters
- Task must exist and belong to the user

### Error Cases
- Task not found: Returns error object
- Permission denied: Returns error object
- Invalid parameters: Returns error object

### Examples
**Input**:
```json
{
  "user_id": "user123",
  "task_id": 1,
  "title": "Buy groceries and fruits"
}
```

**Output**:
```json
{
  "task_id": 1,
  "status": "updated",
  "title": "Buy groceries and fruits"
}
```

---

## Common Error Format

All tools return errors in the following format:

```json
{
  "error": "string: Descriptive error message",
  "code": "string: Machine-readable error code"
}
```

## Idempotency Notes

- `complete_task`: Calling on an already completed task returns success without changing state
- `delete_task`: Calling on a non-existent task returns an error
- `update_task`: Calling with same values returns success without changing state