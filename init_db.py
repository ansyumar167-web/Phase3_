#!/usr/bin/env python3
"""
Database initialization script for the Todo AI Agent.
This script sets up the Neon PostgreSQL database with proper schema and indexes.
"""

import sys
import os
from pathlib import Path

# Add the backend directory to the path so imports work correctly
backend_path = str(Path(__file__).parent / "backend")
sys.path.insert(0, backend_path)

from src.database.neon_migration import run_full_setup
from src.config import settings


def main():
    """Main entry point for database initialization."""
    print("[INIT] Initializing Neon PostgreSQL database for Todo AI Agent...")

    # Print current configuration
    print(f"[INFO] Current environment: {settings.environment}")
    print(f"[INFO] Database URL configured: {'Yes' if settings.database_url and 'postgresql' in settings.database_url else 'No'}")

    if settings.environment == "development":
        print("[WARN] Running in development mode")

    # Run the full setup
    success = run_full_setup()

    if not success:
        print("[ERROR] Database initialization failed!")
        sys.exit(1)

    print("[SUCCESS] Database initialization completed successfully!")


if __name__ == "__main__":
    main()