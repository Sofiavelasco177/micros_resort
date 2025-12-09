from fastapi import Header, HTTPException, status
from typing import Optional, Dict
from ..utils.security import decode_token


def get_current_user(authorization: Optional[str] = Header(None)) -> Dict:
    """Dependency para obtener usuario actual del token"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token no proporcionado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = authorization.replace("Bearer ", "")
    payload = decode_token(token)
    
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return {
        "user_id": int(payload["sub"]),
        "email": payload.get("email"),
        "role": payload.get("role")
    }


def require_admin(current_user: Dict = Header(None, alias="authorization")) -> Dict:
    """Dependency para requerir rol de administrador"""
    user = get_current_user(current_user)
    
    if user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Se requieren permisos de administrador"
        )
    
    return user
