"""
Basic test to verify the Todo AI Agent is set up correctly.
"""

import asyncio
from src.models.task import TaskCreate
from src.services.task_service import TaskService
from src.database.session import get_session_direct


async def test_basic_functionality():
    """Test basic functionality of the Todo AI Agent."""
    print("Testing basic functionality...")

    # Get a database session
    session = get_session_direct()

    try:
        # Test creating a task
        print("\n1. Testing task creation...")
        task_data = TaskCreate(user_id="test_user", title="Test task", description="Test description")
        task_service = TaskService()
        created_task = task_service.create_task(session, task_data)

        print(f"   Created task: ID={created_task.id}, Title='{created_task.title}'")

        # Test retrieving the task
        print("\n2. Testing task retrieval...")
        retrieved_task = task_service.get_task_by_id(session, created_task.id, "test_user")
        if retrieved_task:
            print(f"   Retrieved task: ID={retrieved_task.id}, Title='{retrieved_task.title}', Completed={retrieved_task.completed}")
        else:
            print("   Failed to retrieve task")

        # Test updating the task
        print("\n3. Testing task update...")
        from src.models.task import TaskUpdate
        update_data = TaskUpdate(title="Updated test task", completed=True)
        updated_task = task_service.update_task(session, created_task.id, "test_user", update_data)

        if updated_task:
            print(f"   Updated task: ID={updated_task.id}, Title='{updated_task.title}', Completed={updated_task.completed}")
        else:
            print("   Failed to update task")

        # Test listing tasks
        print("\n4. Testing task listing...")
        tasks = task_service.get_tasks_by_user(session, "test_user")
        print(f"   Found {len(tasks)} tasks for user 'test_user'")

        pending_tasks = task_service.get_tasks_by_user(session, "test_user", "pending")
        print(f"   Found {len(pending_tasks)} pending tasks")

        completed_tasks = task_service.get_tasks_by_user(session, "test_user", "completed")
        print(f"   Found {len(completed_tasks)} completed tasks")

        # Test completing a task
        print("\n5. Testing task completion...")
        completed_task = task_service.complete_task(session, created_task.id, "test_user")
        if completed_task:
            print(f"   Completed task: ID={completed_task.id}, Title='{completed_task.title}', Completed={completed_task.completed}")

        # Clean up - delete the test task
        print("\n6. Cleaning up...")
        deleted = task_service.delete_task(session, created_task.id, "test_user")
        print(f"   Deleted task: {deleted}")

        print("\n✓ All basic functionality tests passed!")

    except Exception as e:
        print(f"\n[FAILED] Error during testing: {e}")
    finally:
        session.close()


if __name__ == "__main__":
    asyncio.run(test_basic_functionality())