"""Módulo de execução da API."""

import json

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from core.constants import NEWS_PATH
from core.news import coletar_noticias, gerar_resumo_e_tema, load_feeds_json

app = FastAPI()


@app.get("/gerar_tema")
def generate_theme():
    """Gera um tema de redação baseado em notícias recentes.
    Args:
        None
    Returns:
        dict: Tema de redação.
    """
    # Coleta as notícias e gera o tema de redação
    news_source = load_feeds_json(NEWS_PATH)
    news_url = [news["URL"] for news in news_source]
    noticias = coletar_noticias(news_url)
    tema = gerar_resumo_e_tema(noticias)
    tema = json.loads(tema)
    # extrai o JSON
    tema_json = jsonable_encoder(tema)
    return JSONResponse(content=tema_json)
