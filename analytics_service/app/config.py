import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore", case_sensitive=False)
    
    SERVICE_NAME: str = "Analytics Service"
    SERVICE_PORT: int = 8008
    DATABASE_URL: str = "sqlite:///./data/analytics.db"
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    AUTH_SERVICE_URL: str = "http://auth-service:8001"
    ROOM_SERVICE_URL: str = "http://room-service:8003"
    USER_SERVICE_URL: str = "http://user-service:8002"
    RESTAURANT_SERVICE_URL: str = "http://restaurant-service:8005"
    EXPERIENCE_SERVICE_URL: str = "http://experience-service:8007"


settings = Settings()
