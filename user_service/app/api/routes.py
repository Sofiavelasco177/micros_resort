from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database.connection import get_db
from ..schemas.schemas import (
    UserCreate,
    UserUpdate,
    UserResponse,
    UserProfileUpdate,
    VerifyCredentialsRequest,
    ResetPasswordRequest,
    MessageResponse
)
from ..services.user_service import UserService
from ..api.dependencies import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=List[UserResponse])
def get_users(
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Listar todos los usuarios (solo admin)
    
    - **skip**: Número de registros a saltar
    - **limit**: Número máximo de registros a retornar
    """
    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Se requieren permisos de administrador"
        )
    
    service = UserService(db)
    users = service.get_all_users(skip, limit)
    return users


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtener usuario por ID
    
    Los usuarios pueden ver su propio perfil, admin puede ver cualquiera
    """
    # Verificar permisos
    if current_user.get("role") != "admin" and current_user.get("user_id") != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para ver este usuario"
        )
    
    service = UserService(db)
    return service.get_user_by_id(user_id)


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user_data: UserCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Crear nuevo usuario (solo admin)
    
    - **email**: Email único del usuario
    - **password**: Contraseña (mínimo 6 caracteres)
    - **first_name**: Nombre
    - **last_name**: Apellido
    - **phone**: Teléfono (opcional)
    - **role**: Rol del usuario (user o admin)
    """
    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Se requieren permisos de administrador"
        )
    
    service = UserService(db)
    return service.create_user(user_data)


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_data: UserUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Actualizar usuario
    
    Los usuarios pueden actualizar su propio perfil (excepto rol)
    Admin puede actualizar cualquier usuario
    """
    # Verificar permisos
    if current_user.get("role") != "admin" and current_user.get("user_id") != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para actualizar este usuario"
        )
    
    service = UserService(db)
    return service.update_user(user_id, user_data, current_user.get("role"))


@router.delete("/{user_id}", response_model=MessageResponse)
def delete_user(
    user_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Eliminar usuario (solo admin)
    """
    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Se requieren permisos de administrador"
        )
    
    service = UserService(db)
    service.delete_user(user_id)
    return MessageResponse(message="Usuario eliminado exitosamente")


@router.get("/profile/me", response_model=UserResponse)
def get_my_profile(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtener perfil del usuario actual
    """
    service = UserService(db)
    return service.get_user_by_id(current_user.get("user_id"))


@router.put("/profile/me", response_model=UserResponse)
def update_my_profile(
    profile_data: UserProfileUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Actualizar perfil del usuario actual
    
    - **first_name**: Nombre (opcional)
    - **last_name**: Apellido (opcional)
    - **phone**: Teléfono (opcional)
    """
    service = UserService(db)
    return service.update_profile(current_user.get("user_id"), profile_data)


# Endpoints internos para comunicación entre servicios
@router.post("/verify-credentials", response_model=UserResponse)
def verify_credentials(
    credentials: VerifyCredentialsRequest,
    db: Session = Depends(get_db)
):
    """
    Verificar credenciales de usuario (endpoint interno)
    
    Usado por Auth Service para validar login
    """
    service = UserService(db)
    return service.verify_credentials(credentials)


@router.put("/reset-password", response_model=MessageResponse)
def reset_password(
    reset_data: ResetPasswordRequest,
    db: Session = Depends(get_db)
):
    """
    Resetear contraseña (endpoint interno)
    
    Usado por Auth Service
    """
    service = UserService(db)
    service.reset_password(reset_data)
    return MessageResponse(message="Contraseña actualizada exitosamente")
