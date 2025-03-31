import requests
import json

API_URL = "http://localhost:7001"

def test_login():
    """Test login and get token"""
    login_data = {
        "username": "test@example.com",
        "password": "testpassword"
    }
    response = requests.post(f"{API_URL}/token", data=login_data)
    print(f"Login status: {response.status_code}")
    if response.status_code == 200:
        token = response.json()["access_token"]
        print(f"Token: {token[:20]}...")
        return token
    else:
        print(f"Error: {response.text}")
        return None

def test_get_alerts(token):
    """Test getting alerts using the token"""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_URL}/alerts/", headers=headers)
    print(f"Get alerts status: {response.status_code}")
    if response.status_code == 200:
        alerts = response.json()
        print(f"Found {len(alerts)} alerts")
        if alerts:
            print("Sample alert:", json.dumps(alerts[0], indent=2))
    else:
        print(f"Error: {response.text}")

if __name__ == "__main__":
    print("Testing API...")
    token = test_login()
    if token:
        test_get_alerts(token)
    else:
        print("Login failed, cannot test alerts endpoint") 