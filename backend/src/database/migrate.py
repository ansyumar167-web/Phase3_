"""
Database migration script for the Todo AI Agent.
This now uses the enhanced Neon PostgreSQL migration system.
"""

from .neon_migration import run_full_setup, create_db_and_tables


def migrate():
    """Run the database migration using Neon-optimized setup."""
    run_full_setup()


if __name__ == "__main__":
    migrate()