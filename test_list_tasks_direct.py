"""
Test list_tasks functionality directly
"""
import sys
sys.path.insert(0, 'backend')

from backend.src.services.task_service import TaskService

def test_list_tasks():
    """Test listing tasks for user 12"""
    print("=" * 60)
    print("Testing List Tasks for User 12 (Imran)")
    print("=" * 60)

    try:
        # List all tasks
        print("\nListing ALL tasks for user 12...")
        tasks = TaskService.get_tasks(user_id="12", status="all")
        print(f"Found {len(tasks)} task(s)")

        for task in tasks:
            print(f"\n  Task ID: {task.id}")
            print(f"  Title: {task.title}")
            print(f"  Description: {task.description}")
            print(f"  Completed: {task.completed}")

        # List pending tasks
        print("\n" + "-" * 60)
        print("Listing PENDING tasks for user 12...")
        pending_tasks = TaskService.get_tasks(user_id="12", status="pending")
        print(f"Found {len(pending_tasks)} pending task(s)")

        # List completed tasks
        print("\n" + "-" * 60)
        print("Listing COMPLETED tasks for user 12...")
        completed_tasks = TaskService.get_tasks(user_id="12", status="completed")
        print(f"Found {len(completed_tasks)} completed task(s)")

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_list_tasks()
