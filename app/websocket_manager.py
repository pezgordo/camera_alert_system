from fastapi import WebSocket
from typing import List

# Store active WebSocket connections
active_connections: List[WebSocket] = []

async def broadcast_alert(alert_data: str):
    """Broadcast alert to all connected WebSocket clients"""
    for connection in active_connections:
        try:
            await connection.send_text(alert_data)
        except Exception as e:
            print(f"Error sending alert to WebSocket client: {e}") 