from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # JWT Configuration (para validar tokens)
    SECRET_KEY: str = "tu-clave-secreta-muy-segura-cambiala-en-produccion"
    ALGORITHM: str = "HS256"
    
    # Database
    DATABASE_URL: str = "sqlite:///./database.db"
    
    # Service Info
    SERVICE_NAME: str = "User Service"
    SERVICE_PORT: int = 8002
    
    class Config:
        env_file = "../.env"
        extra = "ignore"


settings = Settings()
