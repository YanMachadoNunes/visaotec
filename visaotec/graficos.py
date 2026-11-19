"""Gráficos do painel de vendas (matplotlib).

Ficam separados dos cálculos: `vendas.py` e `previsao.py` produzem as tabelas,
e este módulo só as desenha.
"""
import pandas as pd
from matplotlib.figure import Figure
from matplotlib.ticker import FuncFormatter

from visaotec.estilo import AZUL, GRADE, LARANJA, TEXTO, nova_figura, rotulo_mes


def grafico_ranking(ranking: pd.DataFrame) -> Figure:
    """Barras dos mais vendidos, com o primeiro colocado no topo."""
    figura, eixos = nova_figura(altura=max(2.0, 0.36 * len(ranking) + 0.6))
    barras = eixos.barh(ranking["nome"], ranking["quantidade"], color=AZUL, height=0.62)
    eixos.bar_label(barras, padding=4, fontsize=9, color=TEXTO)
    eixos.invert_yaxis()
    eixos.spines["bottom"].set_visible(False)
    eixos.set_xticks([])
    eixos.margins(x=0.08)
    return figura


def grafico_faturamento(mensal: pd.DataFrame) -> Figure:
    """Linha do faturamento por mês."""
    figura, eixos = nova_figura()
    posicoes = range(len(mensal))
    eixos.plot(posicoes, mensal["faturamento"], color=AZUL, linewidth=2, marker="o", markersize=5)
    eixos.set_xticks(list(posicoes), [rotulo_mes(m) for m in mensal["mes"]])
    eixos.set_ylim(bottom=0, top=mensal["faturamento"].max() * 1.1)
    eixos.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"R$ {v / 1000:.0f} mil"))
    eixos.grid(axis="y", color=GRADE, linewidth=1)
    return figura


def grafico_previsao(mensal: pd.DataFrame, previsao: pd.DataFrame,
                     coluna: str = "faturamento") -> Figure:
    """Curva histórica + curva prevista, para 'faturamento' ou 'itens'."""
    em_reais = coluna == "faturamento"
    figura, eixos = nova_figura(largura=10)  # mais larga: são 15 meses no eixo
    total = len(mensal)
    x_real = list(range(1, total + 1))
    y_real = mensal[coluna].tolist()
    x_prev = list(range(total + 1, total + len(previsao) + 1))
    y_prev = previsao["previsto"].tolist()

    eixos.plot(x_real, y_real, color=AZUL, linewidth=2, marker="o", markersize=5,
               label="Vendido")
    # A previsão sai do último mês real, para as duas curvas ficarem ligadas.
    eixos.plot([total] + x_prev, [y_real[-1]] + y_prev, color=LARANJA, linewidth=2,
               linestyle=(0, (4, 2)), marker="o", markersize=5,
               markevery=list(range(1, len(x_prev) + 1)), label="Previsão")
    rotulo_final = f"R$ {y_prev[-1] / 1000:.1f} mil".replace(".", ",") if em_reais else f"{y_prev[-1]:.0f}"
    eixos.annotate(rotulo_final, (x_prev[-1], y_prev[-1]), xytext=(0, 8),
                   textcoords="offset points", ha="center", fontsize=9, color=TEXTO)

    rotulos = [rotulo_mes(m) for m in list(mensal["mes"]) + list(previsao["mes"])]
    eixos.set_xticks(x_real + x_prev, rotulos)
    eixos.set_ylim(bottom=0, top=max(y_real + y_prev) * 1.15)
    if em_reais:
        eixos.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"R$ {v / 1000:.0f} mil"))
    else:
        eixos.set_ylabel("Itens vendidos", fontsize=9, color=TEXTO)
    eixos.grid(axis="y", color=GRADE, linewidth=1)
    eixos.legend(loc="lower left", frameon=False, fontsize=9, ncols=2)
    return figura
