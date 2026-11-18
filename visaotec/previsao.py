"""Previsão de demanda com regressão linear.

Conteúdo da disciplina: machine learning (scikit-learn).
"""
import pandas as pd
from matplotlib.figure import Figure

from visaotec.estilo import AZUL, GRADE, LARANJA, TEXTO, nova_figura, rotulo_mes


def treinar(mensal: pd.DataFrame):
    """Treina uma LinearRegression com X = número do mês e y = vendas daquele mês.

    `mensal` vem de vendas.faturamento_mensal. O primeiro mês é o número 1,
    e y é a coluna quantidade.
    """
    # TODO
    raise NotImplementedError


def prever(modelo, meses_historico: int, meses_a_frente: int = 3) -> pd.DataFrame:
    """Previsão para os meses seguintes ao histórico.

    Com 12 meses de histórico e 3 à frente, prevê os meses 13, 14 e 15.
    Devolve as colunas: n (número do mês), quantidade (valor previsto).
    """
    # TODO
    raise NotImplementedError


def grafico_previsao(mensal: pd.DataFrame, previsao: pd.DataFrame) -> Figure:
    """Curva histórica + curva prevista no mesmo gráfico."""
    figura, eixos = nova_figura()
    total = len(mensal)
    x_real = list(range(1, total + 1))
    y_real = mensal["quantidade"].tolist()
    x_prev = previsao["n"].tolist()
    y_prev = previsao["quantidade"].tolist()

    eixos.plot(x_real, y_real, color=AZUL, linewidth=2, marker="o", markersize=5,
               label="Vendido")
    # A previsão sai do último mês real, para as duas curvas ficarem ligadas.
    eixos.plot([total] + x_prev, [y_real[-1]] + y_prev, color=LARANJA, linewidth=2,
               linestyle=(0, (4, 2)), marker="o", markersize=5, markevery=list(range(1, len(x_prev) + 1)),
               label="Previsão")
    eixos.annotate(f"{y_prev[-1]:.0f}", (x_prev[-1], y_prev[-1]), xytext=(0, 8),
                   textcoords="offset points", ha="center", fontsize=9, color=TEXTO)

    ultimo_mes = pd.Period(mensal["mes"].iloc[-1], "M")
    rotulos = [rotulo_mes(m) for m in mensal["mes"]]
    rotulos += [rotulo_mes(ultimo_mes + (n - total)) for n in x_prev]
    eixos.set_xticks(x_real + x_prev, rotulos)
    eixos.set_ylim(bottom=0, top=max(y_real + y_prev) * 1.15)
    eixos.set_ylabel("Itens vendidos", fontsize=9, color=TEXTO)
    eixos.grid(axis="y", color=GRADE, linewidth=1)
    eixos.legend(loc="lower left", frameon=False, fontsize=9, ncols=2)
    return figura
