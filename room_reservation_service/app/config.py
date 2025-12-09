import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SERVICE_NAME: str = "Room Reservation Service"
    SERVICE_PORT: int = 8004
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    DATABASE_URL: str = "sqlite:///./room_reservation.db"
    
    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
