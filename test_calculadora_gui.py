import unittest
from decimal import Decimal

from calculadora_gui import calcular, formatar_resultado


class CalculoTests(unittest.TestCase):
    def test_operacoes_basicas(self):
        casos = (
            ("12 + 3", Decimal("15")),
            ("12 - 20", Decimal("-8")),
            ("2.5 * 4", Decimal("10.0")),
            ("7 / 2", Decimal("3.5")),
        )
        for expressao, esperado in casos:
            with self.subTest(expressao=expressao):
                self.assertEqual(calcular(expressao), esperado)

    def test_aceita_operandos_negativos_e_decimais(self):
        self.assertEqual(calcular("-2.5 * -4"), Decimal("10.0"))
        self.assertEqual(calcular("5--2"), Decimal("7"))

    def test_divisao_por_zero_gera_erro(self):
        with self.assertRaises(ZeroDivisionError):
            calcular("10 / 0")

    def test_rejeita_entradas_invalidas(self):
        expressoes_invalidas = (
            "",
            "1 +",
            "1 + 2 + 3",
            "abc / 2",
            "1 // 2",
            "NaN + 1",
        )
        for expressao in expressoes_invalidas:
            with self.subTest(expressao=expressao):
                with self.assertRaises(ValueError):
                    calcular(expressao)

    def test_formata_resultado_sem_zeros_finais(self):
        self.assertEqual(formatar_resultado(Decimal("2.5000")), "2.5")
        self.assertEqual(formatar_resultado(Decimal("100")), "100")
        self.assertEqual(formatar_resultado(Decimal("-0.000")), "0")


if __name__ == "__main__":
    unittest.main()
