
"""
visaotec/lentes.py
Catálogo fictício de lentes, recomendação de índice e montagem de orçamentos.
 
Conteúdos da disciplina aplicados aqui:
- NOÇÃO DE CONJUNTOS: lentes aceitas pela armação ∩ lentes possíveis para a receita
- PRINCÍPIO FUNDAMENTAL DA CONTAGEM: nº de orçamentos = índices × tipos × tratamentos
- FUNÇÕES: escolha do índice por faixa de grau e cálculo de preço
"""
 
from itertools import product
 
from visaotec.receita import Olho
 
# ---------------------------------------------------------------------------
# Catálogo fictício (preços em R$, par de lentes)
# Preço final = preço do índice + adicional do tipo + adicional do tratamento
# ---------------------------------------------------------------------------
PRECO_INDICE = {
    1.50: 120.0,   # resina comum (CR-39)
    1.59: 220.0,   # policarbonato
    1.67: 380.0,   # alto índice
    1.74: 650.0,   # altíssimo índice
}
 
ADICIONAL_TIPO = {
    "visão simples": 0.0,
    "bifocal": 150.0,
    "multifocal": 450.0,
}
 
ADICIONAL_TRATAMENTO = {
    "sem tratamento": 0.0,
    "antirreflexo": 120.0,
    "filtro de luz azul": 180.0,
    "fotossensível": 300.0,
}
 
INDICES = set(PRECO_INDICE)
TIPOS = set(ADICIONAL_TIPO)
TRATAMENTOS = set(ADICIONAL_TRATAMENTO)
 
# Quais índices cada tipo de armação aceita
LENTES_POR_ARMACAO = {
    "aro fechado": {1.50, 1.59, 1.67, 1.74},   # aceita qualquer lente
    "fio de nylon": {1.50, 1.59, 1.67, 1.74},  # meio aro: lente com canaleta
    # Sem aro: o furo do parafuso trinca lentes frágeis, então só policarbonato.
    # (A proposta cita também trivex, mas trivex não está no catálogo fictício.)
    "parafusada": {1.59},
}
 
# Faixas de grau para escolher o índice (valor absoluto do maior grau, em dioptrias).
# Simplificação das faixas usuais do mercado: quanto maior o grau, maior o índice,
# para a lente ficar mais fina.
FAIXAS_INDICE = [
    (2.00, 1.50),
    (4.00, 1.59),
    (6.00, 1.67),
    (float("inf"), 1.74),
]
 
 
# ---------------------------------------------------------------------------
# Recomendação de índice
# ---------------------------------------------------------------------------
def maior_grau(od: Olho, oe: Olho) -> float:
    """Maior grau absoluto entre os meridianos dos dois olhos.
 
    Cada olho tem dois meridianos: o esférico (E) e o esférico + cilindro (E + C).
    A espessura da lente depende do meridiano mais forte.
    """
    meridianos = [od.esferico, od.esferico + od.cilindro,
                  oe.esferico, oe.esferico + oe.cilindro]
    return max(abs(m) for m in meridianos)
 
 
def escolher_indice(od: Olho, oe: Olho) -> float:
    """Recomenda o índice de refração pela faixa do maior grau."""
    grau = maior_grau(od, oe)
    for limite, indice in FAIXAS_INDICE:
        if grau <= limite:
            return indice
    return 1.74  # nunca chega aqui por causa do inf, mas deixa explícito
 
 
# ---------------------------------------------------------------------------
# Conjuntos de lentes compatíveis
# ---------------------------------------------------------------------------
def lentes_da_armacao(armacao: str) -> set[float]:
    """Conjunto de índices que a armação aceita."""
    if armacao not in LENTES_POR_ARMACAO:
        raise ValueError(f"Armação desconhecida: {armacao}")
    return set(LENTES_POR_ARMACAO[armacao])
 
 
def lentes_da_receita(od: Olho, oe: Olho) -> set[float]:
    """Conjunto de índices adequados à receita.
 
    Vale o índice recomendado e todos os maiores que ele
    (um índice maior também serve, só fica mais fino e mais caro).
    """
    minimo = escolher_indice(od, oe)
    return {indice for indice in INDICES if indice >= minimo}
 
 
def opcoes_compativeis(od: Olho, oe: Olho, armacao: str) -> set[float]:
    """Índices válidos para o cliente: interseção dos dois conjuntos."""
    return lentes_da_armacao(armacao) & lentes_da_receita(od, oe)
 
 
def tipos_da_receita(od: Olho, oe: Olho) -> set[str]:
    """Tipos de lente que atendem a receita.
 
    Sem adição: só visão simples.
    Com adição: bifocal ou multifocal, que corrigem longe e perto na mesma lente.
    (Visão simples para quem tem adição corrigiria só a distância, então fica de fora.)
    """
    if od.adicao == 0 and oe.adicao == 0:
        return {"visão simples"}
    return {"bifocal", "multifocal"}
 
 
# ---------------------------------------------------------------------------
# Orçamentos (princípio fundamental da contagem)
# ---------------------------------------------------------------------------
def contar_orcamentos(indices=INDICES, tipos=TIPOS, tratamentos=TRATAMENTOS) -> int:
    """Regra do produto: cada escolha é independente, então multiplica.
 
    Com o catálogo completo: 4 índices × 3 tipos × 4 tratamentos = 48.
    """
    return len(indices) * len(tipos) * len(tratamentos)
 
 
def preco(indice: float, tipo: str, tratamento: str) -> float:
    """Preço do par de lentes para uma combinação."""
    return PRECO_INDICE[indice] + ADICIONAL_TIPO[tipo] + ADICIONAL_TRATAMENTO[tratamento]
 
 
def gerar_orcamentos(indices=INDICES, tipos=TIPOS, tratamentos=TRATAMENTOS) -> list[dict]:
    """Lista todas as combinações (produto cartesiano) com o preço de cada uma."""
    return [
        {"indice": i, "tipo": t, "tratamento": tr, "preco": preco(i, t, tr)}
        for i, t, tr in product(sorted(indices), sorted(tipos), sorted(tratamentos))
    ]
 
 
def tres_mais_baratas(od: Olho, oe: Olho, armacao: str) -> list[dict]:
    """As 3 opções mais baratas que servem para a receita e a armação.
 
    Lista vazia = nenhuma lente do catálogo serve nessa armação
    (ex.: grau alto numa parafusada); a tela deve sugerir outra armação.
    """
    orcamentos = gerar_orcamentos(
        indices=opcoes_compativeis(od, oe, armacao),
        tipos=tipos_da_receita(od, oe),
    )
    return sorted(orcamentos, key=lambda o: o["preco"])[:3]
 