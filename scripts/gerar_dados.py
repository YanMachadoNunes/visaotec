"""Gera os dados fictícios do VisãoTec e grava em data/visaotec.db.

- catálogo de armações e lentes
- 12 meses de vendas
- receitas de exemplo
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from visaotec import db  # noqa: E402

SEMENTE = 42  # para os dados saírem iguais toda vez


def gerar_catalogo():
    # TODO: lista de armações (com tipo de montagem) e lentes, com preços
    raise NotImplementedError


def gerar_vendas(catalogo, meses: int = 12):
    # TODO: vendas por dia/mês; vale pôr tendência e sazonalidade para a regressão ter o que aprender
    raise NotImplementedError


def gerar_receitas(n: int = 50):
    # TODO
    raise NotImplementedError


def main():
    conn = db.conectar()
    db.criar_tabelas(conn)
    # TODO: chamar os geradores e inserir no banco
    conn.commit()
    print(f"Banco criado em {db.CAMINHO_DB}")


if __name__ == "__main__":
    main()
