from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str = "tu-clave-secreta-muy-segura-cambiala-en-produccion"
    ALGORITHM: str = "HS256"
    DATABASE_URL: str = "sqlite:///./database.db"
    SERVICE_NAME: str = "Room Service"
    SERVICE_PORT: int = 8003
    
    class Config:
        env_file = "../.env"
        extra = "ignore"


settings = Settings()
