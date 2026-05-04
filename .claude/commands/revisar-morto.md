# /revisar-morto

Identifica codigo, variaveis, funcoes e arquivos que nao sao mais utilizados no projeto.

## Comportamento

1. Se um arquivo for informado (ex: `/revisar-morto app.py`), analisar somente ele
2. Caso contrario, varrer todos os arquivos relevantes do projeto

## O que procurar

- Variaveis declaradas mas nunca lidas
- Funcoes definidas mas nunca chamadas
- Imports nao utilizados
- Blocos de codigo comentado que nao servem mais
- Arquivos que nao sao referenciados em nenhum outro lugar
- Configuracoes em `PROJETOS_CONFIG` para repos que ja foram deletados no GitHub
- CSS com seletores que nao correspondem a nenhum elemento HTML gerado

## Regras

- Nunca deletar ou alterar nada — apenas listar o que foi encontrado
- Para cada item, indicar: o que e, onde esta (arquivo + linha) e por que parece morto
- Classificar o risco de remocao: seguro, verificar antes, nao remover
- Ignorar `.venv`, `.git` e `assets`
