"""Consultas de leitura usadas pela interface."""
import sqlite3
from pathlib import Path

from visaotec.db import CAMINHO_DB


def banco_pronto(caminho: Path = CAMINHO_DB) -> bool:
    """Diz se o banco já existe e tem o catálogo gerado."""
    if not Path(caminho).exists():
        return False
    conn = sqlite3.connect(caminho)
    try:
        return conn.execute("SELECT COUNT(*) FROM produtos").fetchone()[0] > 0
    except sqlite3.OperationalError:
        return False
    finally:
        conn.close()


def armacoes_por_montagem(conn: sqlite3.Connection, tipo_montagem: str) -> list[sqlite3.Row]:
    """Armações do catálogo com um tipo de montagem, da mais barata à mais cara."""
    return conn.execute(
        "SELECT nome, preco FROM produtos "
        "WHERE categoria = 'armacao' AND tipo_montagem = ? ORDER BY preco",
        (tipo_montagem,),
    ).fetchall()


def orcamentos_atualizados(conn: sqlite3.Connection) -> bool:
    """Diz se a tabela orcamentos já tem as colunas atuais de db.py."""
    colunas = {linha[1] for linha in conn.execute("PRAGMA table_info(orcamentos)")}
    return {"armacao", "indice", "tipo", "tratamento", "preco"} <= colunas


def listar_orcamentos(conn: sqlite3.Connection, limite: int = 20) -> list[sqlite3.Row]:
    """Últimos orçamentos salvos, do mais recente para o mais antigo."""
    return conn.execute(
        "SELECT id, criado_em, receita_id, armacao, indice, tipo, tratamento, preco "
        "FROM orcamentos ORDER BY id DESC LIMIT ?",
        (limite,),
    ).fetchall()
