"""Testes para o módulo de exceptions."""

import unittest
from fastapi import HTTPException
from core.exceptions import (
    NewsNotFoundException, 
    NewsCollectionException, 
    NewsSummaryException,
    ParserError
)


class TestExceptions(unittest.TestCase):
    """Testa as exceções personalizadas."""

    def test_news_not_found_exception(self):
        """Testa a exceção NewsNotFoundException."""
        exception = NewsNotFoundException()
        self.assertIsInstance(exception, HTTPException)
        self.assertEqual(exception.status_code, 404)
        self.assertEqual(exception.detail, "No news found.")

    def test_news_collection_exception(self):
        """Testa a exceção NewsCollectionException."""
        exception = NewsCollectionException()
        self.assertIsInstance(exception, HTTPException)
        self.assertEqual(exception.status_code, 500)
        self.assertEqual(exception.detail, "Error collecting news.")

    def test_news_summary_exception(self):
        """Testa a exceção NewsSummaryException."""
        exception = NewsSummaryException()
        self.assertIsInstance(exception, HTTPException)
        self.assertEqual(exception.status_code, 500)
        self.assertEqual(exception.detail, "Error generating summary.")

    def test_parser_error_with_message(self):
        """Testa a exceção ParserError com mensagem personalizada."""
        message = "Erro ao analisar o feed RSS"
        exception = ParserError(message)
        self.assertIsInstance(exception, Exception)
        self.assertEqual(exception.message, message)
        self.assertEqual(str(exception), message)

    def test_parser_error_empty_message(self):
        """Testa a exceção ParserError com mensagem vazia."""
        message = ""
        exception = ParserError(message)
        self.assertIsInstance(exception, Exception)
        self.assertEqual(exception.message, message)
        self.assertEqual(str(exception), message)

    def test_parser_error_special_characters(self):
        """Testa a exceção ParserError com caracteres especiais."""
        message = "Erro com acentuação: não foi possível fazer o parsing!"
        exception = ParserError(message)
        self.assertIsInstance(exception, Exception)
        self.assertEqual(exception.message, message)
        self.assertEqual(str(exception), message)


if __name__ == '__main__':
    unittest.main()