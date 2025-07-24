"""Auth"""

import os

from fastapi import Header, HTTPException


# Função de dependência para verificação do token
def verificar_token(authorization: str = Header(...)):
    """Verifica se o token de autorização é válido.
    Args:
        authorization (str): Token de autorização.
    Raises:
        HTTPException: Erro de autenticação.
    """
    api_token = os.getenv("UAI_API_TOKEN")
    if authorization != f"Bearer {api_token}":
        raise HTTPException(status_code=401, detail="Token de autorização inválido")
    return True
