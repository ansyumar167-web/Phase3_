#!/usr/bin/env python3
"""
Script to create a test user in the database for the Todo AI Agent application.
This addresses the 403 Forbidden error caused by missing user records.
"""

import requests
import json

def create_test_user():
    """Create a test user to resolve authentication issues."""
    # Backend server URL
    base_url = "http://localhost:8000"

    # Test user data
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "testpassword123"
    }

    print("Creating test user...")
    print(f"Registering user: {user_data['email']}")

    try:
        # Register the user
        response = requests.post(
            f"{base_url}/api/register",
            json=user_data,
            headers={"Content-Type": "application/json"}
        )

        if response.status_code == 200:
            user_info = response.json()
            print(f"[SUCCESS] User created successfully!")
            print(f"  User ID: {user_info['id']}")
            print(f"  Email: {user_info['email']}")
            print(f"  Username: {user_info['username']}")

            # Now try to login to get a token
            print("\n[INFO] Logging in to get authentication token...")
            login_data = {
                "email": user_data["email"],
                "password": user_data["password"]
            }

            login_response = requests.post(
                f"{base_url}/api/login",
                json=login_data,
                headers={"Content-Type": "application/json"}
            )

            if login_response.status_code == 200:
                login_result = login_response.json()
                token = login_result["access_token"]
                print(f"[SUCCESS] Login successful!")
                print(f"  Token: {token[:20]}..." if len(token) > 20 else f"  Token: {token}")

                # Test the chat endpoint with the token
                print("\n[INFO] Testing chat endpoint with authentication...")
                chat_data = {
                    "message": "Hello, this is a test message!",
                    "conversation_id": None
                }

                chat_response = requests.post(
                    f"{base_url}/api/chat",
                    json=chat_data,
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {token}"
                    }
                )

                if chat_response.status_code == 200:
                    chat_result = chat_response.json()
                    print(f"[SUCCESS] Chat endpoint working!")
                    print(f"  Conversation ID: {chat_result['conversation_id']}")
                    print(f"  Response: {chat_result['response'][:50]}...")
                else:
                    print(f"[ERROR] Chat endpoint failed with status: {chat_response.status_code}")
                    print(f"  Response: {chat_response.text}")

            else:
                print(f"[ERROR] Login failed with status: {login_response.status_code}")
                print(f"  Response: {login_response.text}")

        elif response.status_code == 400 and "already registered" in response.text.lower():
            print("[WARNING] User already exists, no need to create.")

            # Try to login instead
            login_data = {
                "email": user_data["email"],
                "password": user_data["password"]
            }

            login_response = requests.post(
                f"{base_url}/api/login",
                json=login_data,
                headers={"Content-Type": "application/json"}
            )

            if login_response.status_code == 200:
                login_result = login_response.json()
                token = login_result["access_token"]
                print(f"[SUCCESS] Successfully logged in existing user!")
                print(f"  Token: {token[:20]}..." if len(token) > 20 else f"  Token: {token}")

                # Test the chat endpoint with the token
                print("\n[INFO] Testing chat endpoint with authentication...")
                chat_data = {
                    "message": "Hello, this is a test message!",
                    "conversation_id": None
                }

                chat_response = requests.post(
                    f"{base_url}/api/chat",
                    json=chat_data,
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {token}"
                    }
                )

                if chat_response.status_code == 200:
                    chat_result = chat_response.json()
                    print(f"[SUCCESS] Chat endpoint working!")
                    print(f"  Conversation ID: {chat_result['conversation_id']}")
                    print(f"  Response: {chat_result['response'][:50]}...")
                else:
                    print(f"[ERROR] Chat endpoint failed with status: {chat_response.status_code}")
                    print(f"  Response: {chat_response.text}")
            else:
                print(f"[ERROR] Login failed with status: {login_response.status_code}")
                print(f"  Response: {login_response.text}")
        else:
            print(f"[ERROR] User creation failed with status: {response.status_code}")
            print(f"  Response: {response.text}")

    except requests.exceptions.ConnectionError:
        print("[ERROR] Could not connect to the backend server.")
        print("  Please make sure the backend server is running on http://localhost:8000")
    except Exception as e:
        print(f"[ERROR] Error occurred: {str(e)}")

if __name__ == "__main__":
    create_test_user()