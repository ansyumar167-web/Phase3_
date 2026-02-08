#!/usr/bin/env python3
"""
Test script to check users in the database
"""

import sys
from pathlib import Path

# Add the backend directory to the path so imports work correctly
backend_path = str(Path(__file__).parent / "backend")
sys.path.insert(0, backend_path)

from src.database.session import get_session
from src.database.models import User as DBUser
from sqlmodel import select

def check_users():
    """Check if there are any users in the database."""
    session_gen = get_session()
    session = next(session_gen)
    try:
        statement = select(DBUser)
        users = session.exec(statement).all()

        if users:
            print(f"Found {len(users)} users in the database:")
            for user in users:
                print(f"- ID: {user.id}, Email: {user.email}, Username: {user.username}")
        else:
            print("No users found in the database. You need to register first.")
    finally:
        session.close()

if __name__ == "__main__":
    check_users()