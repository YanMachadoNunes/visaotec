


import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score


def _eixo_x(n: int, inicio: int = 0) -> np.ndarray:
    """Números dos meses no formato que o scikit-learn espera (uma coluna)."""
    return np.arange(inicio, inicio + n).reshape(-1, 1)


def treinar(mensal: pd.DataFrame, coluna: str = "faturamento") -> dict:
    """Ajusta a reta aos dados mensais (saída de vendas.faturamento_mensal).

    Devolve um dicionário com o modelo e o que mostrar na interface:
    a (crescimento por mês), b (valor no mês 0), R² e erro médio (MAE).
    """
    if len(mensal) < 3:
        raise ValueError("São necessários pelo menos 3 meses para treinar.")

    x = _eixo_x(len(mensal))
    y = mensal[coluna].to_numpy()
    modelo = LinearRegression().fit(x, y)
    ajustado = modelo.predict(x)

    return {
        "modelo": modelo,
        "coluna": coluna,
        "n_meses": len(mensal),
        "ultimo_mes": mensal["mes"].iloc[-1],
        "a": float(modelo.coef_[0]),
        "b": float(modelo.intercept_),
        "r2": float(r2_score(y, ajustado)),
        "mae": float(mean_absolute_error(y, ajustado)),
    }


def prever(treino: dict, meses: int = 3) -> pd.DataFrame:
    """Continua a reta pelos próximos meses.

    Devolve as colunas: mes ('AAAA-MM') e previsto.
    """
    x_futuro = _eixo_x(meses, inicio=treino["n_meses"])
    previsto = treino["modelo"].predict(x_futuro)
    ultimo = pd.Period(treino["ultimo_mes"], freq="M")
    nomes = [str(ultimo + i) for i in range(1, meses + 1)]
    return pd.DataFrame({"mes": nomes, "previsto": np.round(previsto, 2)})


def avaliar(mensal: pd.DataFrame, coluna: str = "faturamento",
            meses_teste: int = 3) -> dict:
    """Teste honesto: treina sem os últimos meses e compara a previsão com o real.

    Mostra se o modelo acerta meses que ele não viu no treino.
    """
    treino = treinar(mensal.iloc[:-meses_teste], coluna)
    real = mensal[coluna].iloc[-meses_teste:].to_numpy()
    previsto = prever(treino, meses_teste)["previsto"].to_numpy()
    mae = float(mean_absolute_error(real, previsto))
    return {
        "mae": mae,
        "erro_percentual": round(float(100 * mae / real.mean()), 1),
        "real": real.tolist(),
        "previsto": previsto.tolist(),
    }