"""
visaotec/db.py
Banco de dados SQLite do VisãoTec: conexão, tabelas e histórico.

Conteúdo da disciplina aplicado aqui: BANCO DE DADOS.

Tabelas:
- produtos:    catálogo de armações e lentes (gerado por scripts/gerar_dados.py)
- vendas:      itens vendidos nos últimos 12 meses (gerado pelo mesmo script)
- receitas:    receitas conferidas no app (histórico)
- orcamentos:  orçamentos escolhidos para cada receita (histórico)
"""

import sqlite3
from datetime import datetime
from pathlib import Path

from visaotec.receita import Olho

CAMINHO_DB = Path(__file__).resolve().parent.parent / "data" / "visaotec.db"

TABELAS = """
CREATE TABLE IF NOT EXISTS produtos (
    id            INTEGER PRIMARY KEY,
    categoria     TEXT NOT NULL,          -- 'armacao' ou 'lente'
    nome          TEXT NOT NULL,
    preco         REAL NOT NULL,
    tipo_montagem TEXT,                   -- só armações
    material      TEXT,                   -- só lentes
    indice        REAL                    -- só lentes
);

CREATE TABLE IF NOT EXISTS vendas (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    data       TEXT NOT NULL,             -- 'AAAA-MM-DD'
    produto_id INTEGER NOT NULL REFERENCES produtos(id),
    quantidade INTEGER NOT NULL,
    valor      REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS receitas (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    criada_em TEXT NOT NULL,              -- 'AAAA-MM-DDTHH:MM:SS'
    od_esf REAL NOT NULL, od_cil REAL NOT NULL, od_eixo INTEGER NOT NULL, od_add REAL NOT NULL,
    oe_esf REAL NOT NULL, oe_cil REAL NOT NULL, oe_eixo INTEGER NOT NULL, oe_add REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS orcamentos (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    criado_em  TEXT NOT NULL,
    receita_id INTEGER REFERENCES receitas(id),
    armacao    TEXT NOT NULL,             -- tipo de montagem
    indice     REAL NOT NULL,
    tipo       TEXT NOT NULL,             -- visão simples, bifocal, multifocal
    tratamento TEXT NOT NULL,
    preco      REAL NOT NULL
);
"""


# ---------------------------------------------------------------------------
# Conexão e tabelas
# ---------------------------------------------------------------------------
def conectar(caminho: Path | str = CAMINHO_DB) -> sqlite3.Connection:
    """Abre o banco (cria a pasta data/ se faltar). ':memory:' serve para testes."""
    if caminho != ":memory:":
        Path(caminho).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(caminho)
    conn.row_factory = sqlite3.Row        # linhas acessíveis por nome da coluna
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def criar_tabelas(conn: sqlite3.Connection) -> None:
    """Cria as tabelas que ainda não existem (não apaga nada)."""
    conn.executescript(TABELAS)


def _agora() -> str:
    return datetime.now().isoformat(timespec="seconds")


# ---------------------------------------------------------------------------
# Histórico de receitas
# ---------------------------------------------------------------------------
def salvar_receita(conn: sqlite3.Connection, od: Olho, oe: Olho) -> int:
    """Grava a receita (OD e OE) e devolve o id criado."""
    cursor = conn.execute(
        "INSERT INTO receitas (criada_em, od_esf, od_cil, od_eixo, od_add, "
        "oe_esf, oe_cil, oe_eixo, oe_add) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (_agora(),
         od.esferico, od.cilindro, od.eixo, od.adicao,
         oe.esferico, oe.cilindro, oe.eixo, oe.adicao),
    )
    conn.commit()
    return cursor.lastrowid


def listar_receitas(conn: sqlite3.Connection, limite: int = 20) -> list[dict]:
    """Últimas receitas salvas, da mais recente para a mais antiga.

    Cada item: {"id", "criada_em", "od": Olho, "oe": Olho}.
    Devolver Olho permite reaproveitar direto as funções de receita.py e lentes.py.
    """
    linhas = conn.execute(
        "SELECT * FROM receitas ORDER BY id DESC LIMIT ?", (limite,)
    ).fetchall()
    return [
        {
            "id": linha["id"],
            "criada_em": linha["criada_em"],
            "od": Olho(linha["od_esf"], linha["od_cil"], linha["od_eixo"], linha["od_add"]),
            "oe": Olho(linha["oe_esf"], linha["oe_cil"], linha["oe_eixo"], linha["oe_add"]),
        }
        for linha in linhas
    ]


# ---------------------------------------------------------------------------
# Histórico de orçamentos
# ---------------------------------------------------------------------------
def salvar_orcamento(conn: sqlite3.Connection, armacao: str, orcamento: dict,
                     receita_id: int | None = None) -> int:
    """Grava o orçamento escolhido e devolve o id criado.

    `orcamento` é um item de lentes.tres_mais_baratas ou lentes.gerar_orcamentos:
    {"indice", "tipo", "tratamento", "preco"}.
    `receita_id` liga o orçamento à receita salva (opcional).
    """
    cursor = conn.execute(
        "INSERT INTO orcamentos (criado_em, receita_id, armacao, indice, tipo, tratamento, preco) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        (_agora(), receita_id, armacao, orcamento["indice"], orcamento["tipo"],
         orcamento["tratamento"], orcamento["preco"]),
    )
    conn.commit()
    return cursor.lastrowid