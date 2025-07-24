"""JWT Authentication Module"""

import os
from datetime import datetime, timedelta
from typing import Dict, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

# Configurações JWT
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Configuração de senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Esquema de segurança
security = HTTPBearer()

# Usuário simples para demonstração (em produção, usar banco de dados)
DEMO_USER = {
    "username": "admin",
    "password_hash": pwd_context.hash("admin123"),  # senha: admin123
}


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class User(BaseModel):
    username: str


class UserInDB(User):
    password_hash: str


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica a senha."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Gera hash da senha."""
    return pwd_context.hash(password)


def authenticate_user(username: str, password: str) -> Optional[UserInDB]:
    """Autentica o usuário."""
    if username == DEMO_USER["username"]:
        user = UserInDB(username=username, password_hash=DEMO_USER["password_hash"])
        if verify_password(password, user.password_hash):
            return user
    return None


def create_access_token(data: Dict, expires_delta: Optional[timedelta] = None) -> str:
    """Cria token JWT de acesso."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    """Obtém o usuário atual a partir do token JWT."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token de autorização inválido",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    
    if token_data.username != DEMO_USER["username"]:
        raise credentials_exception
    
    return User(username=token_data.username)


# Função de dependência para verificação do token (compatibilidade)
def verificar_token(current_user: User = Depends(get_current_user)) -> bool:
    """Verifica se o token JWT é válido (mantém compatibilidade).
    Args:
        current_user (User): Usuário atual obtido do token.
    Returns:
        bool: True se o token for válido.
    """
    return True
