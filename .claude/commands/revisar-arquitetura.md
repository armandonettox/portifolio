# /revisar-arquitetura

Analisa a arquitetura do projeto e sugere melhorias sem alterar nenhum arquivo.

## Comportamento

1. Se um arquivo for informado (ex: `/revisar-arquitetura app.py`), analisar somente ele
2. Caso contrario, listar todos os arquivos relevantes do projeto e analisar cada um

## O que analisar

- Organizacao geral: responsabilidades bem definidas, separacao de logica e apresentacao
- Tamanho e complexidade: funcoes ou blocos grandes demais que deveriam ser separados
- Dependencias: imports desnecessarios, acoplamento excessivo
- Consistencia: padroes seguidos de forma uniforme ao longo do codigo
- Oportunidades de simplificacao sem perder clareza

## Regras

- Nunca alterar arquivos — apenas sugerir
- Apresentar os problemas em ordem de prioridade (mais critico primeiro)
- Para cada problema, mostrar onde esta (arquivo + linha) e o que poderia ser feito
- Ignorar `.venv`, `.git` e `assets`
