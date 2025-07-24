"""Testes para o módulo de preprocessamento."""

import unittest
from core.preprocessamento import remover_acentos


class TestPreprocessamento(unittest.TestCase):
    """Testa as funções de preprocessamento de texto."""

    def test_remover_acentos_texto_com_acentos(self):
        """Testa remoção de acentos em texto com acentos."""
        texto = "Educação é fundamental"
        resultado = remover_acentos(texto)
        esperado = "Educacao e fundamental"
        self.assertEqual(resultado, esperado)

    def test_remover_acentos_texto_sem_acentos(self):
        """Testa remoção de acentos em texto sem acentos."""
        texto = "Brasil tem futuro"
        resultado = remover_acentos(texto)
        esperado = "Brasil tem futuro"
        self.assertEqual(resultado, esperado)

    def test_remover_acentos_texto_vazio(self):
        """Testa remoção de acentos em texto vazio."""
        texto = ""
        resultado = remover_acentos(texto)
        esperado = ""
        self.assertEqual(resultado, esperado)

    def test_remover_acentos_caracteres_especiais(self):
        """Testa remoção de acentos com caracteres especiais."""
        texto = "São Paulo - 123!@#"
        resultado = remover_acentos(texto)
        esperado = "Sao Paulo - 123!@#"
        self.assertEqual(resultado, esperado)

    def test_remover_acentos_acentos_diversos(self):
        """Testa remoção de diferentes tipos de acentos."""
        texto = "ção, ão, ês, áéíóú, àèìòù, âêîôû, ãõ, ç"
        resultado = remover_acentos(texto)
        esperado = "cao, ao, es, aeiou, aeiou, aeiou, ao, c"
        self.assertEqual(resultado, esperado)


if __name__ == '__main__':
    unittest.main()