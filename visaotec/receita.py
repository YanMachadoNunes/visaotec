"""Módulo 1: conferência de receita.

Conteúdo da disciplina: funções.
"""
from dataclasses import dataclass


@dataclass
class Olho:
    esferico: float          # E, em dioptrias
    cilindrico: float = 0.0  # C
    eixo: int = 0            # θ, de 1 a 180
    adicao: float = 0.0      # A (só para perto / multifocal)


def transpor_cilindro(olho: Olho) -> Olho:
    """Reescreve a receita com o sinal do cilindro trocado.

    E' = E + C,  C' = -C,  θ' = θ ± 90°  (θ' sempre entre 1 e 180)
    """
    # TODO: implementar. Cuidado com o caso do eixo: quando somar e quando subtrair 90?
    raise NotImplementedError


def para_cilindro_negativo(olho: Olho) -> Olho:
    """Garante que a receita está em cilindro negativo (formato que o laboratório pede)."""
    # TODO: usar transpor_cilindro só quando precisar
    raise NotImplementedError


def grau_perto(olho: Olho) -> float:
    """E_perto = E_longe + A"""
    # TODO
    raise NotImplementedError


def equivalente_esferico(olho: Olho) -> float:
    """EE = E + C/2"""
    # TODO
    raise NotImplementedError


def validar(olho: Olho) -> list[str]:
    """Devolve a lista de alertas da receita (vazia se estiver tudo ok).

    Ideias de regras: graus em passos de 0,25; eixo entre 1 e 180;
    eixo informado sem cilindro; adição fora de 0,75 a 3,50; graus muito altos.
    """
    # TODO: definir as regras e as faixas
    raise NotImplementedError
