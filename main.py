"""Módulo de execução da API."""

import json
from datetime import timedelta

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from openai import OpenAIError

from core.authentication import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    Token,
    User,
    authenticate_user,
    create_access_token,
    get_current_user,
)
from core.constants import NEWS_PATH
from core.news import coletar_noticias, gerar_resumo_e_tema, load_feeds_json

app = FastAPI(
    title="ProsaAI API",
    description="API para geração de temas de redação baseados em notícias recentes",
    version="1.0.0",
)


@app.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Endpoint de login para obter token JWT.
    
    Args:
        form_data: Dados do formulário com username e password.
        
    Returns:
        Token: Token JWT de acesso.
        
    Raises:
        HTTPException: Erro de autenticação.
    """
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nome de usuário ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/gerar_tema")
def gerar_tema(current_user: User = Depends(get_current_user)):
    """
    Gera um tema de redação baseado em notícias recentes.
    
    Args:
        current_user: Usuário autenticado via JWT.
        
    Returns:
        dict: Tema de redação.
    """
    # Coleta as notícias e gera o tema de redação
    fonte_noticias = load_feeds_json(NEWS_PATH)
    news_url = [news["URL"] for news in fonte_noticias]
    noticias = coletar_noticias(news_url)

    try:
        resumo_e_tema = gerar_resumo_e_tema(noticias)
        resumo_e_tema = json.loads(resumo_e_tema)
    except OpenAIError as error_summary:
        return JSONResponse(content={"error": str(error_summary)})

    # extrai o JSON
    tema_json = jsonable_encoder(resumo_e_tema)
    return JSONResponse(content=tema_json)


@app.get("/")
def root():
    """
    Endpoint raiz da API.
    
    Returns:
        dict: Informações básicas da API.
    """
    return {
        "message": "ProsaAI API",
        "version": "1.0.0",
        "endpoints": {
            "login": "/login - POST - Obter token JWT",
            "gerar_tema": "/gerar_tema - GET - Gerar tema de redação (requer autenticação)",
        }
    }
