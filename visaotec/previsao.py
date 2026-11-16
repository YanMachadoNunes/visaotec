"""Previsão de demanda com regressão linear.

Conteúdo da disciplina: machine learning (scikit-learn).
"""
import pandas as pd
from matplotlib.figure import Figure


def treinar(mensal: pd.DataFrame):
    """Treina uma LinearRegression com X = número do mês e y = vendas daquele mês."""
    # TODO
    raise NotImplementedError


def prever(modelo, meses_a_frente: int = 3) -> pd.DataFrame:
    """Previsão para os próximos meses."""
    # TODO
    raise NotImplementedError


def grafico_previsao(mensal: pd.DataFrame, previsao: pd.DataFrame) -> Figure:
    """Curva histórica + curva prevista no mesmo gráfico."""
    # TODO
    raise NotImplementedError
