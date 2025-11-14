import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_api():
    print("Testing OctoFit Tracker API...\n")
    
    try:
        # Test API root
        print("1. Testing API Root Endpoint...")
        response = requests.get(f"{BASE_URL}/api/")
        if response.status_code == 200:
            print("✓ API Root: SUCCESS")
            data = response.json()
            print(json.dumps(data, indent=2))
        else:
            print(f"✗ API Root: FAILED (Status: {response.status_code})")
        
        print("\n" + "="*50 + "\n")
        
        # Test user registration
        print("2. Testing User Registration...")
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass123",
            "password_confirm": "testpass123",
            "first_name": "Test",
            "last_name": "User"
        }
        response = requests.post(f"{BASE_URL}/api/users/register/", json=user_data)
        if response.status_code in [200, 201]:
            print("✓ User Registration: SUCCESS")
            print(json.dumps(response.json(), indent=2))
        elif response.status_code == 400:
            print("ℹ User may already exist")
            print(response.json())
        else:
            print(f"✗ User Registration: FAILED (Status: {response.status_code})")
        
        print("\n" + "="*50 + "\n")
        
        # Test login
        print("3. Testing Login...")
        login_data = {
            "username": "admin",
            "password": "admin123"
        }
        response = requests.post(f"{BASE_URL}/api/auth/login/", json=login_data)
        if response.status_code == 200:
            print("✓ Login: SUCCESS")
            token_data = response.json()
            print(json.dumps(token_data, indent=2))
            token = token_data.get('key')
            
            if token:
                # Test authenticated endpoint
                print("\n4. Testing Authenticated Endpoint (My Profile)...")
                headers = {"Authorization": f"Token {token}"}
                response = requests.get(f"{BASE_URL}/api/profiles/my_profile/", headers=headers)
                if response.status_code == 200:
                    print("✓ My Profile: SUCCESS")
                    print(json.dumps(response.json(), indent=2))
                else:
                    print(f"✗ My Profile: FAILED (Status: {response.status_code})")
        else:
            print(f"✗ Login: FAILED (Status: {response.status_code})")
            print(response.json())
        
        print("\n" + "="*50)
        print("API Testing Complete!")
        
    except requests.exceptions.ConnectionError:
        print("✗ ERROR: Could not connect to the server.")
        print("Make sure Django server is running on http://127.0.0.1:8000/")
    except Exception as e:
        print(f"✗ ERROR: {str(e)}")

if __name__ == "__main__":
    test_api()
