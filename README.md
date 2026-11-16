# VisãoTec

Assistente web para óticas: confere receitas de óculos, recomenda lentes e analisa vendas.
Trabalho A3 de Matemática Computacional Aplicada (profs. Aron e Cristiano).

Integrantes: Maycon da Silva Pereira, Yan Machado Nunes.

## Instalação

```bash
uv venv --python 3.12
source .venv/bin/activate      # fish: source .venv/bin/activate.fish
uv pip install -r requirements.txt
```

## Execução

```bash
python scripts/gerar_dados.py   # cria data/visaotec.db com dados fictícios
streamlit run app.py
```

## Testes

```bash
pytest
```

## Estrutura

| Caminho | O que tem | Conteúdo da disciplina |
| --- | --- | --- |
| `visaotec/receita.py` | Transposição, grau de perto, equivalente esférico, validação | Funções |
| `visaotec/lentes.py` | Índice por faixa, compatibilidade, contagem de orçamentos | Funções, conjuntos, contagem |
| `visaotec/vendas.py` | Ranking e faturamento mensal | Pandas, matplotlib |
| `visaotec/previsao.py` | Regressão linear da demanda | Machine learning |
| `visaotec/db.py` + `schema.sql` | Banco SQLite | Banco de dados |
| `scripts/gerar_dados.py` | Gera catálogo, 12 meses de vendas e receitas fictícias | Pandas |
| `app.py` | Interface Streamlit com as três abas | |

Todos os dados são fictícios.
