"""
visaotec/receita.py
Cálculos e validação de receitas de óculos.

Conteúdo da disciplina aplicado aqui: FUNÇÕES.
Cada função recebe um olho (ou valores numéricos) e devolve um resultado,
sem alterar o objeto original.
"""

from dataclasses import dataclass, replace

# ---------------------------------------------------------------------------
# Faixas aceitas (valores típicos de receitas; usados na validação)
# ---------------------------------------------------------------------------
PASSO = 0.25                    # graus sempre variam de 0,25 em 0,25
ESFERICO_MIN, ESFERICO_MAX = -20.0, 20.0
CILINDRO_MIN, CILINDRO_MAX = -6.0, 6.0
EIXO_MIN, EIXO_MAX = 1, 180
ADICAO_MIN, ADICAO_MAX = 0.75, 3.50
LIMITE_ANISOMETROPIA = 2.0      # diferença entre olhos que merece alerta


@dataclass(frozen=True)
class Olho:
    """Representa a receita de um olho.

    esferico: grau esférico (miopia -, hipermetropia +)
    cilindro: grau cilíndrico (astigmatismo); 0 = sem astigmatismo
    eixo:     ângulo do cilindro em graus (1 a 180); 0 quando não há cilindro
    adicao:   adição para perto (presbiopia); 0 quando não há
    """
    esferico: float
    cilindro: float = 0.0
    eixo: int = 0
    adicao: float = 0.0


# ---------------------------------------------------------------------------
# Funções de cálculo
# ---------------------------------------------------------------------------
def _girar_eixo(eixo: int) -> int:
    """Gira o eixo em 90°, mantendo o resultado entre 1 e 180."""
    return eixo + 90 if eixo <= 90 else eixo - 90


def transpor_cilindro(olho: Olho) -> Olho:
    """Escreve a mesma receita na notação de cilindro oposta.

    Regra:  E' = E + C   |   C' = -C   |   eixo' = eixo ± 90°
    Se o cilindro for 0, não há o que transpor: devolve o olho sem alterar.
    """
    if olho.cilindro == 0:
        return olho
    return replace(
        olho,
        esferico=round(olho.esferico + olho.cilindro, 2),
        cilindro=round(-olho.cilindro, 2),
        eixo=_girar_eixo(olho.eixo),
    )


def para_cilindro_negativo(olho: Olho) -> Olho:
    """Padroniza a receita em cilindro negativo (notação dos laboratórios)."""
    if olho.cilindro > 0:
        return transpor_cilindro(olho)
    return olho


def grau_perto(olho: Olho) -> Olho:
    """Calcula a receita de perto: E_perto = E_longe + adição.

    Só o esférico muda; cilindro e eixo continuam iguais.
    A adição deixa de existir na receita de perto.
    """
    return replace(olho, esferico=round(olho.esferico + olho.adicao, 2), adicao=0.0)


def equivalente_esferico(olho: Olho) -> float:
    """Equivalente esférico: EE = E + C/2 (usado para escolher o índice)."""
    return round(olho.esferico + olho.cilindro / 2, 3)


# ---------------------------------------------------------------------------
# Validação
# ---------------------------------------------------------------------------
def _multiplo_do_passo(valor: float) -> bool:
    """Confere se o valor anda em passos de 0,25."""
    return abs(valor / PASSO - round(valor / PASSO)) < 1e-9


def _validar_olho(olho: Olho, nome: str) -> list[str]:
    """Devolve a lista de erros encontrados em um olho."""
    erros = []

    if not ESFERICO_MIN <= olho.esferico <= ESFERICO_MAX:
        erros.append(f"{nome}: esférico fora da faixa ({ESFERICO_MIN} a {ESFERICO_MAX}).")
    if not _multiplo_do_passo(olho.esferico):
        erros.append(f"{nome}: esférico deve variar de 0,25 em 0,25.")

    if not CILINDRO_MIN <= olho.cilindro <= CILINDRO_MAX:
        erros.append(f"{nome}: cilindro fora da faixa ({CILINDRO_MIN} a {CILINDRO_MAX}).")
    if not _multiplo_do_passo(olho.cilindro):
        erros.append(f"{nome}: cilindro deve variar de 0,25 em 0,25.")

    # O eixo só é obrigatório quando existe cilindro
    if olho.cilindro != 0 and not EIXO_MIN <= olho.eixo <= EIXO_MAX:
        erros.append(f"{nome}: eixo deve estar entre {EIXO_MIN}° e {EIXO_MAX}°.")

    if olho.adicao != 0:
        if not ADICAO_MIN <= olho.adicao <= ADICAO_MAX:
            erros.append(f"{nome}: adição fora da faixa ({ADICAO_MIN} a {ADICAO_MAX}).")
        if not _multiplo_do_passo(olho.adicao):
            erros.append(f"{nome}: adição deve variar de 0,25 em 0,25.")

    return erros


def validar(od: Olho, oe: Olho) -> dict[str, list[str]]:
    """Valida a receita completa (olho direito e olho esquerdo).

    Devolve {"erros": [...], "alertas": [...]}.
    Erros impedem o pedido; alertas só pedem atenção do atendente.
    """
    erros = _validar_olho(od, "OD") + _validar_olho(oe, "OE")
    alertas = []

    diferenca = abs(equivalente_esferico(od) - equivalente_esferico(oe))
    if diferenca > LIMITE_ANISOMETROPIA:
        alertas.append(
            f"Diferença de {diferenca:.2f} entre os olhos: confira a receita com o cliente."
        )

    if od.adicao != oe.adicao:
        alertas.append("Adição diferente entre os olhos: confira a receita.")

    return {"erros": erros, "alertas": alertas}