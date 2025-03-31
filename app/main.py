from fastapi import FastAPI, Depends, HTTPException, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import json
import logging
import jwt
import os

from .database import get_db
from .models import Event, Alert
from .schemas import EventCreate, EventResponse, AlertResponse, Token
from .auth import get_current_user, authenticate_user, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM
from .tasks import process_event
from .websocket_manager import active_connections

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get port from environment variable
PORT = int(os.getenv("PORT", "7001"))

app = FastAPI(title="Camera Alert System")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

@app.websocket("/ws/alerts")
async def websocket_endpoint(websocket: WebSocket):
    try:
        # Get token from query parameters
        token = websocket.query_params.get("token")
        if not token:
            await websocket.close(code=4001, reason="No token provided")
            return

        # Verify token and get user
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email: str = payload.get("sub")
            if email is None:
                await websocket.close(code=4001, reason="Invalid token")
                return
        except jwt.JWTError as e:
            logger.error(f"JWT error: {e}")
            await websocket.close(code=4001, reason="Invalid token")
            return

        # Accept connection with CORS headers
        headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Authorization",
            "Access-Control-Allow-Credentials": "true",
        }
        
        await websocket.accept(headers=headers)
        active_connections.append(websocket)
        logger.info(f"WebSocket connection accepted for user {email}")
        
        try:
            while True:
                data = await websocket.receive_text()
                logger.info(f"Received message: {data}")
                # Handle incoming messages if needed
        except Exception as e:
            logger.error(f"WebSocket error: {e}")
        finally:
            active_connections.remove(websocket)
            logger.info(f"WebSocket connection closed for user {email}")
    except Exception as e:
        logger.error(f"WebSocket connection error: {e}")
        await websocket.close(code=4001, reason="Connection error")

@app.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/events/", response_model=EventResponse)
async def create_event(
    event: EventCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    try:
        logger.info(f"Creating event for user {current_user.id}")
        logger.info(f"Event data: {json.dumps(event.dict(), indent=2)}")
        
        # Create event in database
        db_event = Event(
            device_id=event.device_id,
            event_type=event.event_type,
            confidence=event.confidence,
            timestamp=datetime.utcnow(),
            raw_data=event.raw_data,
            user_id=current_user.id
        )
        db.add(db_event)
        db.commit()
        db.refresh(db_event)
        
        logger.info(f"Event created with ID: {db_event.id}")

        # Queue event for processing
        try:
            from .tasks import queue, process_event
            # Enqueue the event for processing
            job = queue.enqueue(process_event, db_event.id)
            logger.info(f"Event {db_event.id} queued for processing with job ID: {job.id}")
        except Exception as e:
            logger.error(f"Failed to queue event for processing: {e}")
            # Don't raise here, as the event was already created

        return db_event
    except Exception as e:
        logger.error(f"Error creating event: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create event: {str(e)}"
        )

@app.get("/alerts/", response_model=list[AlertResponse])
async def get_alerts(
    skip: int = 0,
    limit: int = 100,
    severity: str = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    query = db.query(Alert).filter(Alert.user_id == current_user.id)
    
    if severity:
        query = query.filter(Alert.severity == severity)
    
    alerts = query.order_by(Alert.created_at.desc()).offset(skip).limit(limit).all()
    return alerts

@app.get("/")
async def root():
    return {"message": "Welcome to Camera Alert System API"} 