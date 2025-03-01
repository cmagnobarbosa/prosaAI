"""
Contém funções que validam o tema da redação.
"""

import json
import logging

from sentence_transformers import SentenceTransformer, util

from core.constants import (GUARDRAIL_MSG, SIM_THRESHOLD, termos_inapropriados)

from core.constants import (PROVIDER1, PROVIDER1_API_KEY, MODEL1)

from core.preprocessamento import remover_acentos
from core.servico_llm import make_llm_call

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

EMB_MODEL = SentenceTransformer('paraphrase-MiniLM-L6-v2')


embeddings_termos = EMB_MODEL.encode(
    termos_inapropriados, convert_to_tensor=True)




def checar_tema_enem_semantica(tema):
    """
    Se o tema conter algum termo considerado inapropriado

    a função retorna False.

    Utiliza uma lista de termos combinada com
    embedding para calcular a similaridade.

    Args:
        tema (str): Tema da redação.

    Returns:
        bool: Se o tema é válido ou não.
    """

    logger.info("Validando tema com embedding...")
    # to lower case, remove accents and special characters
    tema = tema.lower()
    # remove accents
    tema = remover_acentos(tema)
    tema_embedding = EMB_MODEL.encode(tema, convert_to_tensor=True)
    similaridade = util.pytorch_cos_sim(tema_embedding, embeddings_termos)
    if similaridade.max() > SIM_THRESHOLD:
        logger.warning(GUARDRAIL_MSG, tema)
        return False
    return True


def checar_tema_enem_analise_sintatica(tema):
    """
    Se o tema conter algum termo considerado inapropriado
    a função retorna False.

    Args:
        tema (str): Tema da redação.
    Returns:
        bool: Se o tema é válido ou não.
    """
    # to lower case, remove accents and special characters
    tema = tema.lower()
    # remove accents
    tema = remover_acentos(tema)

    if any(termo in tema for termo in termos_inapropriados):
        logger.warning(GUARDRAIL_MSG, tema)
        return False
    return True


def checar_tema_enem_por_llm(tema):
    """Agente de LLM para checar se o tema da redação é ético.
    Args:
        tema (str): Tema da redação.
    Returns:
        bool: Se o tema é ético ou não.
    """
    contexto = ("Você é um agente de validação ética de temas de "
                "redação do ENEM.")
    tarefa = ("Valide se o tema da redação proposto não "
              "fere os direitos humanos.")
    formato_resposta = {
        "resposta": "sim/não",
        "justificativa": "justificativa da resposta",
    }
    prompt = (
        f"{contexto}\n\n"
        f"{tarefa}\n\n"
        f"### Tema da Redação ###\n"
        f"{tema}\n\n"
        f"Devolva a resposta em formato JSON:\n\n"
        f"{formato_resposta}"
    )
    # Usa um modelo mais poderoso para validar o tema
    # Escala de modelos: gpt-4o-mini < gpt-4o
    logger.info("Validando tema com modelo mais poderoso...")
    response = make_llm_call(PROVIDER1, MODEL1, contexto, prompt, PROVIDER1_API_KEY)
    response = json.loads(response)
    if "sim" in response['resposta']:
        return True
    logger.warning(GUARDRAIL_MSG, tema)
    return False
