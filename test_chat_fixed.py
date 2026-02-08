import requests
import json

# Test the chat endpoint with authentication
def test_chat():
    # First, register a new user to make sure we have a clean test
    register_url = "http://localhost:8000/api/register"

    register_data = {
        "email": "testchat@example.com",
        "username": "testchatuser",
        "password": "securepassword123"
    }

    headers = {
        "Content-Type": "application/json"
    }

    print("Step 1: Registering a new user for testing...")
    try:
        register_response = requests.post(register_url, json=register_data, headers=headers)
        print(f"Register Response Status: {register_response.status_code}")

        if register_response.status_code == 200:
            register_result = register_response.json()
            print(f"Registration successful! New user: {register_result}")
            user_id = str(register_result.get("id", ""))
        elif register_response.status_code == 400:
            # User might already exist, try to log in
            print("User might already exist, attempting login...")
        else:
            print(f"Registration failed: {register_response.text}")
            return False

    except Exception as e:
        print(f"Registration error: {str(e)}")
        return False

    # Now try to log in to get an authentication token
    login_url = "http://localhost:8000/api/login"

    login_data = {
        "email": "testchat@example.com",
        "password": "securepassword123"
    }

    print("\nStep 2: Logging in to get authentication token...")
    try:
        login_response = requests.post(login_url, json=login_data, headers=headers)
        print(f"Login Response Status: {login_response.status_code}")

        if login_response.status_code != 200:
            print("Login failed!")
            print(f"Login Response: {login_response.text}")
            return False

        login_result = login_response.json()
        access_token = login_result.get("access_token")

        # Get user ID from the login response
        user_obj = login_result.get("user", {})
        user_id = str(user_obj.get("id", ""))

        print(f"Login successful! User ID from login: {user_id}")

    except Exception as e:
        print(f"Login error: {str(e)}")
        return False

    # Now test the chat endpoint with the authentication token
    chat_url = f"http://localhost:8000/api/{user_id}/chat"

    chat_data = {
        "message": "Hello, can you help me create a task?",
        "conversation_id": None  # Will create a new conversation
    }

    # Add the authentication header
    auth_headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    print(f"\nStep 3: Testing chat endpoint for user {user_id}...")
    print(f"Sending request to: {chat_url}")
    print(f"Data: {json.dumps(chat_data, indent=2)}")

    try:
        response = requests.post(chat_url, json=chat_data, headers=auth_headers)

        print(f"Response Status Code: {response.status_code}")
        print(f"Response Body: {response.text}")

        if response.status_code in [200, 201]:
            print("\n[SUCCESS] Chat message sent successfully!")
            return True
        else:
            print(f"\n[FAILED] Chat request failed with status code: {response.status_code}")
            return False

    except requests.exceptions.ConnectionError:
        print("[ERROR] Could not connect to the server. Is it running on http://localhost:8000?")
        return False
    except Exception as e:
        print(f"[ERROR] An error occurred: {str(e)}")
        return False

if __name__ == "__main__":
    test_chat()