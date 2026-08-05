# Configuração

## Chave da API NVIDIA NIM

O projeto guarda segredos em `.secrets/.env` (fora do `requirements.txt` de produção, essa pasta fica isolada do resto do repo). Copie o arquivo de exemplo e preencha com a sua chave:

```bash
cp .env.example .secrets/.env
```

```dotenv
NVIDIA_API_KEY=seu_api_key_aqui
```

!!! danger "Nunca commitar o .env"
    O arquivo `.secrets/.env` contém a `NVIDIA_API_KEY`. Nunca deve ser commitado com valores reais — verifique o `.gitignore` antes do primeiro commit. Em produção (Streamlit Community Cloud), a chave é lida via `st.secrets` em vez do arquivo.

## Parâmetros do projeto (`config.py`)

Além da chave de API, `config.py` define os caminhos e modelos usados. Não é necessário editar para rodar o projeto como está, mas é a referência caso queira ajustar algo:

| Configuração | Valor padrão | Descrição |
|---|---|---|
| `BIBLE_JSON_PATH` | `data/biblia.json` | Arquivo fonte com os versículos |
| `CHROMA_DB_PATH` | `chroma-db` | Pasta onde o Chroma persiste o banco vetorial |
| `COLLECTION_NAME` | `biblia` | Nome da coleção no Chroma |
| `EMBEDDING_MODEL` | `nvidia/nv-embedqa-e5-v5` | Modelo de embedding da NVIDIA NIM |
| `CHAT_MODEL` | `meta/llama-3.1-8b-instruct` | Modelo de chat completions da NVIDIA NIM |
| `TOP_K` | `40` | Quantos blocos de texto retornar por busca, no máximo |
| `SIMILARIDADE_MINIMA` | `40` | Corte de similaridade (%) abaixo do qual um resultado é descartado |

## Próximo passo

Com a chave configurada, construa o banco vetorial e inicie o app.

[Rodando →](running.md)
