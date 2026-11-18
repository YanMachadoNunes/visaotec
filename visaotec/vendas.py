"""Módulo 3: painel de vendas.

Conteúdos da disciplina: DataFrames com Pandas e gráficos com matplotlib.
"""
import pandas as pd
from matplotlib.figure import Figure
from matplotlib.ticker import FuncFormatter

from visaotec.estilo import AZUL, GRADE, TEXTO, nova_figura, rotulo_mes


def carregar_vendas(conn) -> pd.DataFrame:
    """Lê a tabela de vendas (com dados do produto) do SQLite para um DataFrame.

    Colunas: data (datetime), quantidade, valor, categoria, nome.
    """
    consulta = """
        SELECT v.data, v.quantidade, v.valor, p.categoria, p.nome
        FROM vendas AS v
        JOIN produtos AS p ON p.id = v.produto_id
        ORDER BY v.data
    """
    return pd.read_sql_query(consulta, conn, parse_dates=["data"])


def ranking_produtos(df: pd.DataFrame, categoria: str, n: int = 10) -> pd.DataFrame:
    """Os n produtos mais vendidos de uma categoria ('armacao' ou 'lente').

    Devolve as colunas: nome, quantidade (do maior para o menor).
    """
    # TODO
    raise NotImplementedError


def faturamento_mensal(df: pd.DataFrame) -> pd.DataFrame:
    """Soma do valor e da quantidade vendidos por mês.

    Devolve as colunas: mes (texto 'AAAA-MM'), faturamento, quantidade,
    em ordem cronológica.
    """
    # TODO
    raise NotImplementedError


def grafico_faturamento(mensal: pd.DataFrame) -> Figure:
    """Gráfico de faturamento por mês."""
    figura, eixos = nova_figura()
    posicoes = range(len(mensal))
    eixos.plot(posicoes, mensal["faturamento"], color=AZUL, linewidth=2, marker="o", markersize=5)
    eixos.set_xticks(list(posicoes), [rotulo_mes(m) for m in mensal["mes"]])
    eixos.set_ylim(bottom=0)
    eixos.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"R$ {v / 1000:.0f} mil"))
    eixos.grid(axis="y", color=GRADE, linewidth=1)
    return figura


def grafico_ranking(ranking: pd.DataFrame) -> Figure:
    """Gráfico de barras dos mais vendidos, com o primeiro colocado no topo."""
    figura, eixos = nova_figura(altura=max(2.0, 0.36 * len(ranking) + 0.6))
    barras = eixos.barh(ranking["nome"], ranking["quantidade"], color=AZUL, height=0.62)
    eixos.bar_label(barras, padding=4, fontsize=9, color=TEXTO)
    eixos.invert_yaxis()
    eixos.spines["bottom"].set_visible(False)
    eixos.set_xticks([])
    eixos.margins(x=0.08)
    return figura
