from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # JWT Configuration
    SECRET_KEY: str = "tu-clave-secreta-muy-segura-cambiala-en-produccion"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Database
    DATABASE_URL: str = "sqlite:///./database.db"
    
    # Service Info
    SERVICE_NAME: str = "Auth Service"
    SERVICE_PORT: int = 8001
    
    # User Service URL (para comunicación entre servicios)
    USER_SERVICE_URL: str = "http://localhost:8002"
    
    class Config:
        env_file = "../.env"
        extra = "ignore"


settings = Settings()
