from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional, Dict
import httpx
from ..models.models import AuthToken
from ..schemas.schemas import RegisterRequest, LoginRequest, TokenResponse, VerifyTokenResponse
from ..utils.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
    get_token_expiration
)
from ..config import settings
from fastapi import HTTPException, status


class AuthService:
    """Servicio de autenticación"""
    
    def __init__(self, db: Session):
        self.db = db
    
    async def register_user(self, user_data: RegisterRequest) -> TokenResponse:
        """Registrar nuevo usuario"""
        # Crear usuario en User Service
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{settings.USER_SERVICE_URL}/users/",
                    json={
                        "email": user_data.email,
                        "password": user_data.password,
                        "first_name": user_data.first_name,
                        "last_name": user_data.last_name,
                        "phone": user_data.phone,
                        "role": "user"
                    }
                )
                
                if response.status_code != 201:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Error al crear usuario"
                    )
                
                user = response.json()
                
                # Crear tokens
                return self._create_tokens_for_user(user)
                
            except httpx.RequestError:
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail="User Service no disponible"
                )
    
    async def login_user(self, login_data: LoginRequest) -> TokenResponse:
        """Iniciar sesión de usuario"""
        # Verificar credenciales en User Service
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{settings.USER_SERVICE_URL}/users/verify-credentials",
                    json={
                        "email": login_data.email,
                        "password": login_data.password
                    }
                )
                
                if response.status_code != 200:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Credenciales inválidas"
                    )
                
                user = response.json()
                
                # Crear tokens
                return self._create_tokens_for_user(user)
                
            except httpx.RequestError:
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail="User Service no disponible"
                )
    
    def _create_tokens_for_user(self, user: Dict) -> TokenResponse:
        """Crear tokens de acceso y refresco para un usuario"""
        # Datos para el token
        token_data = {
            "sub": str(user["id"]),
            "email": user["email"],
            "role": user["role"]
        }
        
        # Crear tokens
        access_token = create_access_token(token_data)
        refresh_token = create_refresh_token({"sub": str(user["id"])})
        
        # Guardar en base de datos
        expires_at = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        
        db_token = AuthToken(
            user_id=user["id"],
            token=access_token,
            refresh_token=refresh_token,
            expires_at=expires_at
        )
        
        self.db.add(db_token)
        self.db.commit()
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )
    
    def refresh_access_token(self, refresh_token: str) -> TokenResponse:
        """Refrescar token de acceso"""
        # Decodificar refresh token
        payload = decode_token(refresh_token)
        
        if not payload or payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token inválido"
            )
        
        # Verificar que el token existe y no está revocado
        db_token = self.db.query(AuthToken).filter(
            AuthToken.refresh_token == refresh_token,
            AuthToken.revoked == False
        ).first()
        
        if not db_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token no válido o revocado"
            )
        
        # Obtener información del usuario
        user_id = int(payload["sub"])
        
        # Crear nuevo access token
        token_data = {
            "sub": str(user_id),
            "email": payload.get("email"),
            "role": payload.get("role")
        }
        
        access_token = create_access_token(token_data)
        
        # Actualizar token en base de datos
        db_token.token = access_token
        db_token.expires_at = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        self.db.commit()
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )
    
    def logout_user(self, token: str) -> bool:
        """Cerrar sesión revocando el token"""
        db_token = self.db.query(AuthToken).filter(
            AuthToken.token == token
        ).first()
        
        if db_token:
            db_token.revoked = True
            self.db.commit()
            return True
        
        return False
    
    def verify_token(self, token: str) -> VerifyTokenResponse:
        """Verificar validez del token"""
        # Verificar que no esté revocado
        db_token = self.db.query(AuthToken).filter(
            AuthToken.token == token,
            AuthToken.revoked == False
        ).first()
        
        if not db_token:
            return VerifyTokenResponse(valid=False)
        
        # Decodificar token
        payload = decode_token(token)
        
        if not payload:
            return VerifyTokenResponse(valid=False)
        
        return VerifyTokenResponse(
            valid=True,
            user_id=int(payload["sub"]),
            email=payload.get("email"),
            role=payload.get("role")
        )
    
    async def reset_password(self, email: str, new_password: str) -> bool:
        """Restablecer contraseña de usuario"""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.put(
                    f"{settings.USER_SERVICE_URL}/users/reset-password",
                    json={
                        "email": email,
                        "new_password": new_password
                    }
                )
                
                return response.status_code == 200
                
            except httpx.RequestError:
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail="User Service no disponible"
                )
