---
name: todo-app-chatbot-skill
description: Build a conversational AI skill that interprets natural language todo commands and interacts with a stateless backend using MCP tools and OpenAI Agents SDK.
---

# Todo App Chatbot Skill

## Instructions

1. **Conversational UI**
   - All interactions occur via chat messages.
   - Handle commands for: add, list, update, complete, delete tasks.
   - Confirm each action politely to the user.
   - Ask for clarification if the user input is ambiguous or missing required info.

2. **Agent Behavior**
   - Use OpenAI Agents SDK to parse natural language commands.
   - Determine the intent (add, list, update, complete, delete).
   - Call the appropriate MCP tool for each action.
   - Never store state in memory — always fetch and update tasks in Neon PostgreSQL.

3. **MCP Tool Integration**
   - `add_task` → Add a new task.
   - `list_tasks` → List all tasks for the user.
   - `complete_task` → Mark a task as completed.
   - `delete_task` → Remove a task.
   - `update_task` → Update task details.
   - Tools are stateless and persist state to database.

4. **Best Practices**
   - Keep responses short, clear, and friendly.
   - Provide success confirmation after every action.
   - Handle errors gracefully: e.g., 'Sorry, I couldn't complete your request.'
   - Support Markdown formatting for lists and emphasis.
   - Ensure accessibility for all messages in the UI.

## Example Structure
```text
User: "Add a task to call Mom at 5 PM"
Assistant: "I'm going to use the Task tool to launch the todo-app-chatbot-skill to handle this command."
Assistant: "✅ Task added: Call Mom at 5 PM"

User: "Show me my tasks"
Assistant: "I'm going to use the Task tool to launch the todo-app-chatbot-skill to handle this command."
Assistant: "Here are your tasks: 
1. Call Mom at 5 PM
2. Finish the report"

User: "Mark task 1 as done"
Assistant: "I'm going to use the Task tool to launch the todo-app-chatbot-skill to handle this command."
Assistant: "✅ Task 1 completed"
