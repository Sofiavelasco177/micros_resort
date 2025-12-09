from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Service URLs
    AUTH_SERVICE_URL: str = "http://localhost:8001"
    USER_SERVICE_URL: str = "http://localhost:8002"
    ROOM_SERVICE_URL: str = "http://localhost:8003"
    ROOM_RESERVATION_SERVICE_URL: str = "http://localhost:8004"
    RESTAURANT_SERVICE_URL: str = "http://localhost:8005"
    RESTAURANT_RESERVATION_SERVICE_URL: str = "http://localhost:8006"
    EXPERIENCE_SERVICE_URL: str = "http://localhost:8007"
    ANALYTICS_SERVICE_URL: str = "http://localhost:8008"
    
    # Gateway Config
    GATEWAY_PORT: int = 8000
    GATEWAY_NAME: str = "Hotel Management API Gateway"
    
    class Config:
        env_file = "../.env"
        extra = "ignore"


settings = Settings()

# Service mapping
SERVICES = {
    "auth": settings.AUTH_SERVICE_URL,
    "users": settings.USER_SERVICE_URL,
    "rooms": settings.ROOM_SERVICE_URL,
    "room_reservations": settings.ROOM_RESERVATION_SERVICE_URL,
    "reservations": settings.ROOM_RESERVATION_SERVICE_URL,  # Alias
    "restaurant": settings.RESTAURANT_SERVICE_URL,
    "restaurant_reservations": settings.RESTAURANT_RESERVATION_SERVICE_URL,
    "experiences": settings.EXPERIENCE_SERVICE_URL,
    "analytics": settings.ANALYTICS_SERVICE_URL,
}
