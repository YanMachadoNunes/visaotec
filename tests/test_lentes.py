
"""tests/test_lentes.py — rode com: pytest"""
 
import pytest
 
from visaotec.receita import Olho
from visaotec.lentes import (
    escolher_indice, lentes_da_armacao, lentes_da_receita, opcoes_compativeis,
    contar_orcamentos, gerar_orcamentos, tres_mais_baratas,
)
 
 
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
    assert lentes_da_armacao("parafusada") == {1.59}
    assert opcoes_compativeis(od, oe, "parafusada") == {1.59}
    assert opcoes_compativeis(od, oe, "aro fechado") == {1.59, 1.67, 1.74}
 
 
def test_intersecao_vazia_grau_alto_na_parafusada():
    od, oe = Olho(-5.0), Olho(-5.0)            # pede 1.67 ou maior
    assert opcoes_compativeis(od, oe, "parafusada") == set()
    assert tres_mais_baratas(od, oe, "parafusada") == []
 
 
def test_armacao_desconhecida():
    with pytest.raises(ValueError):
        lentes_da_armacao("de madeira")
 
 
def test_tres_mais_baratas_sem_adicao():
    r = tres_mais_baratas(Olho(-1.0), Olho(-1.25), "aro fechado")
    assert [o["preco"] for o in r] == [120.0, 220.0, 240.0]
    assert all(o["tipo"] == "visão simples" for o in r)
 
 
def test_tres_mais_baratas_respeita_armacao():
    r = tres_mais_baratas(Olho(-1.0), Olho(-1.0), "parafusada")
    assert len(r) == 3
    assert all(o["indice"] == 1.59 for o in r)
 
 
def test_tres_mais_baratas_com_adicao_nao_traz_visao_simples():
    od = Olho(-1.0, adicao=2.0)
    oe = Olho(-1.25, adicao=2.0)
    r = tres_mais_baratas(od, oe, "aro fechado")
    assert len(r) == 3
    assert all(o["tipo"] in {"bifocal", "multifocal"} for o in r)
    assert r[0]["preco"] == 270.0              # 1.50 (120) + bifocal (150)
 