"""Aparência comum dos gráficos do painel."""
import matplotlib
import pandas as pd
from matplotlib.axes import Axes
from matplotlib.figure import Figure

SUPERFICIE = "#fcfcfb"
TEXTO = "#0b0b0b"
TEXTO_SECUNDARIO = "#52514e"
GRADE = "#e6e5e0"
AZUL = "#2a78d6"     # dados reais
LARANJA = "#eb6834"  # previsão

# Fonte parecida com a do Streamlit (Source Sans); usa a primeira que existir na máquina.
matplotlib.rcParams["font.family"] = "sans-serif"
matplotlib.rcParams["font.sans-serif"] = [
    "Source Sans 3", "Source Sans Pro", "Noto Sans", "Segoe UI", "Arial", "DejaVu Sans",
]

MESES = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]


def rotulo_mes(mes) -> str:
    """Transforma '2025-11' (ou um Period) em 'nov/25'."""
    periodo = pd.Period(mes, "M")
    return f"{MESES[periodo.month - 1]}/{periodo.year % 100:02d}"


def nova_figura(largura: float = 8, altura: float = 3.6) -> tuple[Figure, Axes]:
    """Cria a figura sem pyplot, para não acumular figuras abertas no Streamlit."""
    figura = Figure(figsize=(largura, altura), layout="constrained", facecolor=SUPERFICIE)
    eixos = figura.subplots()
    eixos.set_facecolor(SUPERFICIE)
    eixos.set_axisbelow(True)
    eixos.tick_params(colors=TEXTO_SECUNDARIO, labelsize=9, length=0)
    for lado in ("top", "right", "left"):
        eixos.spines[lado].set_visible(False)
    eixos.spines["bottom"].set_color(GRADE)
    return figura, eixos
