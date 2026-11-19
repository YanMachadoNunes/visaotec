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
| `visaotec/vendas.py` | Leitura das vendas, ranking e faturamento mensal, total ou por categoria | Pandas |
| `visaotec/previsao.py` | Regressão linear da demanda, com R², erro médio e teste nos últimos meses | Machine learning |
| `visaotec/graficos.py` | Gráficos de ranking, faturamento e previsão | matplotlib |
| `visaotec/estilo.py` | Cores e formatação comuns aos gráficos | matplotlib |
| `visaotec/db.py` + `schema.sql` | Banco SQLite | Banco de dados |
| `scripts/gerar_dados.py` | Gera catálogo, 12 meses de vendas e receitas fictícias | Banco de dados |
| `app.py` | Interface Streamlit com as três abas | |
| `tests/` | Testes de receita, lentes, vendas e previsão | |

## Previsão de demanda

O painel ajusta uma reta `y = ax + b`, em que `x` é o número do mês (0 no primeiro mês) e `y` é o total de itens ou o faturamento. A previsão pode usar todas as vendas ou só armações ou lentes. A reta capta a tendência, mas não a sazonalidade.

Todos os dados são fictícios.
