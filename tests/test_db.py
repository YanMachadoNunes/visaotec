
"""tests/test_db.py — rode com: pytest"""
 
import sqlite3
 
import pytest
 
from visaotec import db
from visaotec.receita import Olho
from visaotec.lentes import tres_mais_baratas
 
 
@pytest.fixture
def conn():
    """Banco vazio em memória: não mexe no data/visaotec.db de verdade."""
    c = db.conectar(":memory:")
    db.criar_tabelas(c)
    yield c
    c.close()
 
 
def test_salvar_e_listar_receita(conn):
    od, oe = Olho(-2.0, -0.75, 170, 1.5), Olho(-1.75, 0.0, 0, 1.5)
    rid = db.salvar_receita(conn, od, oe)
    receitas = db.listar_receitas(conn)
    assert len(receitas) == 1
    assert receitas[0]["id"] == rid
    assert receitas[0]["od"] == od and receitas[0]["oe"] == oe
 
 
def test_listar_mais_recente_primeiro_e_limite(conn):
    for esf in (-1.0, -2.0, -3.0):
        db.salvar_receita(conn, Olho(esf), Olho(esf))
    receitas = db.listar_receitas(conn, limite=2)
    assert [r["od"].esferico for r in receitas] == [-3.0, -2.0]
 
 
def test_salvar_orcamento_ligado_a_receita(conn):
    od, oe = Olho(-1.0), Olho(-1.0)
    rid = db.salvar_receita(conn, od, oe)
    escolhido = tres_mais_baratas(od, oe, "aro fechado")[0]
    oid = db.salvar_orcamento(conn, "aro fechado", escolhido, receita_id=rid)
    linha = conn.execute("SELECT * FROM orcamentos WHERE id = ?", (oid,)).fetchone()
    assert linha["receita_id"] == rid
    assert linha["preco"] == escolhido["preco"]
    assert linha["tipo"] == "visão simples"
 
 
def test_orcamento_sem_receita(conn):
    oid = db.salvar_orcamento(conn, "parafusada",
                              {"indice": 1.59, "tipo": "visão simples",
                               "tratamento": "antirreflexo", "preco": 340.0})
    assert oid == 1
 
 
def test_orcamento_com_receita_inexistente_falha(conn):
    with pytest.raises(sqlite3.IntegrityError):
        db.salvar_orcamento(conn, "aro fechado",
                            {"indice": 1.50, "tipo": "visão simples",
                             "tratamento": "sem tratamento", "preco": 120.0},
                            receita_id=999)
 