import requests
import json

# Test the registration endpoint
def test_registration():
    url = "http://localhost:8000/api/register"

    # Test data with a new email
    test_data = {
        "email": "newuser@example.com",
        "username": "newuser",
        "password": "securepassword123"
    }

    headers = {
        "Content-Type": "application/json"
    }

    try:
        print("Testing registration endpoint...")
        print(f"Sending request to: {url}")
        print(f"Data: {json.dumps(test_data, indent=2)}")

        response = requests.post(url, json=test_data, headers=headers)

        print(f"Response Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print(f"Response Body: {response.text}")

        if response.status_code == 200:
            print("\n[SUCCESS] Registration successful!")
            return True
        else:
            print(f"\n[FAILED] Registration failed with status code: {response.status_code}")
            return False

    except requests.exceptions.ConnectionError:
        print("[ERROR] Could not connect to the server. Is it running on http://localhost:8000?")
        return False
    except Exception as e:
        print(f"[ERROR] An error occurred: {str(e)}")
        return False

if __name__ == "__main__":
    test_registration()