"""Previsão de demanda com regressão linear.

Conteúdo da disciplina: machine learning (scikit-learn).
"""
import pandas as pd


def treinar(mensal: pd.DataFrame):
    """Treina uma LinearRegression com X = número do mês e y = vendas daquele mês.

    `mensal` vem de vendas.faturamento_mensal. O primeiro mês é o número 1,
    e y é a coluna itens.
    """
    # TODO
    raise NotImplementedError


def prever(modelo, meses_historico: int, meses_a_frente: int = 3) -> pd.DataFrame:
    """Previsão para os meses seguintes ao histórico.

    Com 12 meses de histórico e 3 à frente, prevê os meses 13, 14 e 15.
    Devolve as colunas: n (número do mês), itens (valor previsto).
    """
    # TODO
    raise NotImplementedError
