# Verbo

Verbo é um RAG fechado sobre a Bíblia Católica Ave Maria, em português. Responde perguntas usando só o texto da Bíblia como fonte, sem inventar com conhecimento geral do LLM. Projeto público, pensado para qualquer pessoa usar após publicação.

O nome é uma referência a João 1:1, "no princípio era o Verbo".

## Stack

- Python 3.x
- ChromaDB (banco vetorial local)
- NVIDIA NIM (embeddings + chat completions, free tier)
- Streamlit (interface)
- python-dotenv

## Fonte dos dados

Bíblia Ave Maria (católica), do repositório [`fidalgobr/bibliaAveMariaJSON`](https://github.com/fidalgobr/bibliaAveMariaJSON): 35.450 versículos, 73 livros, UTF-8.

## Como funciona

1. **Banco vetorial (Chroma)** — guarda cada versículo transformado em vetor, organizado por assunto
2. **Embedding (NVIDIA NIM)** — transforma texto em vetor de significado; calculado uma vez para os versículos e a cada pergunta nova
3. **Busca por similaridade** — compara a pergunta com os vetores existentes, retorna os 5 versículos mais próximos
4. **Geração da resposta (NVIDIA NIM, chat completions)** — recebe pergunta + versículos encontrados e responde só com base nisso

A resposta sempre cita a referência (livro, capítulo, versículo) dos trechos usados.

## Começando

- [Instalação](getting-started/installation.md) — ambiente virtual e dependências
- [Configuração](getting-started/configuration.md) — chave da API NVIDIA NIM
- [Rodando](getting-started/running.md) — construir o banco vetorial e iniciar o app
