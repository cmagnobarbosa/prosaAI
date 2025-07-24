"""Testes para o módulo de authentication."""

import os
import unittest
from unittest.mock import patch
from fastapi import HTTPException
from core.authentication import verificar_token


class TestAuthentication(unittest.TestCase):
    """Testa as funções de autenticação."""

    def setUp(self):
        """Configuração inicial para os testes."""
        # Remove a variável de ambiente se existir
        if 'UAI_API_TOKEN' in os.environ:
            del os.environ['UAI_API_TOKEN']

    def tearDown(self):
        """Limpeza após os testes."""
        # Remove a variável de ambiente se existir
        if 'UAI_API_TOKEN' in os.environ:
            del os.environ['UAI_API_TOKEN']

    @patch.dict(os.environ, {'UAI_API_TOKEN': 'test_token_123'})
    def test_verificar_token_valido(self):
        """Testa verificação com token válido."""
        authorization = "Bearer test_token_123"
        resultado = verificar_token(authorization)
        self.assertTrue(resultado)

    @patch.dict(os.environ, {'UAI_API_TOKEN': 'test_token_123'})
    def test_verificar_token_invalido(self):
        """Testa verificação com token inválido."""
        authorization = "Bearer token_invalido"
        with self.assertRaises(HTTPException) as context:
            verificar_token(authorization)
        
        self.assertEqual(context.exception.status_code, 401)
        self.assertEqual(context.exception.detail, "Token de autorização inválido")

    @patch.dict(os.environ, {'UAI_API_TOKEN': 'test_token_123'})
    def test_verificar_token_sem_bearer(self):
        """Testa verificação com token sem prefixo Bearer."""
        authorization = "test_token_123"
        with self.assertRaises(HTTPException) as context:
            verificar_token(authorization)
        
        self.assertEqual(context.exception.status_code, 401)
        self.assertEqual(context.exception.detail, "Token de autorização inválido")

    @patch.dict(os.environ, {'UAI_API_TOKEN': 'test_token_123'})
    def test_verificar_token_vazio(self):
        """Testa verificação com token vazio."""
        authorization = "Bearer "
        with self.assertRaises(HTTPException) as context:
            verificar_token(authorization)
        
        self.assertEqual(context.exception.status_code, 401)
        self.assertEqual(context.exception.detail, "Token de autorização inválido")

    @patch.dict(os.environ, {'UAI_API_TOKEN': ''})
    def test_verificar_token_env_vazio(self):
        """Testa verificação quando variável de ambiente está vazia."""
        authorization = "Bearer test_token_123"
        with self.assertRaises(HTTPException) as context:
            verificar_token(authorization)
        
        self.assertEqual(context.exception.status_code, 401)
        self.assertEqual(context.exception.detail, "Token de autorização inválido")

    def test_verificar_token_env_nao_definida(self):
        """Testa verificação quando variável de ambiente não está definida."""
        authorization = "Bearer test_token_123"
        with self.assertRaises(HTTPException) as context:
            verificar_token(authorization)
        
        self.assertEqual(context.exception.status_code, 401)
        self.assertEqual(context.exception.detail, "Token de autorização inválido")


if __name__ == '__main__':
    unittest.main()