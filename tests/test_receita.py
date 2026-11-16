"""Testes do módulo de receita. Rodar com: pytest

TODO: escrever os valores esperados fazendo as contas à mão primeiro.
"""
from visaotec.receita import Olho


def test_exemplo_estrutura():
    olho = Olho(esferico=-2.00, cilindrico=-1.00, eixo=90)
    assert olho.eixo == 90


# def test_transposicao():
#     resultado = transpor_cilindro(Olho(+1.00, -2.00, 30))
#     assert resultado == Olho(?, ?, ?)
#
# def test_transposicao_eixo_acima_de_90(): ...
# def test_grau_perto(): ...
# def test_equivalente_esferico(): ...
