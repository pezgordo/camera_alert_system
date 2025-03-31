from rq import Queue
from sqlalchemy.orm import Session
from datetime import datetime
import random
import json
import asyncio
from redis import Redis

from .database import SessionLocal
from .models import Event, Alert
from .websocket_manager import broadcast_alert

# Initialize RQ queue with Redis connection
redis_url = "redis://redis:6379/0"
redis_conn = Redis.from_url(redis_url)
queue = Queue("camera_tasks", connection=redis_conn)

def process_event(event_id: int):
    """
    Process an event and create an alert based on the event data.
    This is a simulated AI processing function.
    """
    db = SessionLocal()
    try:
        # Get the event
        event = db.query(Event).filter(Event.id == event_id).first()
        if not event:
            return

        # Simulate AI processing
        # In a real application, this would involve actual image/video processing
        is_critical = random.random() < 0.3  # 30% chance of being critical
        severity = "critical" if is_critical else "normal"
        
        # Create alert
        alert = Alert(
            event_id=event.id,
            severity=severity,
            description=f"Processed {event.event_type} event from device {event.device_id}",
            user_id=event.user_id
        )
        
        db.add(alert)
        db.commit()
        
        # Prepare alert data for WebSocket broadcast
        alert_data = {
            "id": alert.id,
            "event_id": alert.event_id,
            "severity": alert.severity,
            "description": alert.description,
            "created_at": alert.created_at.isoformat(),
            "user_id": alert.user_id
        }
        
        # Broadcast alert to WebSocket clients
        asyncio.run(broadcast_alert(json.dumps(alert_data)))

    finally:
        db.close() 