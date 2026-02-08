"""
Test script to verify task creation is working properly
"""
import sys
sys.path.insert(0, 'backend')

from backend.src.services.task_service import TaskService
from backend.src.models.task import TaskCreate
from backend.src.database.session import get_session_context
from backend.src.database.models import Task as DBTask
from sqlmodel import select

def test_task_creation():
    """Test if tasks can be created and retrieved"""
    print("=" * 50)
    print("Testing Task Creation")
    print("=" * 50)

    # Test 1: Create a task
    print("\n1. Creating a test task...")
    try:
        task_data = TaskCreate(
            user_id="test_user_123",
            title="Test Task - Buy Groceries",
            description="This is a test task"
        )

        created_task = TaskService.create_task(task_data)
        print(f"✅ Task created successfully!")
        print(f"   Task ID: {created_task.id}")
        print(f"   Title: {created_task.title}")
        print(f"   User ID: {created_task.user_id}")

    except Exception as e:
        print(f"❌ Error creating task: {e}")
        import traceback
        traceback.print_exc()
        return

    # Test 2: Retrieve the task
    print("\n2. Retrieving tasks for user...")
    try:
        tasks = TaskService.get_tasks(user_id="test_user_123", status="all")
        print(f"✅ Found {len(tasks)} task(s)")
        for task in tasks:
            print(f"   - Task #{task.id}: {task.title}")
    except Exception as e:
        print(f"❌ Error retrieving tasks: {e}")
        import traceback
        traceback.print_exc()
        return

    # Test 3: Direct database query
    print("\n3. Direct database query...")
    try:
        with get_session_context() as session:
            statement = select(DBTask).where(DBTask.user_id == "test_user_123")
            db_tasks = session.exec(statement).all()
            print(f"✅ Found {len(db_tasks)} task(s) in database")
            for task in db_tasks:
                print(f"   - Task #{task.id}: {task.title} (completed: {task.completed})")
    except Exception as e:
        print(f"❌ Error querying database: {e}")
        import traceback
        traceback.print_exc()
        return

    # Test 4: Check all tasks in database
    print("\n4. Checking ALL tasks in database...")
    try:
        with get_session_context() as session:
            statement = select(DBTask)
            all_tasks = session.exec(statement).all()
            print(f"✅ Total tasks in database: {len(all_tasks)}")
            for task in all_tasks:
                print(f"   - Task #{task.id}: {task.title} (user: {task.user_id})")
    except Exception as e:
        print(f"❌ Error querying all tasks: {e}")
        import traceback
        traceback.print_exc()

    print("\n" + "=" * 50)
    print("Test Complete")
    print("=" * 50)

if __name__ == "__main__":
    test_task_creation()
