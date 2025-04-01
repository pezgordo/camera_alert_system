# Remote Camera Alert System

A FastAPI-based system for processing camera events and generating alerts. This system simulates a camera monitoring system where devices can send events that are processed by a background worker.

## Features

- FastAPI backend with JWT authentication
- PostgreSQL database for storing events and alerts
- Redis for background task queue
- RQ worker for processing events
- WebSocket support for real-time alerts
- Docker Compose setup for easy deployment
- Automated setup script for quick deployment

## Prerequisites

- Docker and Docker Compose
- Python 3.11+ (for local development)

## Getting Started

1. Clone the repository:

```bash
git clone <repository-url>
cd camera-alert-system
```

2. Make the setup script executable:

```bash
chmod +x setup.sh
```

3. Run the setup script:

```bash
./setup.sh
```

The system will be available at:

- API: http://localhost:7001
- Frontend: http://localhost:5173
- API Documentation: http://localhost:7001/docs

## Default Login Credentials

- Email: test@example.com
- Password: testpassword

## API Endpoints

- `POST /token`: Get authentication token
- `POST /events/`: Create a new camera event
- `GET /alerts/`: Get list of alerts
- `WS /ws/alerts`: WebSocket endpoint for real-time alerts

## Development

To run the application locally:

1. Create a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set up environment variables:

```bash
export DATABASE_URL="postgresql://postgres:postgres@localhost:5433/camera_alerts"
export REDIS_URL="redis://localhost:6379/0"
export JWT_SECRET="your-secret-key-here"
```

4. Run the application:

```bash
uvicorn app.main:app --reload --port 7001
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
├── scripts/
│   ├── setup.py
│   ├── simulate_events.py
│   └── test_system.py
├── frontend/
│   └── src/
├── docker-compose.yml
├── Dockerfile
├── setup.sh
└── requirements.txt
```

## Testing the System

1. Start the system using the setup script:

```bash
./setup.sh
```

2. Simulate camera events:

```bash
docker-compose exec web python scripts/simulate_events.py
```

3. Run system tests:

```bash
docker-compose exec web python scripts/test_system.py
```

## Security Notes

- In production, make sure to:
  - Use strong passwords
  - Set proper CORS origins
  - Use environment variables for sensitive data
  - Enable HTTPS
  - Implement rate limiting
  - Change the default JWT secret key
  - Use secure database credentials
