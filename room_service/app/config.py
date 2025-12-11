from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore", case_sensitive=False)
    
    SECRET_KEY: str = "tu-clave-secreta-muy-segura-cambiala-en-produccion"
    ALGORITHM: str = "HS256"
    DATABASE_URL: str = "sqlite:///./data/rooms.db"
    SERVICE_NAME: str = "Room Service"
    SERVICE_PORT: int = 8003
    AUTH_SERVICE_URL: str = "http://auth-service:8001"


settings = Settings()
