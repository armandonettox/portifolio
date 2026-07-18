# Arquitetura

## Estrutura do projeto

```
verbo/
    data/
        biblia-ave-maria.json    <- fonte validada (73 livros, 35.450 versículos)
        construir-banco.py       <- gera embeddings e popula o Chroma
    modules/
        busca.py                 <- consulta o Chroma, retorna versículos próximos
        resposta.py              <- monta prompt e chama NVIDIA NIM chat completions
    app.py                       <- interface Streamlit
    config.py                    <- configurações, nomes de modelo, paths
```

## Módulos

### `app.py` — Interface

Ponto de entrada Streamlit. Recebe a pergunta do usuário, chama `buscar_versiculos()` e `gerar_resposta()` em sequência, e exibe a resposta seguida dos versículos consultados.

### `modules/busca.py` — Busca por similaridade

**`buscar_versiculos(pergunta)`**

1. Gera o embedding da pergunta via NVIDIA NIM (`EMBEDDING_MODEL`).
2. Consulta a coleção do Chroma (`CHROMA_DB_PATH` / `COLLECTION_NAME`) com esse vetor.
3. Retorna os `TOP_K` versículos mais próximos, cada um com `texto` e `referencia`.

Cliente OpenAI e coleção Chroma são inicializados uma única vez (lazy, via `_init()`) e reutilizados entre chamadas.

### `modules/resposta.py` — Geração da resposta

**`gerar_resposta(pergunta, versiculos)`**

Monta um prompt com os versículos encontrados como contexto e uma instrução explícita para responder **exclusivamente** com base neles, chama o modelo de chat da NVIDIA NIM (`CHAT_MODEL`) e retorna o texto da resposta.

### `data/construir-banco.py` — Indexação

Lê `biblia-ave-maria.json`, gera o embedding de cada versículo via NVIDIA NIM e popula a coleção do Chroma. Roda uma única vez (ou sempre que a fonte de dados mudar).

## Fluxo de uma pergunta

```
Usuário digita a pergunta (app.py)
        ↓
busca.buscar_versiculos(pergunta)
  - embedding da pergunta (NVIDIA NIM)
  - query no Chroma → top 5 versículos
        ↓
resposta.gerar_resposta(pergunta, versiculos)
  - monta prompt com os versículos como contexto
  - chat completion (NVIDIA NIM)
        ↓
app.py exibe resposta + versículos consultados
```

## API usada

Ambos os módulos (`busca.py` e `resposta.py`) usam o cliente `openai.OpenAI` apontado para o endpoint da NVIDIA NIM (`base_url="https://integrate.api.nvidia.com/v1"`), autenticado com `NVIDIA_API_KEY`. É a mesma API para embeddings e chat completions, só muda o modelo.
