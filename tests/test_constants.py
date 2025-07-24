"""Testes para o módulo constants."""

import unittest
from unittest.mock import patch
from core.constants import (
    NEWS_PATH, NUM_NOTICIAS, SIM_THRESHOLD, GUARDRAIL_MSG,
    temas_enem, termos_inapropriados
)


class TestConstants(unittest.TestCase):
    """Testa as constantes do projeto."""

    def test_news_path_value(self):
        """Testa se NEWS_PATH tem o valor esperado."""
        self.assertEqual(NEWS_PATH, "source/rss_source.json")

    def test_num_noticias_value(self):
        """Testa se NUM_NOTICIAS tem o valor esperado."""
        self.assertEqual(NUM_NOTICIAS, 3)
        self.assertIsInstance(NUM_NOTICIAS, int)

    def test_sim_threshold_value(self):
        """Testa se SIM_THRESHOLD tem o valor esperado."""
        self.assertEqual(SIM_THRESHOLD, 0.7)
        self.assertIsInstance(SIM_THRESHOLD, float)

    def test_guardrail_msg_format(self):
        """Testa se GUARDRAIL_MSG tem formato correto."""
        self.assertEqual(GUARDRAIL_MSG, "Tema inapropriado: %s")
        # Testa se pode ser formatada
        formatted = GUARDRAIL_MSG % "teste"
        self.assertEqual(formatted, "Tema inapropriado: teste")

    def test_temas_enem_structure(self):
        """Testa a estrutura dos temas ENEM."""
        self.assertIsInstance(temas_enem, dict)
        # Verifica se contém os anos esperados
        self.assertIn(1998, temas_enem)
        self.assertIn(2023, temas_enem)
        
        # Verifica alguns temas específicos
        self.assertEqual(temas_enem[1998], "Viver e aprender")
        self.assertEqual(temas_enem[2023], "Desafios do envelhecimento populacional no Brasil")

    def test_temas_enem_all_years_present(self):
        """Testa se todos os anos de 1998 a 2023 estão presentes."""
        for ano in range(1998, 2024):
            self.assertIn(ano, temas_enem, f"Ano {ano} não encontrado nos temas ENEM")

    def test_temas_enem_values_are_strings(self):
        """Testa se todos os valores dos temas são strings."""
        for ano, tema in temas_enem.items():
            self.assertIsInstance(tema, str, f"Tema do ano {ano} não é string")
            self.assertTrue(len(tema) > 0, f"Tema do ano {ano} está vazio")

    def test_termos_inapropriados_structure(self):
        """Testa a estrutura dos termos inapropriados."""
        self.assertIsInstance(termos_inapropriados, list)
        self.assertTrue(len(termos_inapropriados) > 0)
        
        # Verifica alguns termos específicos
        self.assertIn("impuros", termos_inapropriados)
        self.assertIn("morte", termos_inapropriados)
        self.assertIn("limpeza étnica", termos_inapropriados)

    def test_termos_inapropriados_all_strings(self):
        """Testa se todos os termos inapropriados são strings."""
        for termo in termos_inapropriados:
            self.assertIsInstance(termo, str, f"Termo '{termo}' não é string")
            self.assertTrue(len(termo) > 0, f"Termo vazio encontrado")

    def test_termos_inapropriados_no_duplicates(self):
        """Testa se não há termos duplicados."""
        unique_terms = set(termos_inapropriados)
        self.assertEqual(len(unique_terms), len(termos_inapropriados), 
                        "Existem termos duplicados na lista")

    @patch.dict('os.environ', {
        'PROVIDER1': 'test_provider1',
        'PROVIDER1_API_KEY': 'test_key1',
        'MODEL1': 'test_model1',
        'PROVIDER2': 'test_provider2',
        'PROVIDER2_API_KEY': 'test_key2',
        'MODEL2': 'test_model2'
    })
    def test_environment_variables_loading(self):
        """Testa se as variáveis de ambiente são carregadas corretamente."""
        # Reimportar o módulo para aplicar as variáveis de ambiente mocadas
        import importlib
        import core.constants
        importlib.reload(core.constants)
        
        self.assertEqual(core.constants.PROVIDER1, 'test_provider1')
        self.assertEqual(core.constants.PROVIDER1_API_KEY, 'test_key1')
        self.assertEqual(core.constants.MODEL1, 'test_model1')
        self.assertEqual(core.constants.PROVIDER2, 'test_provider2')
        self.assertEqual(core.constants.PROVIDER2_API_KEY, 'test_key2')
        self.assertEqual(core.constants.MODEL2, 'test_model2')

    def test_constants_immutability_attempt(self):
        """Testa se as constantes importantes são do tipo correto."""
        # Verificar tipos das constantes principais
        self.assertIsInstance(NEWS_PATH, str)
        self.assertIsInstance(NUM_NOTICIAS, int)
        self.assertIsInstance(SIM_THRESHOLD, float)
        self.assertIsInstance(GUARDRAIL_MSG, str)
        self.assertIsInstance(temas_enem, dict)
        self.assertIsInstance(termos_inapropriados, list)


if __name__ == '__main__':
    unittest.main()