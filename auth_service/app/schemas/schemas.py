from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional


class RegisterRequest(BaseModel):
    """Schema para registro de usuario"""
    email: EmailStr
    password: str = Field(..., min_length=6)
    first_name: str
    last_name: str
    phone: Optional[str] = None


class LoginRequest(BaseModel):
    """Schema para inicio de sesión"""
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Schema para respuesta de token"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class RefreshTokenRequest(BaseModel):
    """Schema para refrescar token"""
    refresh_token: str


class VerifyTokenResponse(BaseModel):
    """Schema para verificación de token"""
    valid: bool
    user_id: Optional[int] = None
    email: Optional[str] = None
    role: Optional[str] = None


class ResetPasswordRequest(BaseModel):
    """Schema para restablecer contraseña"""
    email: EmailStr
    new_password: str = Field(..., min_length=6)


class MessageResponse(BaseModel):
    """Schema para mensajes generales"""
    message: str
