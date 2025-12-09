import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SERVICE_NAME: str = "Analytics Service"
    SERVICE_PORT: int = 8008
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    
    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
