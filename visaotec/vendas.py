
import sqlite3

import pandas as pd

CONSULTA_VENDAS = """
    SELECT v.data, v.produto_id, v.quantidade, v.valor,
           p.nome, p.categoria
    FROM vendas v
    JOIN produtos p ON p.id = v.produto_id
"""


def carregar_vendas(conn: sqlite3.Connection) -> pd.DataFrame:
    """Lê as vendas do banco já com o nome e a categoria de cada produto.

    Colunas: data, produto_id, quantidade, valor, nome, categoria.
    """
    df = pd.read_sql_query(CONSULTA_VENDAS, conn)
    df["data"] = pd.to_datetime(df["data"])
    return df


def _filtrar_categoria(df: pd.DataFrame, categoria: str | None) -> pd.DataFrame:
    """Mantém só 'armacao' ou 'lente'; None devolve tudo."""
    if categoria is None:
        return df
    return df[df["categoria"] == categoria]


def ranking_produtos(df: pd.DataFrame, categoria: str | None = None,
                     top: int | None = None) -> pd.DataFrame:
    """Produtos mais vendidos, do maior para o menor.

    Devolve as colunas: nome, categoria, quantidade, faturamento.
    Empate em quantidade é desempatado pelo faturamento.
    """
    ranking = (
        _filtrar_categoria(df, categoria)
        .groupby(["nome", "categoria"], as_index=False)
        .agg(quantidade=("quantidade", "sum"), faturamento=("valor", "sum"))
        .sort_values(["quantidade", "faturamento"], ascending=False)
        .reset_index(drop=True)
    )
    ranking["faturamento"] = ranking["faturamento"].round(2)
    return ranking.head(top) if top else ranking


def faturamento_mensal(df: pd.DataFrame, categoria: str | None = None) -> pd.DataFrame:
    """Faturamento e itens vendidos por mês, em ordem cronológica.

    Devolve as colunas: mes (texto 'AAAA-MM'), faturamento, itens.
    Essa tabela também é a entrada do modelo de previsão.
    """
    dados = _filtrar_categoria(df, categoria).copy()
    dados["mes"] = dados["data"].dt.strftime("%Y-%m")
    mensal = (
        dados.groupby("mes", as_index=False)
        .agg(faturamento=("valor", "sum"), itens=("quantidade", "sum"))
        .sort_values("mes")
        .reset_index(drop=True)
    )
    mensal["faturamento"] = mensal["faturamento"].round(2)
    return mensal