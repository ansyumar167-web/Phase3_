"""
Basic test to verify the AI agent and MCP integration works properly.
"""
import asyncio
import pytest
from src.services.ai_agent import AIAgent
from src.models.task import TaskCreate
from src.services.task_service import TaskService


@pytest.mark.asyncio
async def test_ai_agent_creation():
    """Test that AI agent can be created without errors."""
    try:
        agent = AIAgent()
        assert agent is not None
        assert len(agent.tools) == 5  # We defined 5 tools
        print("✓ AI Agent created successfully")
        return True
    except Exception as e:
        print(f"✗ Failed to create AI Agent: {e}")
        return False


@pytest.mark.asyncio
async def test_ai_agent_process_simple_message():
    """Test that AI agent can process a simple message."""
    try:
        agent = AIAgent()
        response = await agent.process_simple_message("test_user", "Hello")

        assert response is not None
        assert hasattr(response, 'content')
        assert hasattr(response, 'tool_calls')
        print("✓ AI Agent processed simple message successfully")
        return True
    except Exception as e:
        print(f"✗ Failed to process simple message: {e}")
        return False


async def run_tests():
    """Run all tests."""
    print("Running AI Agent tests...")

    results = []
    results.append(await test_ai_agent_creation())
    results.append(await test_ai_agent_process_simple_message())

    passed = sum(results)
    total = len(results)

    print(f"\nTests completed: {passed}/{total} passed")
    return passed == total


if __name__ == "__main__":
    success = asyncio.run(run_tests())
    exit(0 if success else 1)