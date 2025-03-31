# Remote Camera Alert System

A FastAPI-based system for processing camera events and generating alerts. This system simulates a camera monitoring system where devices can send events that are processed by a background worker.

## Features

- FastAPI backend with JWT authentication
- PostgreSQL database for storing events and alerts
- Redis for background task queue
- RQ worker for processing events
- WebSocket support for real-time alerts
- Docker Compose setup for easy deployment

## Prerequisites

- Docker and Docker Compose
- Python 3.11+ (for local development)

## Getting Started

1. Clone the repository:

```bash
git clone <repository-url>
cd camera-alert-system
```

2. Start the services using Docker Compose:

```bash
docker-compose up --build
```

The system will be available at:

- API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## API Endpoints

- `POST /events/`: Create a new camera event
- `GET /alerts/`: Get list of alerts
- `WS /ws/alerts`: WebSocket endpoint for real-time alerts

## Development

To run the application locally:

1. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set up environment variables:

```bash
export DATABASE_URL="postgresql://postgres:postgres@localhost:5432/camera_alerts"
export REDIS_URL="redis://localhost:6379/0"
export JWT_SECRET="your-secret-key-here"
```

4. Run the application:

```bash
uvicorn app.main:app --reload
```

## Project Structure

```
.
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── database.py
│   ├── auth.py
│   └── tasks.py
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

## Security Notes

- In production, make sure to:
  - Use strong passwords
  - Set proper CORS origins
  - Use environment variables for sensitive data
  - Enable HTTPS
  - Implement rate limiting
