"""
Integration test for concurrent user requests.
"""
import asyncio
import pytest
from fastapi.testclient import TestClient
from src.api.chat_endpoint import app
from src.database.session import get_session_direct
from src.services.task_service import TaskService


def test_concurrent_user_requests_basic():
    """
    Test that multiple users can make requests simultaneously without interfering with each other.
    """
    # Test with multiple different users making requests
    users = [f"concurrent_user_{i}" for i in range(5)]
    tasks_results = []

    def make_request(user_id, task_num):
        """Simulate a single user request."""
        client = TestClient(app)
        response = client.post(f"/api/{user_id}/chat", json={
            "message": f"Add a task for user {user_id}: Task {task_num}",
            "conversation_id": None
        })

        return {
            "user_id": user_id,
            "task_num": task_num,
            "status_code": response.status_code,
            "response": response.json() if response.status_code == 200 else None
        }

    # Simulate concurrent requests using threads (since we're using TestClient which is sync)
    import concurrent.futures

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = []

        # Create requests for different users
        for i, user in enumerate(users):
            future = executor.submit(make_request, user, i)
            futures.append(future)

        # Collect results
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            tasks_results.append(result)

    # Verify all requests succeeded
    assert len(tasks_results) == 5
    for result in tasks_results:
        assert result["status_code"] == 200
        assert result["response"] is not None
        assert "conversation_id" in result["response"]
        assert "response" in result["response"]
        assert "tool_calls" in result["response"]
        assert "add_task" in result["response"]["tool_calls"]

    # Verify each user has their own task in the database
    for user in users:
        session = get_session_direct()
        try:
            task_service = TaskService()
            user_tasks = task_service.get_tasks_by_user(session, user)

            # Each user should have at least one task
            assert len(user_tasks) >= 1

            # Verify tasks belong to the correct user
            for task in user_tasks:
                assert task.user_id == user
        finally:
            session.close()

    print("✓ Concurrent user requests handled correctly")


def test_same_user_concurrent_requests():
    """
    Test that a single user can make multiple requests that don't interfere with each other.
    """
    user_id = "same_user_concurrent_test"
    tasks_results = []

    def make_request(task_num):
        """Simulate a request from the same user."""
        client = TestClient(app)
        response = client.post(f"/api/{user_id}/chat", json={
            "message": f"Add task {task_num} for same user",
            "conversation_id": None
        })

        return {
            "task_num": task_num,
            "status_code": response.status_code,
            "response": response.json() if response.status_code == 200 else None
        }

    import concurrent.futures

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = []

        # Create multiple requests from the same user
        for i in range(3):
            future = executor.submit(make_request, i)
            futures.append(future)

        # Collect results
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            tasks_results.append(result)

    # Verify all requests succeeded
    assert len(tasks_results) == 3
    for result in tasks_results:
        assert result["status_code"] == 200

    # Verify the user has all the tasks in the database
    session = get_session_direct()
    try:
        task_service = TaskService()
        user_tasks = task_service.get_tasks_by_user(session, user_id)

        # Should have 3 tasks
        assert len(user_tasks) == 3

        # All tasks should belong to the same user
        for task in user_tasks:
            assert task.user_id == user_id
    finally:
        session.close()

    print("✓ Same user concurrent requests handled correctly")


def test_database_concurrent_access():
    """
    Test that concurrent database access works correctly.
    """
    user_id = "db_concurrent_test"

    # First, add a few tasks to work with
    session = get_session_direct()
    try:
        task_service = TaskService()

        # Add initial tasks
        from src.models.task import TaskCreate
        for i in range(3):
            task = TaskCreate(user_id=user_id, title=f"Initial task {i}", description=f"Description {i}")
            task_service.create_task(session, task)
    finally:
        session.close()

    # Now test concurrent operations on the same user's data
    results = []

    def perform_operation(op_type, op_id):
        """Perform a specific operation."""
        client = TestClient(app)

        if op_type == "list":
            response = client.post(f"/api/{user_id}/chat", json={
                "message": "Show me all my tasks",
                "conversation_id": None
            })
        elif op_type == "add":
            response = client.post(f"/api/{user_id}/chat", json={
                "message": f"Add another task {op_id}",
                "conversation_id": None
            })
        elif op_type == "complete_first":
            # Try to complete the first task (this is tricky without knowing the ID)
            # We'll just try to list to see if concurrent access works
            response = client.post(f"/api/{user_id}/chat", json={
                "message": "Show me all my tasks",
                "conversation_id": None
            })

        return {
            "operation": op_type,
            "id": op_id,
            "status_code": response.status_code,
            "response": response.json() if response.status_code == 200 else None
        }

    import concurrent.futures

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = []

        # Mix of operations
        ops = [("list", 1), ("add", 2), ("list", 3)]
        for op_type, op_id in ops:
            future = executor.submit(perform_operation, op_type, op_id)
            futures.append(future)

        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            results.append(result)

    # Verify all operations succeeded
    assert len(results) == 3
    for result in results:
        assert result["status_code"] == 200
        assert result["response"] is not None

    print("✓ Concurrent database access works correctly")


if __name__ == "__main__":
    test_concurrent_user_requests_basic()
    test_same_user_concurrent_requests()
    test_database_concurrent_access()
    print("All concurrency tests passed!")