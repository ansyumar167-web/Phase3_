#!/usr/bin/env python3
"""
Test script to verify user registration and login functionality.
"""

import asyncio
import requests
import json
from datetime import datetime
from src.config import settings
from src.database.init import run_init_db
from src.database.session import get_session_context
from src.database.models import User
from sqlmodel import select


def test_database_connection():
    """Test database connection and initialize tables."""
    print("Testing database connection and initializing tables...")
    try:
        # Use the synchronous method instead of async
        from src.database.session import create_db_and_tables
        create_db_and_tables()
        print("SUCCESS: Database tables created successfully!")
        return True
    except Exception as e:
        print(f"ERROR: Database initialization failed: {e}")
        return False


def test_user_creation():
    """Test user creation in the database."""
    print("\nTesting user creation...")
    try:
        with get_session_context() as session:
            # Check if test user already exists
            existing_user = session.exec(select(User).where(User.email == "test@example.com")).first()
            if existing_user:
                print("  Test user already exists, skipping creation.")
                return True

            # Create a new user
            from src.auth.config import get_password_hash
            hashed_password = get_password_hash("testpassword123")

            user = User(
                email="test@example.com",
                username="testuser",
                hashed_password=hashed_password
            )

            session.add(user)
            session.commit()
            session.refresh(user)

            print(f"SUCCESS: User created successfully with ID: {user.id}")
            return True
    except Exception as e:
        print(f"ERROR: User creation failed: {e}")
        return False


def test_user_login():
    """Test user login functionality via API."""
    print("\nTesting user login via API...")

    # Start the API server in a separate process (or use existing one)
    # For this test, we'll simulate a direct function call instead of HTTP request
    # since we're testing the internal functionality

    try:
        from src.api.auth_endpoint import login_handler
        from src.api.auth_endpoint import UserLogin
        from src.database.session import get_session_context

        with get_session_context() as session:
            user_credentials = UserLogin(email="test@example.com", password="testpassword123")
            response = login_handler(user_credentials, session)

        print(f"SUCCESS: Login successful! Access token generated for user: {response.user.email}")
        print(f"  Token type: {response.token_type}")
        print(f"  User ID: {response.user.id}")
        return True
    except Exception as e:
        print(f"ERROR: Login failed: {e}")
        return False


def test_user_registration():
    """Test user registration functionality via API."""
    print("\nTesting user registration via API...")

    try:
        from src.api.auth_endpoint import register_user
        from src.api.auth_endpoint import UserRegister
        from src.database.session import get_session_context

        # Create registration data
        user_data = UserRegister(
            email="newuser@example.com",
            username="newuser",
            password="securepassword123"
        )

        with get_session_context() as session:
            # Check if user already exists
            existing_user = session.exec(select(User).where(User.email == "newuser@example.com")).first()
            if existing_user:
                print("  New test user already exists, skipping registration.")
                return True

            # Register the new user
            user = register_user(user_data, session)

        print(f"SUCCESS: Registration successful! New user created with ID: {user.id}")
        print(f"  Email: {user.email}")
        print(f"  Username: {user.username}")
        return True
    except Exception as e:
        print(f"ERROR: Registration failed: {e}")
        return False


def main():
    """Run all tests."""
    print("="*60)
    print("Testing User Registration and Login Functionality")
    print("="*60)

    tests_passed = 0
    total_tests = 4

    # Test 1: Database connection
    if test_database_connection():
        tests_passed += 1

    # Test 2: User creation
    if test_user_creation():
        tests_passed += 1

    # Test 3: User registration
    if test_user_registration():
        tests_passed += 1

    # Test 4: User login
    if test_user_login():
        tests_passed += 1

    print("\n" + "="*60)
    print(f"Tests completed: {tests_passed}/{total_tests} passed")

    if tests_passed == total_tests:
        print("SUCCESS: All tests passed! User registration and login functionality is working correctly.")
        return True
    else:
        print("ERROR: Some tests failed. Please check the implementation.")
        return False


if __name__ == "__main__":
    main()