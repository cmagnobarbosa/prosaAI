"""Módulo para coleta e processamento de notícias."""
import json
import logging
import random

import feedparser

from core.constants import (temas_enem, NUM_NOTICIAS )

from core.constants import (PROVIDER1, PROVIDER1_API_KEY, MODEL1)

from core.guardrails import (checar_tema_enem_analise_sintatica,
                             checar_tema_enem_semantica,
                             checar_tema_enem_por_llm)
from core.servico_llm import make_llm_call

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def coletar_noticias(feeds):
    """Coleta e consolida notícias dos feeds RSS.
    Args:
        feeds (list): Lista de URLs de feeds RSS.
    Returns:
        list: Lista de notícias.
    """
    noticias = []
    for feed_url in feeds:
        noticias.extend(parse_feed(feed_url))
    return noticias


def parse_feed(feed_url):
    """
    Coleta e consolida notícias de um feed RSS.

    Args:
        feed_url (str): URL of the RSS feed.
    Returns:
        list: List of news entries.
    """
    feed = feedparser.parse(feed_url)
    entries = []
    for entry in feed.get('entries', []):
        try:
            entries.append(
                {
                    "titulo": entry.title,
                    "descricao": entry.description,
                    "link": entry.link,
                }
            )
        except AttributeError as e:
            logger.error("Erro ao coletar notícia: %s", e)
    return entries


def build_prompt(texto_noticias):
    """
    Gera o prompt.
    Args:
        texto_noticias (str)
    Return:
        str: prompt
    """

    response_schema = {
        "resumo": "resumo dos principais temas abordados",
        "tema": "Tema da redação sugerido em português",
        "instrucoes": "instruções em português",
    }
    tarefa = (
        "### Instruções ###\n"
        "1. Forneça um resumo dos principais temas abordados.\n\n"
        "2. Sugira um tema de redação com título e instruções em português\n\n"
        "3. Siga o padrão do ENEM (Exame nacional do Ensino Médio)"
        "4. Adicione recomendação do"
        " número mínimo de linhas e máximo de linhas.\n\n"
    )

    prompt = (
        f"Aqui está um conjunto de notícias recentes:\n\n"
        f" ### Notícias ###\n"
        f"{texto_noticias}\n\n"
        f"### Exemplo de Tema ENEM ###\n"
        f"{random.choice(list(temas_enem.values()))}\n\n"
        f"{tarefa}\n\n"
        f"Devolva a resposta em formato JSON:\n\n"
        f"{response_schema}"
    )
    return prompt


def gerar_resumo_e_tema(noticias):
    """Gera um resumo e um tema de redação considerando as notícias fornecidas.
    Args:
        noticias (list): Lista de notícias.
    Returns:
        str: Resumo e tema de redação
    """

    random.shuffle(noticias)
    # embaralha as notícias e seleciona as 3 primeiras
    noticias = noticias[:NUM_NOTICIAS]
    # Consolida descrições das notícias em um único texto
    texto_noticias = " ".join([noticia["descricao"] for noticia in noticias])
    prompt = build_prompt(texto_noticias)
    contexto = "Você é gerador de temas de redação no Formato ENEM"
    response = make_llm_call(PROVIDER1, MODEL1, contexto, prompt, PROVIDER1_API_KEY)
    tema_sugerido = json.loads(response)

    # Abordagem de validação do tema por três camadas.
    # sobrescreve a situação para testar o validador ético
    if checar_tema_enem_analise_sintatica(tema_sugerido["tema"]):
        return response
    # checa tema por analise semantica
    if checar_tema_enem_semantica(tema_sugerido["tema"]):
        return response

    if checar_tema_enem_por_llm(tema_sugerido["tema"]):
        return response
    logger.warning("Tema inapropriado: %s", tema_sugerido["tema"])
    return "Tema inapropriado"


def load_feeds_json(path_to_json):
    """Carrega feeds RSS de um arquivo JSON.
    Args:
        path_to_json (str): Caminho para o arquivo JSON.
    Returns:
        list: Lista de feeds RSS.

    """
    with open(path_to_json, "r", encoding="utf-8") as file:
        feeds = json.load(file)
    return feeds
