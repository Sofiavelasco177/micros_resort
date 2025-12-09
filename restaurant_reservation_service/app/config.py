import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SERVICE_NAME: str = "Restaurant Reservation Service"
    SERVICE_PORT: int = 8006
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    DATABASE_URL: str = "sqlite:///./restaurant_reservation.db"
    
    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
