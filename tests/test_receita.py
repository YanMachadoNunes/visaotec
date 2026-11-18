"""tests/test_receita.py — rode com: pytest"""

from visaotec.receita import (
    Olho, transpor_cilindro, para_cilindro_negativo,
    grau_perto, equivalente_esferico, validar,
)


def test_transpor_exemplo_classico():
    # +1,00 -2,00 x 180  ->  -1,00 +2,00 x 90
    assert transpor_cilindro(Olho(1.0, -2.0, 180)) == Olho(-1.0, 2.0, 90)


def test_transpor_eixo_90_vira_180():
    assert transpor_cilindro(Olho(-1.0, 2.0, 90)) == Olho(1.0, -2.0, 180)


def test_transpor_duas_vezes_volta_ao_original():
    olho = Olho(-2.25, -1.50, 35)
    assert transpor_cilindro(transpor_cilindro(olho)) == olho


def test_transpor_sem_cilindro_nao_altera():
    olho = Olho(-3.0, 0.0, 0)
    assert transpor_cilindro(olho) == olho


def test_para_cilindro_negativo():
    assert para_cilindro_negativo(Olho(-1.0, 2.0, 90)) == Olho(1.0, -2.0, 180)
    assert para_cilindro_negativo(Olho(1.0, -2.0, 180)) == Olho(1.0, -2.0, 180)


def test_grau_perto():
    assert grau_perto(Olho(-1.0, -0.5, 90, 2.0)) == Olho(1.0, -0.5, 90, 0.0)


def test_equivalente_esferico():
    assert equivalente_esferico(Olho(-2.0, -1.0, 180)) == -2.5


def test_validar_receita_correta():
    r = validar(Olho(-2.0, -0.75, 170), Olho(-1.75, -0.5, 10))
    assert r == {"erros": [], "alertas": []}


def test_validar_detecta_erros():
    r = validar(Olho(-2.1, -0.75, 200), Olho(-1.75))
    assert len(r["erros"]) == 2      # passo errado e eixo fora da faixa


def test_validar_alerta_anisometropia():
    r = validar(Olho(-5.0), Olho(-1.0))
    assert r["erros"] == [] and len(r["alertas"]) == 1