from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    """Base schema para usuario"""
    email: EmailStr
    first_name: str
    last_name: str
    phone: Optional[str] = None


class UserCreate(UserBase):
    """Schema para crear usuario"""
    password: str = Field(..., min_length=6)
    role: str = "user"


class UserUpdate(BaseModel):
    """Schema para actualizar usuario"""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None


class UserResponse(UserBase):
    """Schema para respuesta de usuario"""
    id: int
    role: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class UserProfileUpdate(BaseModel):
    """Schema para actualizar perfil propio"""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None


class VerifyCredentialsRequest(BaseModel):
    """Schema para verificar credenciales"""
    email: EmailStr
    password: str


class ResetPasswordRequest(BaseModel):
    """Schema para resetear contraseña"""
    email: EmailStr
    new_password: str = Field(..., min_length=6)


class MessageResponse(BaseModel):
    """Schema para mensajes generales"""
    message: str
