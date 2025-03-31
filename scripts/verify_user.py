import os
import sys
from pathlib import Path

# Add the project root directory to Python path
project_root = str(Path(__file__).parent.parent)
sys.path.append(project_root)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import User

# Database connection
DATABASE_URL = "postgresql://postgres:postgres@db:5432/camera_alerts"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def verify_user():
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == "test@example.com").first()
        if user:
            print(f"User found: {user.email}")
            return True
        else:
            print("User not found in database")
            return False
    except Exception as e:
        print(f"Error verifying user: {e}")
        return False
    finally:
        db.close()

if __name__ == "__main__":
    verify_user() 