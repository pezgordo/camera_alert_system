import os
import sys
from pathlib import Path

# Add the project root directory to Python path
project_root = str(Path(__file__).parent.parent)
sys.path.append(project_root)

from sqlalchemy import create_engine
from app.database import Base
from app.models import User, Event, Alert

# Database connection
DATABASE_URL = "postgresql://postgres:postgres@db:5432/camera_alerts"
engine = create_engine(DATABASE_URL)

def init_db():
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("Database tables created successfully")
    except Exception as e:
        print(f"Error creating database tables: {e}")
        sys.exit(1)

if __name__ == "__main__":
    init_db() 