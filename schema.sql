-- Esquema do banco VisãoTec (SQLite)
-- TODO: revisar colunas e tipos conforme o projeto evoluir

CREATE TABLE IF NOT EXISTS produtos (
    id        INTEGER PRIMARY KEY,
    categoria TEXT NOT NULL,      -- 'armacao' ou 'lente'
    nome      TEXT NOT NULL,
    preco     REAL NOT NULL
    -- TODO: campos de armação (tipo de montagem) e de lente (índice, tipo, material)
);

CREATE TABLE IF NOT EXISTS vendas (
    id         INTEGER PRIMARY KEY,
    data       TEXT NOT NULL,     -- ISO 'AAAA-MM-DD'
    produto_id INTEGER NOT NULL REFERENCES produtos(id),
    quantidade INTEGER NOT NULL,
    valor      REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS receitas (
    id        INTEGER PRIMARY KEY,
    criada_em TEXT NOT NULL,
    -- olho direito (OD) e esquerdo (OE)
    od_esf REAL, od_cil REAL, od_eixo INTEGER, od_add REAL,
    oe_esf REAL, oe_cil REAL, oe_eixo INTEGER, oe_add REAL
);

CREATE TABLE IF NOT EXISTS orcamentos (
    id         INTEGER PRIMARY KEY,
    receita_id INTEGER REFERENCES receitas(id),
    criado_em  TEXT NOT NULL,
    descricao  TEXT,
    total      REAL
);
