"""Testes para autenticação JWT."""

from datetime import datetime, timedelta

import pytest
from jose import jwt

from core.authentication import (
    ALGORITHM,
    SECRET_KEY,
    authenticate_user,
    create_access_token,
    get_password_hash,
    verify_password,
)


class TestAuthentication:
    """Testes para funcionalidades de autenticação."""

    def test_verify_password(self):
        """Testa verificação de senha."""
        password = "test123"
        hashed = get_password_hash(password)
        assert verify_password(password, hashed)
        assert not verify_password("wrong", hashed)

    def test_authenticate_user_valid(self):
        """Testa autenticação com credenciais válidas."""
        user = authenticate_user("admin", "admin123")
        assert user is not None
        assert user.username == "admin"

    def test_authenticate_user_invalid_username(self):
        """Testa autenticação com username inválido."""
        user = authenticate_user("invalid", "admin123")
        assert user is None

    def test_authenticate_user_invalid_password(self):
        """Testa autenticação com senha inválida."""
        user = authenticate_user("admin", "wrongpassword")
        assert user is None

    def test_create_access_token(self):
        """Testa criação de token JWT."""
        data = {"sub": "testuser"}
        token = create_access_token(data)
        
        # Decodifica o token para verificar
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        assert payload["sub"] == "testuser"
        assert "exp" in payload

    def test_create_access_token_with_expires_delta(self):
        """Testa criação de token JWT com tempo de expiração customizado."""
        data = {"sub": "testuser"}
        expires_delta = timedelta(minutes=60)
        token = create_access_token(data, expires_delta)
        
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        exp_time = datetime.fromtimestamp(payload["exp"])
        expected_time = datetime.utcnow() + expires_delta
        
        # Verifica se o tempo de expiração está próximo do esperado (margem de 1 minuto)
        assert abs((exp_time - expected_time).total_seconds()) < 60

    def test_token_expiration(self):
        """Testa token expirado."""
        # Cria token que expira imediatamente
        data = {"sub": "testuser"}
        expired_token = create_access_token(
            data, expires_delta=timedelta(seconds=-1)
        )
        
        # Tentar decodificar token expirado deve falhar
        with pytest.raises(jwt.ExpiredSignatureError):
            jwt.decode(expired_token, SECRET_KEY, algorithms=[ALGORITHM])

    def test_invalid_token_signature(self):
        """Testa token com assinatura inválida."""
        data = {"sub": "testuser"}
        token = create_access_token(data)
        
        # Modifica o token para invalidar a assinatura
        invalid_token = token[:-5] + "wrong"
        
        with pytest.raises(jwt.JWTError):
            jwt.decode(invalid_token, SECRET_KEY, algorithms=[ALGORITHM])