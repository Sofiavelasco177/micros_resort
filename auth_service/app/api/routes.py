from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from typing import Optional
from ..database.connection import get_db
from ..schemas.schemas import (
    RegisterRequest,
    LoginRequest,
    TokenResponse,
    RefreshTokenRequest,
    VerifyTokenResponse,
    ResetPasswordRequest,
    MessageResponse
)
from ..services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: RegisterRequest,
    db: Session = Depends(get_db)
):
    """
    Registrar un nuevo usuario en el sistema
    
    - **email**: Email del usuario (único)
    - **password**: Contraseña (mínimo 6 caracteres)
    - **first_name**: Nombre
    - **last_name**: Apellido
    - **phone**: Teléfono (opcional)
    """
    service = AuthService(db)
    return await service.register_user(user_data)


@router.post("/login", response_model=TokenResponse)
async def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    Iniciar sesión en el sistema
    
    - **email**: Email del usuario
    - **password**: Contraseña
    
    Retorna tokens de acceso y refresco
    """
    service = AuthService(db)
    return await service.login_user(login_data)


@router.post("/refresh", response_model=TokenResponse)
def refresh_token(
    refresh_data: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    """
    Refrescar el token de acceso usando el refresh token
    
    - **refresh_token**: Token de refresco obtenido en login/register
    """
    service = AuthService(db)
    return service.refresh_access_token(refresh_data.refresh_token)


@router.post("/logout", response_model=MessageResponse)
def logout(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    """
    Cerrar sesión revocando el token actual
    
    Requiere el token en el header: Authorization: Bearer <token>
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token no proporcionado"
        )
    
    token = authorization.replace("Bearer ", "")
    service = AuthService(db)
    
    if service.logout_user(token):
        return MessageResponse(message="Sesión cerrada exitosamente")
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Token no encontrado"
    )


@router.get("/verify", response_model=VerifyTokenResponse)
def verify_token(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    """
    Verificar la validez de un token
    
    Requiere el token en el header: Authorization: Bearer <token>
    """
    if not authorization or not authorization.startswith("Bearer "):
        return VerifyTokenResponse(valid=False)
    
    token = authorization.replace("Bearer ", "")
    service = AuthService(db)
    return service.verify_token(token)


@router.post("/reset-password", response_model=MessageResponse)
async def reset_password(
    reset_data: ResetPasswordRequest,
    db: Session = Depends(get_db)
):
    """
    Restablecer contraseña de usuario
    
    - **email**: Email del usuario
    - **new_password**: Nueva contraseña (mínimo 6 caracteres)
    """
    service = AuthService(db)
    
    if await service.reset_password(reset_data.email, reset_data.new_password):
        return MessageResponse(message="Contraseña restablecida exitosamente")
    
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Error al restablecer contraseña"
    )
