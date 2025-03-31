import requests
import json
import time
from datetime import datetime

API_URL = "http://localhost:7001"

def test_health():
    """Test if the API is running"""
    try:
        response = requests.get(f"{API_URL}/")
        print("Health check:", response.status_code == 200)
        return response.status_code == 200
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

def test_login():
    """Test user login"""
    login_data = {
        "username": "test@example.com",
        "password": "testpassword"
    }
    try:
        response = requests.post(f"{API_URL}/token", data=login_data)
        print("Login test:", response.status_code == 200)
        if response.status_code == 200:
            token = response.json()["access_token"]
            print("Token received:", token[:20] + "...")
            return token
        else:
            print(f"Login failed with status code: {response.status_code}")
            print(f"Response: {response.text}")
        return None
    except Exception as e:
        print(f"Login test failed: {e}")
        return None

def test_create_event(token):
    """Test event creation"""
    event = {
        "device_id": "test_camera_001",
        "event_type": "motion_detected",
        "confidence": 0.95,
        "raw_data": {
            "timestamp": datetime.utcnow().isoformat(),
            "location": "test_zone_1",
            "image_url": "https://example.com/test.jpg",
            "metadata": {
                "resolution": "1920x1080",
                "fps": 30
            }
        }
    }
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    try:
        print("Sending event:", json.dumps(event, indent=2))
        response = requests.post(f"{API_URL}/events/", json=event, headers=headers)
        print(f"Event creation response: {response.status_code}")
        if response.status_code != 200:
            print(f"Error response: {response.text}")
            try:
                error_json = response.json()
                print(f"Error details: {json.dumps(error_json, indent=2)}")
            except:
                pass
        return response.status_code == 200
    except Exception as e:
        print(f"Event creation test failed: {e}")
        return False

def test_get_alerts(token):
    """Test alert retrieval"""
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(f"{API_URL}/alerts/", headers=headers)
        print("Alert retrieval test:", response.status_code == 200)
        if response.status_code == 200:
            alerts = response.json()
            print(f"Retrieved {len(alerts)} alerts")
        return response.status_code == 200
    except Exception as e:
        print(f"Alert retrieval test failed: {e}")
        return False

def main():
    print("Starting system tests...")
    
    # Test API health
    if not test_health():
        print("System is not healthy. Please check if all services are running.")
        return
    
    # Test login
    token = test_login()
    if not token:
        print("Login failed. Please check credentials and try again.")
        return
    
    # Test event creation
    if not test_create_event(token):
        print("Event creation failed. Please check the API and database.")
        print("\nTroubleshooting steps:")
        print("1. Check if the worker service is running:")
        print("   docker-compose ps")
        print("2. Check worker logs:")
        print("   docker-compose logs worker")
        print("3. Check web service logs:")
        print("   docker-compose logs web")
        return
    
    # Wait for event processing
    print("Waiting for event processing...")
    time.sleep(5)
    
    # Test alert retrieval
    if not test_get_alerts(token):
        print("Alert retrieval failed. Please check the API and database.")
        return
    
    print("\nAll tests completed successfully!")

if __name__ == "__main__":
    main() 