import os
import sys
import time
from pathlib import Path

# Add the project root directory to Python path
project_root = str(Path(__file__).parent.parent)
sys.path.append(project_root)

from sqlalchemy import create_engine
from app.database import Base
from app.models import User, Event, Alert
from app.auth import get_password_hash

def wait_for_db(max_retries=5):
    """Wait for database to be ready"""
    DATABASE_URL = "postgresql://postgres:postgres@db:5432/camera_alerts"
    retries = 0
    while retries < max_retries:
        try:
            engine = create_engine(DATABASE_URL)
            engine.connect()
            print("Database is ready!")
            return True
        except Exception as e:
            print(f"Waiting for database... ({retries + 1}/{max_retries})")
            retries += 1
            time.sleep(2)
    return False

def init_db():
    """Initialize database tables"""
    try:
        DATABASE_URL = "postgresql://postgres:postgres@db:5432/camera_alerts"
        engine = create_engine(DATABASE_URL)
        Base.metadata.create_all(bind=engine)
        print("Database tables created successfully")
        return True
    except Exception as e:
        print(f"Error creating database tables: {e}")
        return False

def create_test_user():
    """Create test user if it doesn't exist"""
    try:
        DATABASE_URL = "postgresql://postgres:postgres@db:5432/camera_alerts"
        engine = create_engine(DATABASE_URL)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        # Check if user already exists
        existing_user = db.query(User).filter(User.email == "test@example.com").first()
        if existing_user:
            print("Test user already exists")
            return True

        # Create new test user
        test_user = User(
            email="test@example.com",
            hashed_password=get_password_hash("testpassword")
        )
        db.add(test_user)
        db.commit()
        print("Test user created successfully")
        return True
    except Exception as e:
        print(f"Error creating test user: {e}")
        return False
    finally:
        db.close()

def main():
    print("Starting system setup...")
    
    # Wait for database to be ready
    if not wait_for_db():
        print("Failed to connect to database. Please check if the database container is running.")
        return False
    
    # Initialize database
    if not init_db():
        print("Failed to initialize database.")
        return False
    
    # Create test user
    if not create_test_user():
        print("Failed to create test user.")
        return False
    
    print("\nSetup completed successfully!")
    print("\nYou can now:")
    print("1. Access the API at http://localhost:7001")
    print("2. Access the frontend at http://localhost:5173")
    print("3. Login with:")
    print("   Email: test@example.com")
    print("   Password: testpassword")
    return True

if __name__ == "__main__":
    main() 