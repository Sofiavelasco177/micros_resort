from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime
from ..database.connection import Base


class AuthToken(Base):
    """Modelo para tokens de autenticación"""
    __tablename__ = "auth_tokens"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    token = Column(String(500), unique=True, nullable=False, index=True)
    refresh_token = Column(String(500), unique=True, index=True)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    revoked = Column(Boolean, default=False)
    
    def __repr__(self):
        return f"<AuthToken(user_id={self.user_id}, revoked={self.revoked})>"
