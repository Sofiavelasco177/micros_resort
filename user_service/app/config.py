from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # JWT Configuration (para validar tokens)
    SECRET_KEY: str = "tu-clave-secreta-muy-segura-cambiala-en-produccion"
    ALGORITHM: str = "HS256"
    
    # Database
    DATABASE_URL: str = "mysql+pymysql://root:@localhost:3306/micros_resort"
    
    # Service Info
    SERVICE_NAME: str = "User Service"
    SERVICE_PORT: int = 8002
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore", case_sensitive=False)


settings = Settings()
