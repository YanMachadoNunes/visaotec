# Proposta A3 — VisãoTec: Assistente Técnico para Óticas

Nov 11, 2026 · @Yan

## Identificação

- **Disciplina:** Matemática Computacional Aplicada
- **Professores:** Aron e Cristiano
- **Integrantes:** Maycon da Silva Pereira, Yan Machado Nunes
- **Tema:** próprio, sujeito à aprovação do professor

## Nome, problema e público

**VisãoTec** — assistente web que interpreta receitas de óculos, recomenda a lente adequada e analisa as vendas de uma ótica.

**Problema real.** Em óticas pequenas, o atendente faz conversões de receita à mão (transposição de cilindro, grau de perto) e escolhe o índice da lente "no olho". Erros nessas contas geram lentes refeitas, prejuízo e cliente insatisfeito. Além disso, o dono raramente sabe quais armações e lentes vendem mais em cada mês, e compra estoque sem base em dados.

**Público-alvo:**

- Atendentes e vendedores de óticas, que precisam conferir receitas no balcão
- Donos e gerentes de óticas pequenas, que precisam planejar compras de estoque
- Estudantes de cursos técnicos de óptica, como ferramenta de apoio

## Solução proposta

O VisãoTec tem três módulos, acessados por abas numa interface web.

1. **Conferência de receita:** o atendente digita esférico, cilíndrico, eixo e adição de cada olho. O sistema valida os valores, faz a transposição de cilindro, calcula o grau de perto e o equivalente esférico, e alerta sobre receitas fora do padrão.
2. **Recomendação de lente:** a partir do maior grau, o sistema sugere o índice de refração adequado e lista quais combinações de lente e armação são compatíveis. Também conta quantas opções de orçamento existem e monta as três mais baratas.
3. **Painel de vendas:** com dados fictícios de vendas de uma ótica, mostra as armações e lentes mais vendidas, o faturamento por mês e uma previsão de demanda para os próximos meses, gerada por um modelo de machine learning.

**Funcionalidades da interface:**

- Formulário de receita com resultado e explicação de cada conta
- Exibição das fórmulas usadas em cada cálculo
- Filtro de armações compatíveis com a receita
- Gráficos de vendas e de previsão de demanda
- Histórico de receitas e orçamentos salvo em banco de dados

## Conteúdos da disciplina aplicados

O projeto aplica sete conteúdos da disciplina, acima do mínimo de três exigido.

| Conteúdo | Onde aparece no projeto |
| --- | --- |
| Funções | Transposição de cilindro, grau de perto, equivalente esférico e escolha do índice por faixa de grau |
| Noção de conjuntos | Compatibilidade entre lentes e armações como interseção de conjuntos |
| Princípio fundamental da contagem e combinação | Número de orçamentos possíveis: 4 índices × 3 tipos de lente × 4 tratamentos = 48 opções |
| DataFrames com Pandas | Tabelas de vendas, estoque e receitas |
| Gráficos com matplotlib | Vendas por mês, ranking de produtos e curva de previsão |
| Machine learning | Regressão linear (scikit-learn) para prever vendas mensais por categoria |
| Banco de dados | SQLite com receitas, orçamentos, produtos e vendas |

**Transposição de cilindro.** Uma mesma receita pode ser escrita com cilindro negativo ou positivo. Laboratórios costumam pedir em cilindro negativo:

```latex
E' = E + C, \quad C' = -C, \quad \theta' = \theta \pm 90^\circ
```

O novo eixo θ' sempre fica entre 1° e 180°.

**Grau de perto**, para óculos de leitura e multifocais, somando a adição (A) ao esférico:

```latex
E_{perto} = E_{longe} + A
```

**Equivalente esférico**, usado para escolher o índice da lente e comparar graus:

```latex
EE = E + \frac{C}{2}
```

**Compatibilidade como conjuntos.** Cada armação aceita um conjunto de lentes, e cada receita permite outro conjunto. As opções válidas para o cliente são a interseção:

```latex
\text{Opções} = L_{\text{armação}} \cap L_{\text{receita}}
```

Exemplo: uma armação parafusada (sem aro) só aceita policarbonato ou trivex, porque o furo pode trincar lentes comuns.

## Tecnologias, dados e cronograma

| Camada | Tecnologia |
| --- | --- |
| Linguagem | Python 3 |
| Interface web | Streamlit |
| Dados | Pandas |
| Gráficos | matplotlib |
| Machine learning | scikit-learn (regressão linear) |
| Banco de dados | SQLite |
| Versionamento | GitHub, com README de instalação e execução |

**Dados:** todos fictícios, gerados pelo grupo com um script Python: catálogo de armações e lentes, 12 meses de vendas e receitas de exemplo. Nenhum dado de clientes reais será usado.

| Etapa | Entrega | Prazo |
| --- | --- | --- |
| Proposta | Este documento | \[data de envio\] |
| Protótipo | Módulo de conferência de receita funcionando na interface | 11/11/2026 |
| Versão final | Recomendação de lente, painel de vendas, modelo de previsão, banco e README | 18/11/2026 |
| Amostra da A3 | Pôster com QR Code para o repositório e vídeo de demonstração | 01/12/2026 |
