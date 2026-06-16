from typing import Any, Dict, Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Incident Management System API"
    API_V1_STR: str = "/api/v1"
    
    SECRET_KEY: str = "super-secret-jwt-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    DATABASE_URL: str = "postgresql+asyncpg://postgres:password@localhost:5432/ims"
    
    GCP_PROJECT_ID: str = "incident-management-project"
    GCP_BUCKET_NAME: str = "incident-management-storage"
    
    ADMIN_EMAIL: str = "admin@company.com"
    ADMIN_PASSWORD: str = "admin123"

    SMTP_SERVER: Optional[str] = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USERNAME: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: Optional[str] = None

    class Config:
        env_file = ".env"

settings = Settings()
