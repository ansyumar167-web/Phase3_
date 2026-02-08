#!/usr/bin/env python3
"""
Quickstart validation script for Todo AI Agent.
This script validates that the quickstart instructions work correctly.
"""
import subprocess
import sys
import os
import time
from pathlib import Path


def validate_setup():
    """Validate that the project can be set up correctly."""
    print("[INFO] Validating project setup...")

    # Check if required files exist
    required_files = [
        "pyproject.toml",
        "src/models/task.py",
        "src/services/ai_agent.py",
        "src/api/chat_endpoint.py",
        "src/config.py"
    ]

    for file in required_files:
        if not Path(file).exists():
            print(f"[ERROR] Missing required file: {file}")
            return False

    print("[OK] All required files exist")
    return True


def validate_dependencies():
    """Validate that dependencies can be installed."""
    print("\n[INFO] Validating dependencies...")

    try:
        # Check if we can import the main modules
        import src.models.task
        import src.services.ai_agent
        import src.api.chat_endpoint
        import src.config
        print("[OK] Dependencies can be imported")
        return True
    except ImportError as e:
        print(f"[ERROR] Import error: {e}")
        return False


def validate_database_migration():
    """Validate that database migration works."""
    print("\n[INFO] Validating database migration...")

    try:
        from src.database.migrate import create_db_and_tables
        create_db_and_tables()
        print("[OK] Database migration successful")
        return True
    except Exception as e:
        print(f"[ERROR] Database migration failed: {e}")
        return False


def validate_basic_functionality():
    """Validate basic functionality works."""
    print("\n[INFO] Validating basic functionality...")

    try:
        # Run our test script
        result = subprocess.run([sys.executable, "test_basic.py"],
                              capture_output=True, text=True, cwd=".")

        if result.returncode == 0:
            print("[OK] Basic functionality test passed")
            return True
        else:
            print(f"[ERROR] Basic functionality test failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"[ERROR] Error running basic functionality test: {e}")
        return False


def validate_api_endpoint():
    """Validate that API endpoint can be imported and run."""
    print("\n[INFO] Validating API endpoint...")

    try:
        # Just check if the app can be imported without errors
        from src.api.chat_endpoint import app
        assert app is not None
        print("[OK] API endpoint can be imported")
        return True
    except Exception as e:
        print(f"[ERROR] API endpoint import failed: {e}")
        return False


def main():
    """Run all validations."""
    print("[INFO] Starting Todo AI Agent Quickstart Validation...\n")

    all_passed = True

    # Run all validation steps
    checks = [
        ("Project Setup", validate_setup),
        ("Dependencies", validate_dependencies),
        ("Database Migration", validate_database_migration),
        ("Basic Functionality", validate_basic_functionality),
        ("API Endpoint", validate_api_endpoint)
    ]

    for name, check_func in checks:
        if not check_func():
            all_passed = False
            print(f"[ERROR] {name} validation failed")
        else:
            print(f"[OK] {name} validation passed")

    print("\n" + "="*50)
    if all_passed:
        print("[SUCCESS] All validations passed! The Todo AI Agent is ready for use.")
        print("\nYou can start the service with:")
        print("  cd backend")
        print("  python main.py")
        print("\nOr using uvicorn:")
        print("  cd backend")
        print("  uvicorn src.api.chat_endpoint:app --reload")
        return 0
    else:
        print("[FAILURE] Some validations failed. Please check the errors above.")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)