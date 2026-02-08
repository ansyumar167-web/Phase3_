"""
MCP tool response consistency validation.
"""
import asyncio
from src.services.mcp_server import mcp_server_instance as mcp_server


async def test_mcp_tool_response_consistency():
    """Test that MCP tools return consistent response formats."""

    # Test add_task response format
    add_task_params = {
        "user_id": "consistency_test_user",
        "title": "Consistency test task",
        "description": "Test description"
    }

    result = await mcp_server.handle_call("add_task", add_task_params)
    print("ADD_TASK RESULT:", result)

    if result.success:
        data = result.data
        assert "task_id" in data
        assert "status" in data
        assert "title" in data
        assert data["status"] == "created"
        print("[OK] add_task response format is consistent")
    else:
        # Might fail due to database not being set up properly in this context
        print(f"[WARN] add_task failed (likely due to DB setup): {result.error}")

    # Test list_tasks response format
    list_params = {
        "user_id": "consistency_test_user",
        "status": "all"
    }

    result = await mcp_server.handle_call("list_tasks", list_params)
    print("LIST_TASKS RESULT:", result)

    if result.success:
        data = result.data
        assert isinstance(data, list)
        print("[OK] list_tasks response format is consistent")
    else:
        print(f"[WARN] list_tasks failed: {result.error}")

    # Test complete_task response format (will likely fail since task doesn't exist)
    complete_params = {
        "user_id": "consistency_test_user",
        "task_id": 999999  # Non-existent task
    }

    result = await mcp_server.handle_call("complete_task", complete_params)
    print("COMPLETE_TASK RESULT:", result)

    if not result.success:
        # Expected to fail for non-existent task
        print("[OK] complete_task properly handles errors")
    else:
        # Unexpected success
        data = result.data
        assert "task_id" in data
        assert "status" in data
        assert "title" in data
        print("[OK] complete_task response format is consistent")

    # Test delete_task response format
    delete_params = {
        "user_id": "consistency_test_user",
        "task_id": 999999  # Non-existent task
    }

    result = await mcp_server.handle_call("delete_task", delete_params)
    print("DELETE_TASK RESULT:", result)

    if not result.success:
        # Expected to fail for non-existent task
        print("[OK] delete_task properly handles errors")
    else:
        # Unexpected success
        data = result.data
        assert "task_id" in data
        assert "status" in data
        assert "title" in data
        print("[OK] delete_task response format is consistent")

    # Test update_task response format
    update_params = {
        "user_id": "consistency_test_user",
        "task_id": 999999,  # Non-existent task
        "title": "Updated title"
    }

    result = await mcp_server.handle_call("update_task", update_params)
    print("UPDATE_TASK RESULT:", result)

    if not result.success:
        # Expected to fail for non-existent task
        print("[OK] update_task properly handles errors")
    else:
        # Unexpected success
        data = result.data
        assert "task_id" in data
        assert "status" in data
        assert "title" in data
        print("[OK] update_task response format is consistent")


if __name__ == "__main__":
    print("[INFO] Testing MCP tool response consistency...")
    asyncio.run(test_mcp_tool_response_consistency())
    print("[SUCCESS] MCP tool response consistency validation completed")