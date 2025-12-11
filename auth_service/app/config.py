from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore", case_sensitive=False)
    
    # JWT Configuration
    SECRET_KEY: str = "tu-clave-secreta-muy-segura-cambiala-en-produccion"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Database
    DATABASE_URL: str = "mysql+pymysql://root:@localhost:3306/micros_resort"
    
    # Service Info
    SERVICE_NAME: str = "Auth Service"
    SERVICE_PORT: int = 8001
    
    # User Service URL (para comunicación entre servicios)
    USER_SERVICE_URL: str = "http://user-service:8002"


settings = Settings()
