import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore", case_sensitive=False)
    
    SERVICE_NAME: str = "Room Reservation Service"
    SERVICE_PORT: int = 8004
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    DATABASE_URL: str = "mysql+pymysql://root:@localhost:3306/micros_resort"
    AUTH_SERVICE_URL: str = "http://auth-service:8001"
    ROOM_SERVICE_URL: str = "http://room-service:8003"
    USER_SERVICE_URL: str = "http://user-service:8002"


settings = Settings()
