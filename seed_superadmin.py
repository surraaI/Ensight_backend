# seed_superadmin.py
import os
import sys
from passlib.context import CryptContext

from dotenv import load_dotenv
load_dotenv()

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'app')))

from database import SessionLocal, engine
from models.user import User
from sqlalchemy.exc import IntegrityError

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_superadmin(email: str, password: str):
    db = SessionLocal()
    hashed_password = pwd_context.hash(password)

    superadmin = User(
        email=email,
        hashed_password=hashed_password,
        role='superadmin',
        is_active=True
    )

    try:
        db.add(superadmin)
        db.commit()
        print(f"✅ Superadmin created: {email}")
    except IntegrityError:
        db.rollback()
        print("⚠️  Superadmin already exists or email is taken.")
    finally:
        db.close()

if __name__ == "__main__":
    # Replace with real values or prompt for input
    email = "superadmin@gmail.com"
    password = "12345678"
    create_superadmin(email, password)
