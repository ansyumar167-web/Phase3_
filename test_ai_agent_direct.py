"""
Test the actual chat endpoint with task creation
"""
import sys
sys.path.insert(0, 'backend')

import asyncio
from backend.src.services.ai_agent import AIAgent

async def test_ai_agent():
    """Test AI agent task creation"""
    print("=" * 60)
    print("Testing AI Agent Task Creation")
    print("=" * 60)

    try:
        # Create AI agent
        agent = AIAgent()

        # Test 1: Add a task
        print("\n1. Testing: 'Add a task to buy milk'")
        print("-" * 60)

        response = await agent.process_simple_message(
            user_id="12",  # Imran's user ID
            message="Add a task to buy milk"
        )

        print(f"AI Response: {response.content}")
        print(f"Tool Calls: {response.tool_calls}")

        # Test 2: List tasks
        print("\n2. Testing: 'Show me my tasks'")
        print("-" * 60)

        response = await agent.process_simple_message(
            user_id="12",
            message="Show me my tasks"
        )

        print(f"AI Response: {response.content}")
        print(f"Tool Calls: {response.tool_calls}")

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_ai_agent())
