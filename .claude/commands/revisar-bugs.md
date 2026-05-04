# /revisar-bugs

Varre o projeto em busca de bugs, erros e comportamentos inesperados sem alterar nenhum arquivo.

## Comportamento

1. Se um arquivo for informado (ex: `/revisar-bugs app.py`), analisar somente ele
2. Caso contrario, analisar todos os arquivos relevantes do projeto

## O que procurar

- Erros de logica: condicoes erradas, variaveis usadas antes de serem definidas
- Falhas na integracao com a GitHub API: tratamento de erro ausente, respostas inesperadas nao tratadas
- Problemas de estado no Streamlit: query params mal lidos, cache com comportamento incorreto
- CSS quebrado: seletores que nao funcionam, !important conflitante, dark/light mode inconsistente
- HTML invalido ou mal formado injetado via st.markdown
- Problemas de encoding ou caracteres especiais

## Regras

- Nunca alterar arquivos — apenas reportar
- Classificar cada problema como: critico, medio ou baixo
- Mostrar arquivo + linha onde o problema foi encontrado
- Sugerir a correcao, mas nao aplicar sem confirmacao
- Ignorar `.venv`, `.git` e `assets`
