import unittest

from r37_modular import R37Hibridismo


class TestR37Hibridismo(unittest.TestCase):
    def setUp(self):
        self.r37 = R37Hibridismo('medico')

    def test_comprimido_retorna_5_bytes(self):
        fatores, payload_len, hmac_hex = self.r37.comprimir_r37('paciente relata dor temporal com bruxismo')
        self.assertEqual(len(fatores), 5)
        self.assertGreater(payload_len, 0)
        self.assertTrue(len(hmac_hex) > 20)

    def test_reproducao_deterministica(self):
        msg = 'paciente relata dor temporal com bruxismo'
        a = self.r37.comprimir_r37(msg)
        b = self.r37.comprimir_r37(msg)
        self.assertEqual(a, b)

    def test_descompressao_simulada(self):
        msg = 'paciente relata dor temporal com bruxismo'
        fatores, _, hmac_hex = self.r37.comprimir_r37(msg)
        resultado = self.r37.descomprimir_r37_simulado(fatores, hmac_hex)
        self.assertIn('fator1_palavra_inicial', resultado)
        self.assertIn('hmac_para_validacao', resultado)


if __name__ == '__main__':
    unittest.main()
