# Instalação

## Ambiente virtual

```bash
python -m venv .venv
```

=== "Windows"

    ```powershell
    .venv\Scripts\activate
    ```

=== "Linux/Mac"

    ```bash
    source .venv/bin/activate
    ```

## Dependências

```bash
pip install -r requirements.txt
```

| Pacote | Uso |
|--------|-----|
| `chromadb` | Banco vetorial local, armazena os blocos de texto como embeddings |
| `openai` | Cliente usado para chamar a API da NVIDIA NIM (embeddings e chat completions) |
| `streamlit` | Interface web |
| `python-dotenv` | Leitura das variáveis de ambiente do arquivo `.env` |

Dependências de teste (pytest e afins) ficam separadas, em `tests/requirements.txt`:

```bash
pip install -r tests/requirements.txt
```

## Próximo passo

Com o ambiente pronto, configure a chave da API NVIDIA NIM.

[Configuração →](configuration.md)
