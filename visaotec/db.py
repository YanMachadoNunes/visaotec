"""Acesso ao banco SQLite.

Conteúdo da disciplina: banco de dados.
"""
import sqlite3
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
CAMINHO_DB = RAIZ / "data" / "visaotec.db"
SCHEMA = RAIZ / "schema.sql"


def conectar(caminho: Path = CAMINHO_DB) -> sqlite3.Connection:
    caminho.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(caminho)
    conn.row_factory = sqlite3.Row
    return conn


def criar_tabelas(conn: sqlite3.Connection) -> None:
    conn.executescript(SCHEMA.read_text(encoding="utf-8"))


def salvar_receita(conn, od, oe) -> int:
    """Insere uma receita no histórico e devolve o id."""
    # TODO: INSERT INTO receitas (...) VALUES (?, ...)
    raise NotImplementedError


def listar_receitas(conn) -> list:
    # TODO
    raise NotImplementedError


def salvar_orcamento(conn, receita_id: int, descricao: str, total: float) -> int:
    # TODO
    raise NotImplementedError
