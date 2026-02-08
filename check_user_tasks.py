"""
Check tasks for actual logged-in users
"""
import sys
sys.path.insert(0, 'backend')

from backend.src.database.session import get_session_context
from backend.src.database.models import Task as DBTask, User as DBUser
from sqlmodel import select

def check_user_tasks():
    """Check tasks for each user"""
    print("=" * 60)
    print("Checking Tasks for Each User")
    print("=" * 60)

    try:
        with get_session_context() as session:
            # Get all users
            users = session.exec(select(DBUser)).all()

            print(f"\nFound {len(users)} users")

            for user in users:
                user_id_str = str(user.id)
                print(f"\n{'='*60}")
                print(f"User: {user.username} (ID: {user.id})")
                print(f"Email: {user.email}")
                print(f"Looking for tasks with user_id='{user_id_str}'")
                print("-" * 60)

                # Get tasks for this user
                statement = select(DBTask).where(DBTask.user_id == user_id_str)
                tasks = session.exec(statement).all()

                if len(tasks) == 0:
                    print("  No tasks found for this user")
                else:
                    print(f"  Found {len(tasks)} task(s):")
                    for task in tasks:
                        status = "[DONE]" if task.completed else "[TODO]"
                        print(f"    {status} Task #{task.id}: {task.title}")

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_user_tasks()
