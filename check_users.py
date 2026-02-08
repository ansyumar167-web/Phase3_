"""
Check what users exist in the database
"""
import sys
sys.path.insert(0, 'backend')

from backend.src.database.session import get_session_context
from backend.src.database.models import User as DBUser
from sqlmodel import select

def check_users():
    """Check all users in database"""
    print("=" * 60)
    print("Checking ALL Users in Database")
    print("=" * 60)

    try:
        with get_session_context() as session:
            statement = select(DBUser)
            all_users = session.exec(statement).all()

            print(f"\nTotal users in database: {len(all_users)}")
            print("-" * 60)

            if len(all_users) == 0:
                print("No users found in database!")
            else:
                for user in all_users:
                    print(f"\nUser ID: {user.id}")
                    print(f"  Username: {user.username}")
                    print(f"  Email: {user.email}")
                    print(f"  Active: {user.is_active}")
                    print("-" * 60)

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_users()
