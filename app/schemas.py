from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
        from_attributes = True

class EventBase(BaseModel):
    device_id: str
    event_type: str
    confidence: float
    raw_data: Dict[str, Any]

class EventCreate(EventBase):
    pass

class EventResponse(EventBase):
    id: int
    timestamp: datetime
    user_id: int

    class Config:
        from_attributes = True

class AlertBase(BaseModel):
    severity: str
    description: str

class AlertCreate(AlertBase):
    event_id: int

class AlertResponse(AlertBase):
    id: int
    created_at: datetime
    event_id: int
    user_id: int

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None 