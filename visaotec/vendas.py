"""Módulo 3: painel de vendas.

Conteúdos da disciplina: DataFrames com Pandas e gráficos com matplotlib.
"""
import pandas as pd
from matplotlib.figure import Figure


def carregar_vendas(conn) -> pd.DataFrame:
    """Lê a tabela de vendas (com dados do produto) do SQLite para um DataFrame."""
    # TODO: pd.read_sql com JOIN em produtos
    raise NotImplementedError


def ranking_produtos(df: pd.DataFrame, categoria: str, n: int = 10) -> pd.DataFrame:
    """Os n produtos mais vendidos de uma categoria ('armacao' ou 'lente')."""
    # TODO
    raise NotImplementedError


def faturamento_mensal(df: pd.DataFrame) -> pd.DataFrame:
    """Soma do valor vendido por mês."""
    # TODO
    raise NotImplementedError


def grafico_faturamento(mensal: pd.DataFrame) -> Figure:
    """Gráfico de faturamento por mês."""
    # TODO
    raise NotImplementedError


def grafico_ranking(ranking: pd.DataFrame) -> Figure:
    """Gráfico de barras dos mais vendidos."""
    # TODO
    raise NotImplementedError
