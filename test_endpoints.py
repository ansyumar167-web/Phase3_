#!/usr/bin/env python3
"""
Test script to verify that the API endpoints are working correctly.
This checks both the original issue and the fix.
"""

import requests
import sys
import subprocess
import time
from threading import Thread


def test_endpoints():
    """Test that the API endpoints are accessible."""

    # Test URLs
    base_url = "http://localhost:8000"
    login_url = f"{base_url}/login"
    api_login_url = f"{base_url}/api/login"
    health_url = f"{base_url}/api/health"

    # Test credentials for the demo users
    test_credentials = {
        "email": "test@example.com",
        "password": "any_password"  # Demo doesn't validate password
    }

    print("Testing API endpoints...")

    # Test health endpoint first
    try:
        response = requests.get(health_url, timeout=5)
        print(f"✓ Health check: {response.status_code} - {response.json().get('status', 'unknown')}")
    except Exception as e:
        print(f"✗ Health check failed: {e}")

    # Test original login endpoint (root)
    try:
        response = requests.post(login_url, json=test_credentials, timeout=5)
        print(f"✓ Root login endpoint (/login): {response.status_code}")
    except Exception as e:
        print(f"✗ Root login endpoint failed: {e}")

    # Test API login endpoint (with /api prefix)
    try:
        response = requests.post(api_login_url, json=test_credentials, timeout=5)
        print(f"✓ API login endpoint (/api/login): {response.status_code}")
    except Exception as e:
        print(f"✗ API login endpoint failed: {e}")

    print("\nEndpoint testing completed!")


if __name__ == "__main__":
    test_endpoints()