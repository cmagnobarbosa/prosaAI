"""
    Módulo de provedores de API de chatbots.
"""
class Gemini:
    """
        Google Gemini API - https://ai.google.dev/gemini-api/docs
    """
    def __init__(self):
        """
            Inicializa a classe
        """

    @staticmethod
    def placeholer():
        """
            Retorna o nome do provedor
        """
        return "gemini"

    @staticmethod
    def modelos():
        """
            Retorna os modelos disponíveis para o provedor
        """
        # https://ai.google.dev/gemini-api/docs/models/gemini?hl=pt-br
        return ["gemini-2.0-flash",
                "gemini-2.0-flash-lite",
                "gemini-1.5-flash",
                "gemini-1.5-flash-8b",
                "gemini-1.5-pro"]

class OpenAI:
    """
        OpenAI API - https://platform.openai.com/docs/api-reference/chat
    """
    def __init__(self):
        """
            Inicializa a classe
        """

    @staticmethod
    def placeholer():
        """
            Retorna o nome do provedor
        """
        return "openai"

    @staticmethod
    def modelos():
        """
            Retorna os modelos disponíveis para o provedor
        """
        # https://platform.openai.com/docs/models#models-overview
        return ["gpt-4o",
                "gpt-4o-mini",
                "o1",
                "o3-mini",
                "gpt-4-turbo",
                "gpt-3.5-turbo"]

class DeepSeek:
    """
        DeepSeek API - https://api-docs.deepseek.com/quick_start/pricing
    """
    def __init__(self):
        """
            Inicializa a classe
        """

    @staticmethod
    def placeholer():
        """
            Retorna o nome do provedor
        """
        return "deepseek"

    @staticmethod
    def modelos():
        """
            Retorna os modelos disponíveis para o provedor
        """
        # https://api-docs.deepseek.com/quick_start/pricing
        return ["deepseek-chat"]

class UnsupportedProviderError(Exception):
    """
        Exceção lançada para provedores não suportados ou não implementados.
    """
    def __init__(self, provider, message="Provedor não suportado ou não implementado."):
        """
            Construtor da classe e inicialização da mensagem de erro.
        """
        self.provider = provider
        self.message = f"{message} Provedor fornecido: '{provider}'."
        super().__init__(self.message)

class UnsupportedProviderModelError(Exception):
    """
        Exceção lançada para modelos não suportados ou não implementados.
    """
    def __init__(self, provider, model, message="Modelo não suportado ou não implementado"):
        """
            Construtor da classe e inicialização da mensagem de erro.
        """
        self.provider = provider
        self.model = model
        self.message = f"{message} Modelo '{model}' não disponível para o provedor: '{provider}'"
        super().__init__(self.message)
