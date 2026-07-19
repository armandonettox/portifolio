---
date: 2026-07-19
categories:
  - Dados
---

# AWS Athena vs BigQuery na prática: o que aprendi migrando consultas

Usei BigQuery em projetos de estudo e AWS Athena no dia a dia como analista de dados numa operadora de saúde. São os dois principais "SQL sobre data lake" do mercado e à primeira vista parecem intercambiáveis. Na prática, têm diferenças que mudam como você escreve consulta.

<!-- more -->

## Particionamento

- **Athena** — partitionado por colunas no S3, declaradas no `CREATE TABLE` com `PARTITIONED BY (dt string)`. Precisa rodar `MSCK REPAIR TABLE` após adicionar arquivos novos.
- **BigQuery** — partitionamento nativo por coluna de data/timestamp, declarado no momento da criação da tabela. Sem passo de "repair".

Na prática, em Athena você pensa em particionar como organização de arquivos no S3. Em BigQuery é um detalhe do schema.

## Formato de arquivo

- **Athena** — performance depende fortemente do formato. Parquet com compressão Snappy é a recomendação. CSV é suicídio em tabelas grandes.
- **BigQuery** — você carrega os dados e ele cuida do formato interno. Não pensa nisso.

Se você migrou de um pra outro, esse é o ajuste mental mais brusco: em Athena você é meio engenheiro de dados também.

## Custo

Ambos cobram por bytes lidos, mas a modelagem é diferente:

- **Athena** — cobrado por TB escaneado. Selecionar colunas que não precisa custa caro.
- **BigQuery** — cobrado por TB escaneado também, mas com cached results gratuitos por 24h.

A cache do BigQuery é uma vantagem operacional enorme pra dashboards e relatórios repetidos. Em Athena, consultas idênticas em sequência pagam duas vezes.

## Sintaxe

Ambos seguem ANSI SQL, mas:
- **Athena** (Trino/Presto por baixo) — funções de array/mapa nativas, `UNNEST` pra explodir arrays.
- **BigQuery** — arrays e structs de primeira classe, `UNNEST` com `LEFT JOIN` implícito, funções analíticas mais ricas.

Pra análise exploratória com arrays, BigQuery é mais ergonômico.

## O que uso quando

- **Dia a dia na operadora** — Athena, porque os dados já estão no S3 em Parquet e a infra é AWS.
- **Estudo e protótipos** — BigQuery quando quero agilidade e cache.
- **Consultas analíticas pesadas** — BigQuery, pela predictable performance e funções de janela mais ricas.

## O que aprendi

- Escolher entre Athena e BigQuery é quase sempre uma decisão de infraestrutura existente, não de preferência técnica.
- Em Athena, saber como seus dados estão armazenados no S3 é metade do trabalho de analista. Em BigQuery isso é transparência.
- Cache de 24h do BigQuery parece detalhe, mas muda completamente a conta no fim do mês para dashboards de uso recorrente.