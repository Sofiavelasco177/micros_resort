from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi import HTTPException, status
from ..models.models import User
from ..schemas.schemas import UserCreate, UserUpdate, UserProfileUpdate, VerifyCredentialsRequest, ResetPasswordRequest
from ..utils.security import hash_password, verify_password


class UserService:
    """Servicio de gestión de usuarios"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_all_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Obtener todos los usuarios (solo admin)"""
        return self.db.query(User).offset(skip).limit(limit).all()
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Obtener usuario por ID"""
        user = self.db.query(User).filter(User.id == user_id).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        
        return user
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Obtener usuario por email"""
        return self.db.query(User).filter(User.email == email).first()
    
    def create_user(self, user_data: UserCreate) -> User:
        """Crear nuevo usuario"""
        # Verificar si el email ya existe
        existing_user = self.get_user_by_email(user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El email ya está registrado"
            )
        
        # Crear usuario
        db_user = User(
            email=user_data.email,
            password_hash=hash_password(user_data.password),
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            phone=user_data.phone,
            role=user_data.role
        )
        
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        
        return db_user
    
    def update_user(self, user_id: int, user_data: UserUpdate, current_user_role: str = None) -> User:
        """Actualizar usuario"""
        db_user = self.get_user_by_id(user_id)
        
        # Solo admin puede cambiar el rol
        if user_data.role and current_user_role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Solo administradores pueden cambiar roles"
            )
        
        # Actualizar campos
        update_data = user_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_user, field, value)
        
        self.db.commit()
        self.db.refresh(db_user)
        
        return db_user
    
    def delete_user(self, user_id: int) -> bool:
        """Eliminar usuario (solo admin)"""
        db_user = self.get_user_by_id(user_id)
        
        self.db.delete(db_user)
        self.db.commit()
        
        return True
    
    def update_profile(self, user_id: int, profile_data: UserProfileUpdate) -> User:
        """Actualizar perfil propio"""
        db_user = self.get_user_by_id(user_id)
        
        # Actualizar campos permitidos
        update_data = profile_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_user, field, value)
        
        self.db.commit()
        self.db.refresh(db_user)
        
        return db_user
    
    def verify_credentials(self, credentials: VerifyCredentialsRequest) -> User:
        """Verificar credenciales de usuario"""
        user = self.get_user_by_email(credentials.email)
        
        if not user or not verify_password(credentials.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales inválidas"
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Usuario inactivo"
            )
        
        return user
    
    def reset_password(self, reset_data: ResetPasswordRequest) -> bool:
        """Resetear contraseña de usuario"""
        user = self.get_user_by_email(reset_data.email)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        
        user.password_hash = hash_password(reset_data.new_password)
        self.db.commit()
        
        return True
