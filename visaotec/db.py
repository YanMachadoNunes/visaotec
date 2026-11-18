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


def banco_pronto(caminho: Path = CAMINHO_DB) -> bool:
    """Diz se o banco já existe e tem o catálogo gerado."""
    if not caminho.exists():
        return False
    conn = sqlite3.connect(caminho)
    try:
        return conn.execute("SELECT COUNT(*) FROM produtos").fetchone()[0] > 0
    except sqlite3.OperationalError:
        return False
    finally:
        conn.close()


def armacoes_por_montagem(conn, tipo_montagem: str) -> list[sqlite3.Row]:
    """Armações do catálogo com um tipo de montagem, da mais barata à mais cara."""
    return conn.execute(
        "SELECT nome, preco FROM produtos "
        "WHERE categoria = 'armacao' AND tipo_montagem = ? ORDER BY preco",
        (tipo_montagem,),
    ).fetchall()


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
