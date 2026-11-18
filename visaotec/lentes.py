"""Módulo 2: recomendação de lente.

Conteúdos da disciplina: funções (índice por faixa), conjuntos (compatibilidade)
e princípio fundamental da contagem (orçamentos).
"""
from itertools import product

INDICES = [1.50, 1.56, 1.61, 1.67]
TIPOS = ["visão simples", "bifocal", "multifocal"]
TRATAMENTOS = ["sem tratamento", "antirreflexo", "filtro de luz azul", "fotossensível"]
TIPOS_ARMACAO = ["aro fechado", "fio de nylon", "parafusada"]

# TODO: preços fictícios de cada opção (por índice, tipo e tratamento)
PRECOS: dict = {}


def escolher_indice(maior_grau: float) -> float:
    """Sugere o índice de refração pela faixa do maior grau (em módulo).

    Função definida por partes: cada faixa de grau leva a um índice.
    """
    # TODO: definir as faixas (pesquisar o que as óticas usam)
    raise NotImplementedError


def lentes_da_armacao(tipo_armacao: str) -> set[str]:
    """Conjunto de lentes/materiais que uma armação aceita.

    Ex.: parafusada (sem aro) só aceita policarbonato ou trivex.
    """
    # TODO
    raise NotImplementedError


def lentes_da_receita(maior_grau: float) -> set[str]:
    """Conjunto de lentes/materiais que a receita permite."""
    # TODO
    raise NotImplementedError


def opcoes_compativeis(tipo_armacao: str, maior_grau: float) -> set[str]:
    """Opções = L_armação ∩ L_receita"""
    # TODO
    raise NotImplementedError


def contar_orcamentos() -> int:
    """Número de orçamentos possíveis pelo princípio fundamental da contagem."""
    # TODO: calcular pela regra do produto (não escrever o número na mão)
    raise NotImplementedError


def tres_mais_baratas(opcoes: set[str], tipos: list[str]) -> list[tuple]:
    """Monta as três combinações mais baratas entre as lentes compatíveis.

    `opcoes` vem de opcoes_compativeis e `tipos` são os tipos de lente que a
    receita permite (o app passa só bifocal e multifocal quando há adição).
    Cada item devolvido é (lente, tipo, tratamento, preço).

    Dica: itertools.product gera todas as combinações.
    """
    # TODO
    raise NotImplementedError
