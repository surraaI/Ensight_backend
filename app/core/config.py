from pydantic_settings import BaseSettings
from pydantic import EmailStr, PostgresDsn
from typing import List, Optional
import os

class Settings(BaseSettings):
    # Database Configuration
    DATABASE_URL: PostgresDsn = "postgresql://user:pass@localhost:5432/ensight"
    
    # JWT Configuration
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    JWT_REFRESH_SECRET_KEY: str = "your-refresh-secret-key"
    
    # Authentication
    TOKEN_HEADER: str = "Authorization"  # Added this
    TOKEN_PREFIX: str = "Bearer"         # Added this
    
    # Email Configuration
    EMAIL_FROM: EmailStr
    SMTP_HOST: str
    SMTP_PORT: int = 587
    SMTP_USER: str
    SMTP_PASSWORD: str
    EMAIL_TEMPLATES_DIR: str = "/app/email-templates"
    
    # Application Configuration
    PROJECT_NAME: str = "Ensight"
    DEBUG: bool = False
    API_V1_STR: str = "/api/v1"
    
    # Security
    BACKEND_CORS_ORIGINS: List[str] = ["*"]
    
    # First Superadmin
    FIRST_SUPERADMIN_EMAIL: EmailStr
    FIRST_SUPERADMIN_PASSWORD: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

settings = Settings()