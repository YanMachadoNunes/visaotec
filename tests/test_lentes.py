"""tests/test_lentes.py — rode com: pytest"""

import pytest

from visaotec.lentes import (
    contar_orcamentos,
    escolher_indice,
    gerar_orcamentos,
    lentes_da_armacao,
    lentes_da_receita,
    opcoes_compativeis,
    tres_mais_baratas,
)
from visaotec.receita import Olho


def test_contar_orcamentos_catalogo_completo():
    assert contar_orcamentos() == 48            # 4 × 3 × 4


def test_contagem_bate_com_a_lista_gerada():
    assert len(gerar_orcamentos()) == contar_orcamentos()


@pytest.mark.parametrize("esf, cil, esperado", [
    (-1.00, 0.0, 1.50),
    (-2.00, 0.0, 1.50),
    (-2.00, -1.00, 1.59),   # meridiano mais forte = -3,00
    (-4.00, 0.0, 1.59),
    (+5.00, 0.0, 1.67),
    (-7.00, 0.0, 1.74),
])
def test_escolher_indice(esf, cil, esperado):
    olho = Olho(esf, cil, 180 if cil else 0)
    assert escolher_indice(olho, Olho(0.0)) == esperado


def test_conjuntos_e_intersecao():
    od, oe = Olho(-3.0), Olho(-2.5)            # pede 1.59 ou maior
    assert lentes_da_receita(od, oe) == {1.59, 1.67, 1.74}
    assert lentes_da_armacao("parafusada") == {1.59, 1.67}
    assert opcoes_compativeis(od, oe, "parafusada") == {1.59, 1.67}


def test_armacao_desconhecida():
    with pytest.raises(ValueError):
        lentes_da_armacao("de madeira")


def test_tres_mais_baratas_sem_adicao():
    r = tres_mais_baratas(Olho(-1.0), Olho(-1.25), "aro fechado")
    assert [o["preco"] for o in r] == [120.0, 220.0, 240.0]
    assert all(o["tipo"] == "visão simples" for o in r)


def test_tres_mais_baratas_respeita_armacao():
    r = tres_mais_baratas(Olho(-1.0), Olho(-1.0), "parafusada")
    assert all(o["indice"] in {1.59, 1.67} for o in r)