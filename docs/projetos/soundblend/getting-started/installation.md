# Instalação

Esta página descreve como configurar o ambiente local do Soundblend para desenvolvimento ou execução manual.

## Clonar o repositório

```bash
git clone https://github.com/armandonettox/soundblend.git
cd soundblend
```

## Criar ambiente virtual

=== "Windows"

    ```powershell
    python -m venv .venv
    .venv\Scripts\activate
    ```

=== "Linux/Mac"

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

!!! tip "Ative o ambiente virtual sempre que for trabalhar no projeto"
    O ambiente virtual isola as dependências do Soundblend do restante do sistema. Sempre que abrir um terminal novo para trabalhar no projeto, ative o `.venv` antes de rodar qualquer comando Python ou instalar pacotes.

## Instalar dependências

Com o ambiente virtual ativo, instale todas as dependências listadas no `requirements.txt`:

```bash
pip install -r requirements.txt
```

As principais dependências do projeto são:

| Pacote | Uso |
|--------|-----|
| `streamlit` | Interface web com as 3 abas (Configurar, Playlists, Stats) |
| `spotipy` | Cliente oficial da API do Spotify — autenticação OAuth e chamadas REST |
| `python-dotenv` | Leitura das variáveis de ambiente do arquivo `.env` |
| `pandas` | Manipulação de dados e montagem do CSV de artistas e gêneros |
| `pillow` | Processamento de imagens (capas de álbuns e avatares de artistas) |

## Próximo passo

Com o ambiente pronto, configure as credenciais do Spotify e o arquivo de playlists.

[Configuração →](configuration.md)
