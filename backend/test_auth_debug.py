#!/usr/bin/env python3
"""
Debug script to test authentication flow
"""
import sys
import os

# Fix Windows console encoding issues
if sys.platform == 'win32':
    if sys.stdout.encoding != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')
    if sys.stderr.encoding != 'utf-8':
        sys.stderr.reconfigure(encoding='utf-8')
    os.environ['PYTHONIOENCODING'] = 'utf-8'

from sqlmodel import Session, select
from src.database.session import get_session_context
from src.database.models import User as DBUser
from src.auth.config import get_password_hash, verify_password

def test_database_connection():
    """Test if database is connected"""
    print("=" * 60)
    print("1. Testing Database Connection...")
    print("=" * 60)
    try:
        with get_session_context() as session:
            # Try a simple query
            result = session.exec(select(DBUser)).all()
            print(f"✅ Database connected successfully!")
            print(f"   Found {len(result)} users in database")
            return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def list_all_users():
    """List all users in database"""
    print("\n" + "=" * 60)
    print("2. Listing All Users...")
    print("=" * 60)
    try:
        with get_session_context() as session:
            users = session.exec(select(DBUser)).all()
            if not users:
                print("⚠️  No users found in database")
            else:
                for user in users:
                    print(f"\nUser ID: {user.id}")
                    print(f"  Email: {user.email}")
                    print(f"  Username: {user.username}")
                    print(f"  Has Password: {'Yes' if user.hashed_password else 'No'}")
                    print(f"  Password Hash (first 20 chars): {user.hashed_password[:20]}...")
    except Exception as e:
        print(f"❌ Error listing users: {e}")

def test_register_user():
    """Test registering a new user"""
    print("\n" + "=" * 60)
    print("3. Testing User Registration...")
    print("=" * 60)

    test_email = "debug@test.com"
    test_username = "debuguser"
    test_password = "testpass123"

    try:
        with get_session_context() as session:
            # Check if user already exists
            existing = session.exec(select(DBUser).where(DBUser.email == test_email)).first()
            if existing:
                print(f"⚠️  User {test_email} already exists, deleting...")
                session.delete(existing)
                session.commit()

            # Create new user
            hashed_password = get_password_hash(test_password)
            print(f"\n📝 Creating user:")
            print(f"   Email: {test_email}")
            print(f"   Username: {test_username}")
            print(f"   Password: {test_password}")
            print(f"   Hashed Password (first 20 chars): {hashed_password[:20]}...")

            new_user = DBUser(
                email=test_email,
                username=test_username,
                hashed_password=hashed_password
            )
            session.add(new_user)
            session.commit()
            session.refresh(new_user)

            print(f"\n✅ User registered successfully!")
            print(f"   User ID: {new_user.id}")
            return new_user
    except Exception as e:
        print(f"❌ Registration failed: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_login(email: str, password: str):
    """Test login with credentials"""
    print("\n" + "=" * 60)
    print("4. Testing Login...")
    print("=" * 60)
    print(f"   Email: {email}")
    print(f"   Password: {password}")

    try:
        with get_session_context() as session:
            # Get user by email
            user = session.exec(select(DBUser).where(DBUser.email == email)).first()

            if not user:
                print(f"❌ User not found with email: {email}")
                return False

            print(f"\n✅ User found in database:")
            print(f"   User ID: {user.id}")
            print(f"   Email: {user.email}")
            print(f"   Username: {user.username}")
            print(f"   Has Password: {'Yes' if user.hashed_password else 'No'}")

            # Verify password
            print(f"\n🔐 Verifying password...")
            is_valid = verify_password(password, user.hashed_password)

            if is_valid:
                print(f"✅ Password verification SUCCESS!")
                return True
            else:
                print(f"❌ Password verification FAILED!")
                print(f"   Provided password: {password}")
                print(f"   Stored hash (first 20 chars): {user.hashed_password[:20]}...")
                return False

    except Exception as e:
        print(f"❌ Login test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("\n🔍 AUTH DEBUG SCRIPT")
    print("=" * 60)

    # Test 1: Database connection
    if not test_database_connection():
        print("\n❌ Cannot proceed without database connection")
        sys.exit(1)

    # Test 2: List existing users
    list_all_users()

    # Test 3: Register a test user
    user = test_register_user()
    if not user:
        print("\n❌ Cannot proceed without successful registration")
        sys.exit(1)

    # Test 4: Test login with correct credentials
    test_login("debug@test.com", "testpass123")

    # Test 5: Test login with wrong password
    print("\n" + "=" * 60)
    print("5. Testing Login with WRONG Password...")
    print("=" * 60)
    test_login("debug@test.com", "wrongpassword")

    print("\n" + "=" * 60)
    print("✅ DEBUG COMPLETE!")
    print("=" * 60)

if __name__ == "__main__":
    main()
