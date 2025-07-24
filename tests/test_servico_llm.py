"""Testes para o módulo servico_llm."""

import os
import unittest
from unittest.mock import patch, MagicMock
from core.servico_llm import make_llm_call, make_openai_call


class TestServicoLLM(unittest.TestCase):
    """Testa as funções de serviços LLM."""

    @patch('core.servico_llm.ChatAPI')
    def test_make_llm_call_success(self, mock_chat_api_class):
        """Testa chamada LLM bem-sucedida."""
        # Configurar mock
        mock_chat_api = MagicMock()
        mock_chat_api.gera_conteudo.return_value = "Resposta do modelo"
        mock_chat_api_class.return_value = mock_chat_api
        
        # Executar função
        resultado = make_llm_call(
            provider="openai",
            model="gpt-4",
            contexto="Você é um assistente útil",
            prompt="Olá",
            api_key="test_key"
        )
        
        # Verificar
        mock_chat_api_class.assert_called_once_with("openai", "gpt-4", "test_key")
        mock_chat_api.gera_conteudo.assert_called_once_with(
            "Você é um assistente útil", "Olá"
        )
        self.assertEqual(resultado, "Resposta do modelo")

    @patch('core.servico_llm.ChatAPI')
    def test_make_llm_call_without_api_key(self, mock_chat_api_class):
        """Testa chamada LLM sem chave API."""
        # Configurar mock
        mock_chat_api = MagicMock()
        mock_chat_api.gera_conteudo.return_value = "Resposta sem API key"
        mock_chat_api_class.return_value = mock_chat_api
        
        # Executar função sem api_key
        resultado = make_llm_call(
            provider="openai",
            model="gpt-3.5-turbo",
            contexto="Contexto de teste",
            prompt="Prompt de teste"
        )
        
        # Verificar
        mock_chat_api_class.assert_called_once_with("openai", "gpt-3.5-turbo", "")
        mock_chat_api.gera_conteudo.assert_called_once_with(
            "Contexto de teste", "Prompt de teste"
        )
        self.assertEqual(resultado, "Resposta sem API key")

    @patch('core.servico_llm.OpenAI')
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_openai_key'})
    def test_make_openai_call_success(self, mock_openai_class):
        """Testa chamada OpenAI bem-sucedida."""
        # Configurar mock
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_choice = MagicMock()
        mock_message = MagicMock()
        
        mock_message.content = '{"resposta": "teste"}'
        mock_choice.message = mock_message
        mock_response.choices = [mock_choice]
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai_class.return_value = mock_client
        
        # Executar função
        resultado = make_openai_call(
            contexto="Você é um assistente",
            prompt="Teste",
            model_choice="gpt-4o-mini"
        )
        
        # Verificar
        mock_openai_class.assert_called_once_with(api_key="test_openai_key")
        mock_client.chat.completions.create.assert_called_once_with(
            model="gpt-4o-mini",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": "Você é um assistente"},
                {"role": "user", "content": "Teste"},
            ],
        )
        self.assertEqual(resultado, '{"resposta": "teste"}')

    @patch('core.servico_llm.OpenAI')
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test_openai_key'})
    def test_make_openai_call_default_model(self, mock_openai_class):
        """Testa chamada OpenAI com modelo padrão."""
        # Configurar mock
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_choice = MagicMock()
        mock_message = MagicMock()
        
        mock_message.content = '{"resultado": "padrão"}'
        mock_choice.message = mock_message
        mock_response.choices = [mock_choice]
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai_class.return_value = mock_client
        
        # Executar função sem especificar modelo
        resultado = make_openai_call(
            contexto="Sistema",
            prompt="Pergunta"
        )
        
        # Verificar que o modelo padrão foi usado
        mock_client.chat.completions.create.assert_called_once_with(
            model="gpt-4o-mini",  # modelo padrão
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": "Sistema"},
                {"role": "user", "content": "Pergunta"},
            ],
        )
        self.assertEqual(resultado, '{"resultado": "padrão"}')

    @patch('core.servico_llm.OpenAI')
    def test_make_openai_call_no_api_key(self, mock_openai_class):
        """Testa chamada OpenAI sem chave API no ambiente."""
        # Configurar mock para simular ausência de API key
        mock_openai_class.return_value = MagicMock()
        
        # Executar função sem OPENAI_API_KEY no ambiente
        resultado = make_openai_call(
            contexto="Sistema",
            prompt="Pergunta"
        )
        
        # Verificar que o OpenAI foi chamado com api_key=None
        mock_openai_class.assert_called_once_with(api_key=None)


if __name__ == '__main__':
    unittest.main()