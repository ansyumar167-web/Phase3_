# Quickstart Guide: AI-Powered Conversational Todo Agent

## Setup

1. **Environment Requirements**:
   - Python 3.11+
   - Poetry or pip for dependency management
   - Access to OpenAI API
   - Neon PostgreSQL database instance

2. **Installation**:
   ```bash
   # Clone the repository
   git clone [repo-url]
   cd [repo-name]

   # Install dependencies
   poetry install  # or pip install -r requirements.txt

   # Set up environment variables
   cp .env.example .env
   # Edit .env with your API keys and database connection
   ```

3. **Database Setup**:
   ```bash
   # Run database migrations
   python -m src.database.migrate
   ```

## Running the Service

1. **Start the MCP Server**:
   ```bash
   python -m src.services.mcp_server
   ```

2. **Start the API Service**:
   ```bash
   uvicorn src.api.chat_endpoint:app --reload
   ```

## Testing the Agent

1. **Send a test request**:
   ```bash
   curl -X POST http://localhost:8000/api/ziakhan/chat \
     -H "Content-Type: application/json" \
     -d '{"message": "Add a task to buy groceries", "conversation_id": null}'
   ```

2. **Expected response**:
   ```json
   {
     "conversation_id": 1,
     "response": "I've added the task 'buy groceries' to your list.",
     "tool_calls": ["add_task"]
   }
   ```

## Example Interactions

- "Add a task to buy groceries" → Creates a new task
- "Show me all my tasks" → Lists all tasks
- "What's pending?" → Lists pending tasks
- "Mark task 3 as complete" → Marks task as completed
- "Delete the meeting task" → Prompts for clarification or deletes by ID
- "Change task 1 to 'Call mom tonight'" → Updates task title

## Troubleshooting

- **Database connection errors**: Verify your Neon PostgreSQL connection string in `.env`
- **OpenAI API errors**: Check your API key in `.env`
- **MCP server not responding**: Ensure the MCP server is running alongside the API