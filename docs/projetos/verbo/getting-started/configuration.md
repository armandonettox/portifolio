# Configuração

## Chave da API NVIDIA NIM

Copie o arquivo de exemplo e preencha com a sua chave:

```bash
cp .env.example .env
```

```dotenv
NVIDIA_API_KEY=seu_api_key_aqui
```

!!! danger "Nunca commitar o .env"
    O arquivo `.env` contém a `NVIDIA_API_KEY`. Nunca deve ser commitado com valores reais — verifique o `.gitignore` antes do primeiro commit.

## Parâmetros do projeto (`config.py`)

Além da chave de API, `config.py` define os caminhos e modelos usados. Não é necessário editar para rodar o projeto como está, mas é a referência caso queira ajustar algo:

| Configuração | Valor padrão | Descrição |
|---|---|---|
| `BIBLE_JSON_PATH` | `data/biblia-ave-maria.json` | Arquivo fonte com os versículos |
| `CHROMA_DB_PATH` | `chroma-db` | Pasta onde o Chroma persiste o banco vetorial |
| `COLLECTION_NAME` | `biblia` | Nome da coleção no Chroma |
| `EMBEDDING_MODEL` | `nvidia/nv-embedqa-e5-v5` | Modelo de embedding da NVIDIA NIM |
| `CHAT_MODEL` | `meta/llama-3.1-8b-instruct` | Modelo de chat completions da NVIDIA NIM |
| `TOP_K` | `5` | Quantos versículos retornar por busca |

## Próximo passo

Com a chave configurada, construa o banco vetorial e inicie o app.

[Rodando →](running.md)
