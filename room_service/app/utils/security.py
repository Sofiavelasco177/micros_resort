from passlib.context import CryptContext
from jose import JWTError, jwt
from typing import Optional, Dict
from ..config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def decode_token(token: str) -> Optional[Dict]:
    """Decodificar y validar token JWT"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None
