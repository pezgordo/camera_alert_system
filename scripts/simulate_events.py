import requests
import time
import random
import json
from datetime import datetime

API_URL = "http://localhost:7001"

def get_token():
    login_data = {
        "username": "test@example.com",
        "password": "testpassword"
    }
    response = requests.post(f"{API_URL}/token", data=login_data)
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        raise Exception("Failed to get token")

def create_event(token):
    event_types = ["motion_detected", "person_detected", "object_detected", "face_detected"]
    device_ids = ["camera_001", "camera_002", "camera_003"]
    
    event = {
        "device_id": random.choice(device_ids),
        "event_type": random.choice(event_types),
        "confidence": round(random.uniform(0.5, 1.0), 2),
        "raw_data": {
            "timestamp": datetime.utcnow().isoformat(),
            "location": f"zone_{random.randint(1, 5)}",
            "image_url": f"https://example.com/images/{random.randint(1000, 9999)}.jpg",
            "metadata": {
                "resolution": "1920x1080",
                "fps": 30,
                "compression": "h264"
            }
        }
    }
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(f"{API_URL}/events/", json=event, headers=headers)
        if response.status_code == 200:
            print(f"Created event: {json.dumps(event, indent=2)}")
        else:
            print(f"Error creating event: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"Error: {e}")

def main():
    print("Starting event simulation...")
    try:
        token = get_token()
        print("Successfully obtained token")
        while True:
            create_event(token)
            time.sleep(random.uniform(2, 5))  # Wait between 2-5 seconds
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main() 