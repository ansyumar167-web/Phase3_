#!/usr/bin/env python3
"""Simple test to check database configuration."""

from src.config import settings
from src.database.session import create_db_and_tables
from sqlmodel import SQLModel
from src.database.session import engine

print("Database URL:", settings.database_url)
print("Database Echo:", settings.database_echo)

try:
    # Try to create tables synchronously
    create_db_and_tables()
    print("SUCCESS: Database tables created successfully!")
except Exception as e:
    print(f"ERROR: Database setup failed: {e}")
    import traceback
    traceback.print_exc()