"""
Simple script to check all tasks in the database
"""
import sys
sys.path.insert(0, 'backend')

from backend.src.database.session import get_session_context
from backend.src.database.models import Task as DBTask
from sqlmodel import select

def check_all_tasks():
    """Check all tasks in database"""
    print("=" * 60)
    print("Checking ALL Tasks in Database")
    print("=" * 60)

    try:
        with get_session_context() as session:
            statement = select(DBTask)
            all_tasks = session.exec(statement).all()

            print(f"\nTotal tasks in database: {len(all_tasks)}")
            print("-" * 60)

            if len(all_tasks) == 0:
                print("No tasks found in database!")
            else:
                for task in all_tasks:
                    print(f"\nTask ID: {task.id}")
                    print(f"  User ID: {task.user_id}")
                    print(f"  Title: {task.title}")
                    print(f"  Description: {task.description}")
                    print(f"  Completed: {task.completed}")
                    print(f"  Created: {task.created_at}")
                    print("-" * 60)

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_all_tasks()
