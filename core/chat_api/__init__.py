"""
    ChatAPI é uma classe que faz a comunicação com os provedores de IA
    para gerar respostas a partir de um contexto e um prompt.
    A classe é responsável por fazer a requisição HTTP para o provedor
    e tratar o retorno para retornar apenas o conteúdo da resposta.
"""
import requests
from core.chat_api.provedores import Gemini
from core.chat_api.provedores import OpenAI
from core.chat_api.provedores import DeepSeek
from core.chat_api.provedores import UnsupportedProviderError
from core.chat_api.provedores import UnsupportedProviderModelError

provedores_suportados = {
    OpenAI.placeholer(): {
        "modelos": OpenAI.modelos(),
        "api_url": "https://api.openai.com/v1/chat/completions"
    },
    Gemini.placeholer(): {
        "modelos": Gemini.modelos(),
        "api_url": "https://generativelanguage.googleapis.com/v1beta/models"
    },
    DeepSeek.placeholer(): {
        "modelos": DeepSeek.modelos(),
        "api_url": "https://api.deepseek.com/chat/completions"
    }
}

class ChatAPI:
    """
        ChatAPI é uma classe que faz a comunicação com os provedores de IA
    """
    def __init__(self, provedor="", modelo="", api_key=""):
        if provedor not in provedores_suportados:
            raise UnsupportedProviderError(provedor)

        if modelo not in provedores_suportados[provedor]["modelos"]:
            raise UnsupportedProviderModelError(provedor, modelo)

        self.provedor = provedor
        self.api_url = provedores_suportados[provedor]["api_url"]
        self.modelo = modelo
        self.api_key = api_key

    def ajusta_retorno(self, conteudo):
        """
            Ajusta o retorno da API para retornar apenas o conteúdo da resposta
        """
        return conteudo.replace("```json", "").replace("```", "")

    def gera_conteudo(self, contexto, prompt):
        """
            Gera o conteúdo da resposta a partir de um contexto e um prompt
        """
        url = self.api_url
        headers = {
            "Content-Type": "application/json"
        }

        payload = {}

        if self.provedor == "gemini" :
            url = f'{self.api_url}/{self.modelo}:generateContent?key={self.api_key}'
            payload = {
                "contents": [
                    {
                        "role": "model",
                        "parts": [{"text": contexto}]
                    },
                    {
                        "role": "user",
                        "parts": [{"text": prompt}]
                    }
                ]
            }
        else:
            headers["Authorization"] = f'Bearer {self.api_key}'
            payload = {
                "model": self.modelo,
                "messages": [
                    {"role": "system", "content": contexto},
                    {"role": "user", "content": prompt},
                ]
            }

        resp = requests.post(url, headers=headers, json=payload, timeout=60)

        if resp.status_code == 200 :
            data = resp.json()
            if self.provedor == "gemini" :
                candidates = data["candidates"]
                content = candidates[0]["content"]
                parts = content["parts"][0]
                return self.ajusta_retorno(parts["text"])

            choices = data["choices"][0]
            message = choices["message"]
            content = message["content"]
            return self.ajusta_retorno(content)

        error_message = f'{resp.text} - {resp.url} - {resp.status_code}'
        raise ConnectionError(f'Erro ao fazer a requisição: {error_message}')
