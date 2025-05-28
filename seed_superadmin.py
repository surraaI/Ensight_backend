import os
import sys
from dotenv import load_dotenv
from passlib.context import CryptContext

# Add app directory to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'app')))

from database import SessionLocal
from models.user import User, Role  # Import the Role enum
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select

load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_superadmin():
    """Create initial superadmin if none exists"""
    db = SessionLocal()
    
    try:
        # Check if superadmin already exists - using UPPERCASE enum
        existing_superadmin = db.scalar(
            select(User).where(User.role == Role.SUPERADMIN)  # UPPERCASE
        )
        
        if existing_superadmin:
            print("⏩ Superadmin already exists. Skipping creation.")
            return

        # Get credentials from environment
        email = os.getenv("FIRST_SUPERADMIN_EMAIL")
        password = os.getenv("FIRST_SUPERADMIN_PASSWORD")
        
        if not email or not password:
            raise ValueError("❌ Missing FIRST_SUPERADMIN_EMAIL or FIRST_SUPERADMIN_PASSWORD in .env")

        # Create superadmin - using UPPERCASE enum
        superadmin = User(
            email=email,
            hashed_password=pwd_context.hash(password),
            role=Role.SUPERADMIN,  # UPPERCASE enum value
            is_active=True
        )

        db.add(superadmin)
        db.commit()
        print(f"✅ Superadmin created: {email}")
        
    except IntegrityError as e:
        db.rollback()
        print(f"❌ Integrity error: {str(e)}")
    except Exception as e:
        db.rollback()
        print(f"❌ Unexpected error: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    create_superadmin()