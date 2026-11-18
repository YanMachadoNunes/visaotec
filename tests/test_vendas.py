import sqlite3

import pytest

from visaotec.vendas import carregar_vendas, ranking_produtos, faturamento_mensal


@pytest.fixture
def df():
    """Banco em memória com poucas vendas, para conferir as contas à mão."""
    conn = sqlite3.connect(":memory:")
    conn.executescript("""
        CREATE TABLE produtos (id INTEGER PRIMARY KEY, categoria TEXT, nome TEXT, preco REAL);
        CREATE TABLE vendas (id INTEGER PRIMARY KEY, data TEXT, produto_id INTEGER,
                             quantidade INTEGER, valor REAL);
        INSERT INTO produtos VALUES (1, 'armacao', 'Aurora', 189.90),
                                    (2, 'armacao', 'Bruma', 249.90),
                                    (3, 'lente', 'Resina 1.50', 120.00);
        INSERT INTO vendas (data, produto_id, quantidade, valor) VALUES
            ('2026-01-05', 1, 1, 189.90),
            ('2026-01-20', 1, 1, 170.91),
            ('2026-01-20', 3, 1, 120.00),
            ('2026-02-03', 2, 1, 249.90),
            ('2026-02-03', 3, 1, 120.00);
    """)
    yield carregar_vendas(conn)
    conn.close()


def test_ranking_geral(df):
    r = ranking_produtos(df)
    assert list(r["nome"]) == ["Aurora", "Resina 1.50", "Bruma"]
    assert r.loc[0, "quantidade"] == 2
    assert r.loc[0, "faturamento"] == pytest.approx(360.81)


def test_ranking_por_categoria_e_top(df):
    r = ranking_produtos(df, categoria="armacao", top=1)
    assert list(r["nome"]) == ["Aurora"]


def test_faturamento_mensal(df):
    m = faturamento_mensal(df)
    assert list(m["mes"]) == ["2026-01", "2026-02"]
    assert list(m["faturamento"]) == [pytest.approx(480.81), pytest.approx(369.90)]
    assert list(m["itens"]) == [3, 2]


def test_faturamento_mensal_por_categoria(df):
    m = faturamento_mensal(df, categoria="lente")
    assert list(m["faturamento"]) == [120.0, 120.0]