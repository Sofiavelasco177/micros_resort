import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore", case_sensitive=False)
    
    SERVICE_NAME: str = "Restaurant Reservation Service"
    SERVICE_PORT: int = 8006
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    DATABASE_URL: str = "sqlite:///./data/restaurant_reservations.db"
    AUTH_SERVICE_URL: str = "http://auth-service:8001"
    RESTAURANT_SERVICE_URL: str = "http://restaurant-service:8005"
    USER_SERVICE_URL: str = "http://user-service:8002"


settings = Settings()
