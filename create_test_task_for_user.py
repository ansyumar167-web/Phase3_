"""
Create a test task for an actual user to verify the flow
"""
import sys
sys.path.insert(0, 'backend')

from backend.src.services.task_service import TaskService
from backend.src.models.task import TaskCreate

def create_test_task_for_user():
    """Create a test task for user ID 12 (Imran)"""
    print("=" * 60)
    print("Creating Test Task for User ID 12 (Imran)")
    print("=" * 60)

    try:
        # Create task for user 12
        task_data = TaskCreate(
            user_id="12",  # Imran's user ID
            title="Buy groceries",
            description="Milk, eggs, bread"
        )

        created_task = TaskService.create_task(task_data)
        print(f"\nTask created successfully!")
        print(f"  Task ID: {created_task.id}")
        print(f"  User ID: {created_task.user_id}")
        print(f"  Title: {created_task.title}")
        print(f"  Description: {created_task.description}")

        # Verify it was saved
        print("\nVerifying task was saved...")
        tasks = TaskService.get_tasks(user_id="12", status="all")
        print(f"User 12 now has {len(tasks)} task(s)")
        for task in tasks:
            print(f"  - Task #{task.id}: {task.title}")

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    create_test_task_for_user()
