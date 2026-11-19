"""tests/test_previsao.py — rode com: pytest"""

import pandas as pd
import pytest

from visaotec.previsao import treinar, prever, avaliar


def mensal_em_reta():
    """Dados que formam uma reta exata: 1000 + 100 por mês."""
    meses = [f"2026-{m:02d}" for m in range(1, 7)]
    return pd.DataFrame({"mes": meses, "faturamento": [1000 + 100 * i for i in range(6)]})


def test_treinar_recupera_a_reta():
    t = treinar(mensal_em_reta())
    assert t["a"] == pytest.approx(100)
    assert t["b"] == pytest.approx(1000)
    assert t["r2"] == pytest.approx(1.0)
    assert t["mae"] == pytest.approx(0, abs=1e-6)


def test_prever_continua_a_reta_e_vira_o_ano():
    previsao = prever(treinar(mensal_em_reta()), meses=8)
    assert list(previsao["mes"][:2]) == ["2026-07", "2026-08"]
    assert previsao["mes"].iloc[-1] == "2027-02"
    assert previsao["previsto"].iloc[0] == pytest.approx(1600)


def test_avaliar_sem_erro_em_dados_lineares():
    r = avaliar(mensal_em_reta(), meses_teste=2)
    assert r["mae"] == pytest.approx(0, abs=1e-6)


def test_poucos_meses():
    with pytest.raises(ValueError):
        treinar(mensal_em_reta().head(2))
        