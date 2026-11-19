# VisãoTec

Assistente web para óticas: confere receitas de óculos, recomenda lentes e analisa vendas.
Trabalho A3 de Matemática Computacional Aplicada (profs. Aron e Cristiano).

Integrantes: Maycon da Silva Pereira, Yan Machado Nunes.

## Instalação

Requer Python 3.12.

Linux ou macOS:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Windows (PowerShell):

```powershell
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Execução

```bash
python scripts/gerar_dados.py   # cria data/visaotec.db com dados fictícios
streamlit run app.py
```

O app abre em `http://localhost:8501`.

## Como usar

1. **Conferência de receita:** preencha os dois olhos e clique em "Conferir receita". O app mostra alertas, contas e fórmulas, e permite salvar a receita.
2. **Recomendação de lente:** usa a receita preenchida, sugere o índice, filtra as lentes pela armação e monta as três opções mais baratas.
3. **Painel de vendas:** mostra os mais vendidos, o faturamento mensal e a previsão de demanda.
4. **Histórico:** lista as receitas e os orçamentos salvos.

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
| `visaotec/db.py` | Tabelas SQLite e histórico de receitas e orçamentos | Banco de dados |
| `visaotec/consultas.py` | Consultas de leitura usadas pela interface | Banco de dados |
| `scripts/gerar_dados.py` | Gera catálogo, 12 meses de vendas e receitas fictícias | Banco de dados |
| `app.py` | Interface Streamlit com as abas de receita, lentes, vendas e histórico | |
| `tests/` | Testes de receita, lentes, vendas, previsão e banco | |

## Previsão de demanda

O painel ajusta uma reta `y = ax + b`, em que `x` é o número do mês (0 no primeiro mês) e `y` é o total de itens ou o faturamento. A previsão pode usar todas as vendas ou só armações ou lentes. A reta capta a tendência, mas não a sazonalidade.

Todos os dados são fictícios.
