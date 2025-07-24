"""Testes para a ChatAPI e provedores."""

import unittest
from unittest.mock import patch, Mock

from core.chat_api import ChatAPI, provedores_suportados
from core.chat_api.provedores import (
    Maritaca,
    UnsupportedProviderError, UnsupportedProviderModelError
)


class TestChatAPIProviders(unittest.TestCase):
    """Testa a ChatAPI e os provedores suportados."""

    def test_maritaca_provider_registration(self):
        """Testa se o provedor Maritaca está registrado corretamente."""
        self.assertIn('maritaca', provedores_suportados)
        self.assertEqual(Maritaca.placeholer(), 'maritaca')
        self.assertIsInstance(Maritaca.modelos(), list)
        self.assertGreater(len(Maritaca.modelos()), 0)

    def test_all_providers_registered(self):
        """Testa se todos os provedores estão registrados."""
        expected_providers = ['openai', 'gemini', 'deepseek', 'maritaca']
        for provider in expected_providers:
            self.assertIn(provider, provedores_suportados)

    def test_maritaca_chat_api_instantiation(self):
        """Testa a criação de uma instância ChatAPI com Maritaca."""
        api = ChatAPI('maritaca', 'sabia-2-medium', 'test-key')
        self.assertEqual(api.provedor, 'maritaca')
        self.assertEqual(api.modelo, 'sabia-2-medium')
        self.assertEqual(api.api_url, 'https://chat.maritaca.ai/api/chat/completions')

    def test_unsupported_provider_error(self):
        """Testa erro para provedor não suportado."""
        with self.assertRaises(UnsupportedProviderError):
            ChatAPI('provider_inexistente', 'model', 'key')

    def test_unsupported_model_error(self):
        """Testa erro para modelo não suportado."""
        with self.assertRaises(UnsupportedProviderModelError):
            ChatAPI('maritaca', 'modelo_inexistente', 'key')

    @patch('core.chat_api.requests.post')
    def test_maritaca_api_call(self, mock_post):
        """Testa uma chamada para a API do Maritaca."""
        # Mock da resposta da API
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{
                "message": {
                    "content": "Resposta do Maritaca"
                }
            }]
        }
        mock_post.return_value = mock_response

        api = ChatAPI('maritaca', 'sabia-2-medium', 'test-key')
        result = api.gera_conteudo("Contexto", "Prompt")

        # Verifica se a requisição foi feita corretamente
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        
        # Verifica URL
        self.assertEqual(args[0], 'https://chat.maritaca.ai/api/chat/completions')

        # Verifica headers
        expected_headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer test-key"
        }
        self.assertEqual(kwargs['headers'], expected_headers)

        # Verifica payload
        expected_payload = {
            "model": "sabia-2-medium",
            "messages": [
                {"role": "system", "content": "Contexto"},
                {"role": "user", "content": "Prompt"}
            ]
        }
        self.assertEqual(kwargs['json'], expected_payload)

        # Verifica resultado
        self.assertEqual(result, "Resposta do Maritaca")

    def test_maritaca_models(self):
        """Testa os modelos disponíveis do Maritaca."""
        models = Maritaca.modelos()
        expected_models = ["sabia-2", "sabia-2-small", "sabia-2-medium"]
        self.assertEqual(models, expected_models)


if __name__ == '__main__':
    unittest.main(verbosity=2)
