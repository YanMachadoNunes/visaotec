"""Gera os dados fictícios do VisãoTec e grava em data/visaotec.db.

- catálogo de armações e lentes
- 12 meses de vendas
- receitas de exemplo

Pode rodar de novo: catálogo e vendas são refeitos, e as receitas de exemplo
só entram se a tabela estiver vazia, para não apagar o histórico salvo no app.
"""
import calendar
import random
import sys
from datetime import date, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from visaotec import db
from visaotec.lentes import PRECO_INDICE

SEMENTE = 42  # para os dados saírem iguais toda vez
PRIMEIRO_MES = (2025, 11)
PROPORCAO_SO_LENTE = 0.20  # atendimentos em que o cliente só troca a lente

# (nome, tipo de montagem, preço, peso nas vendas)
ARMACOES = [
    ("Aurora", "aro fechado", 189.90, 9),
    ("Bruma", "aro fechado", 249.90, 8),
    ("Cedro", "aro fechado", 319.90, 6),
    ("Delta", "aro fechado", 429.90, 3),
    ("Estrela", "fio de nylon", 279.90, 5),
    ("Falésia", "fio de nylon", 349.90, 4),
    ("Garoa", "fio de nylon", 459.90, 2),
    ("Horizonte", "parafusada", 399.90, 3),
    ("Íris", "parafusada", 529.90, 2),
]

# (nome, material, índice, preço, peso nas vendas)
# Os índices e preços são os mesmos de visaotec/lentes.py.
LENTES = [
    ("Resina 1.50", "resina", 1.50, PRECO_INDICE[1.50], 10),
    ("Policarbonato 1.59", "policarbonato", 1.59, PRECO_INDICE[1.59], 7),
    ("Alto índice 1.67", "alto índice", 1.67, PRECO_INDICE[1.67], 4),
    ("Altíssimo índice 1.74", "altíssimo índice", 1.74, PRECO_INDICE[1.74], 1),
]

# Dezembro (presentes) e janeiro/fevereiro (volta às aulas) vendem mais.
SAZONALIDADE = {1: 1.10, 2: 1.08, 3: 0.97, 4: 0.94, 5: 1.00, 6: 0.95,
                7: 1.02, 8: 0.96, 9: 0.98, 10: 1.00, 11: 1.03, 12: 1.22}


def gerar_catalogo() -> list[dict]:
    catalogo = []
    for nome, montagem, preco, peso in ARMACOES:
        catalogo.append({"categoria": "armacao", "nome": nome, "preco": preco, "peso": peso,
                         "tipo_montagem": montagem, "material": None, "indice": None})
    for nome, material, indice, preco, peso in LENTES:
        catalogo.append({"categoria": "lente", "nome": nome, "preco": preco, "peso": peso,
                         "tipo_montagem": None, "material": material, "indice": indice})
    for produto_id, produto in enumerate(catalogo, start=1):
        produto["id"] = produto_id
    return catalogo


def gerar_vendas(catalogo: list[dict], meses: int = 12) -> list[tuple]:
    """Cada atendimento vende uma armação e uma lente, ou só a lente.

    O número de atendimentos cresce aos poucos (tendência), muda com a época do
    ano (sazonalidade) e tem um ruído, para a regressão ter o que aprender.
    Parte dos clientes só troca a lente e mantém a armação, por isso as
    categorias têm curvas de venda diferentes.
    """
    armacoes = [p for p in catalogo if p["categoria"] == "armacao"]
    lentes = [p for p in catalogo if p["categoria"] == "lente"]
    ano_inicial, mes_inicial = PRIMEIRO_MES
    sorteio_troca = random.Random(SEMENTE + 1)
    vendas = []
    for i in range(meses):
        ano = ano_inicial + (mes_inicial - 1 + i) // 12
        mes = (mes_inicial - 1 + i) % 12 + 1
        dias_no_mes = calendar.monthrange(ano, mes)[1]
        atendimentos = round((62 + 2.5 * i) * SAZONALIDADE[mes] * random.uniform(0.95, 1.05))
        for _ in range(atendimentos):
            dia = date(ano, mes, random.randint(1, dias_no_mes)).isoformat()
            desconto = random.choice([1.0, 1.0, 1.0, 0.95, 0.90])
            so_troca_lente = sorteio_troca.random() < PROPORCAO_SO_LENTE
            for grupo in (armacoes, lentes):
                produto = random.choices(grupo, weights=[p["peso"] for p in grupo])[0]
                if grupo is armacoes and so_troca_lente:
                    continue
                vendas.append((dia, produto["id"], 1, round(produto["preco"] * desconto, 2)))
    return vendas


def _grau(minimo: float, maximo: float) -> float:
    """Sorteia um grau em passos de 0,25."""
    return random.randint(round(minimo * 4), round(maximo * 4)) / 4


def gerar_receitas(n: int = 50) -> list[tuple]:
    agora = datetime(2026, 11, 1, 9, 0).isoformat(timespec="seconds")
    receitas = []
    for _ in range(n):
        adicao = _grau(0.75, 3.00) if random.random() < 0.3 else 0.0
        linha = [agora]
        for _olho in range(2):
            cilindro = _grau(-2.50, 0.00)
            eixo = random.randint(1, 180) if cilindro else 0
            linha += [_grau(-6.00, 4.00), cilindro, eixo, adicao]
        receitas.append(tuple(linha))
    return receitas


def main():
    random.seed(SEMENTE)
    conn = db.conectar()
    db.criar_tabelas(conn)
    conn.execute("DELETE FROM vendas")
    conn.execute("DELETE FROM produtos")

    catalogo = gerar_catalogo()
    conn.executemany(
        "INSERT INTO produtos (id, categoria, nome, preco, tipo_montagem, material, indice) "
        "VALUES (:id, :categoria, :nome, :preco, :tipo_montagem, :material, :indice)",
        catalogo,
    )
    vendas = gerar_vendas(catalogo)
    conn.executemany(
        "INSERT INTO vendas (data, produto_id, quantidade, valor) VALUES (?, ?, ?, ?)", vendas
    )
    if conn.execute("SELECT COUNT(*) FROM receitas").fetchone()[0] == 0:
        conn.executemany(
            "INSERT INTO receitas (criada_em, od_esf, od_cil, od_eixo, od_add, "
            "oe_esf, oe_cil, oe_eixo, oe_add) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            gerar_receitas(),
        )
    conn.commit()
    conn.close()
    print(f"Banco criado em {db.CAMINHO_DB}: {len(catalogo)} produtos, {len(vendas)} itens vendidos")


if __name__ == "__main__":
    main()
