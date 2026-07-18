# Configuração

Esta página cobre tudo que é necessário para configurar o Soundblend antes de executá-lo: credenciais do Spotify, estrutura de playlists e verificação da configuração.

---

## Credenciais do Spotify

Localmente, o Soundblend usa um arquivo `.env` na raiz do projeto para armazenar as credenciais. Copie o arquivo de exemplo e preencha com os seus valores:

```bash
cp .env.example .env
```

O arquivo `.env` preenchido deve ter este formato:

```dotenv
SPOTIFY_CLIENT_ID=abc123def456abc123def456abc123de
SPOTIFY_CLIENT_SECRET=xyz789xyz789xyz789xyz789xyz789xy
SPOTIFY_REDIRECT_URI=http://localhost:8080/callback
```

### Descrição de cada variável

| Variável | Obrigatória | Descrição |
|---|---|---|
| `SPOTIFY_CLIENT_ID` | Sim | Client ID do seu Spotify App |
| `SPOTIFY_CLIENT_SECRET` | Sim | Client Secret do seu Spotify App |
| `SPOTIFY_REDIRECT_URI` | Sim | URI de redirecionamento OAuth registrada no Dashboard |

!!! danger "Campos obrigatórios sem valor padrão"
    `SPOTIFY_CLIENT_ID`, `SPOTIFY_CLIENT_SECRET` e `SPOTIFY_REDIRECT_URI` não têm valores padrão e a aplicação **não inicia** sem eles. Sem essas variáveis configuradas corretamente, todas as chamadas à API do Spotify falharão com erro de autenticação.

!!! note "Em produção: st.secrets do Streamlit Cloud"
    No Streamlit Community Cloud não existe `.env`. As credenciais ficam em **Settings → Secrets** do app, no formato `.toml` (veja [deploy no Streamlit Cloud](../deploy/streamlit-cloud.md)). O código lê primeiro `st.secrets`, e cai para o `.env`/variável de ambiente como fallback local.

### Como obter o Client ID e o Client Secret

1. Acesse o [Spotify for Developers Dashboard](https://developer.spotify.com/dashboard).
2. Faça login com sua conta Spotify.
3. Clique em **Create app**.
4. Preencha nome e descrição (qualquer texto serve para uso pessoal).
5. No campo **Redirect URIs**, adicione exatamente o valor que você usará em `SPOTIFY_REDIRECT_URI`. Para rodar localmente: `http://localhost:8080/callback`. Para produção no Streamlit Cloud, use a URL do seu app (ex: `https://seuapp.streamlit.app/`).
6. Salve e abra o app criado. O **Client ID** aparece na tela inicial. Clique em **View client secret** para revelar o **Client Secret**.

!!! warning "Segurança das credenciais"
    Nunca commite o arquivo `.env` nem exponha o `SPOTIFY_CLIENT_SECRET` publicamente. O repositório já inclui `.env` no `.gitignore`. Verifique isso antes do primeiro commit.

---

## Configuração de playlists (`config/production.json`)

O arquivo `config/production.json` define quais playlists serão gerenciadas pelo Soundblend e as regras de classificação por gênero de cada uma.

### Estrutura do arquivo

```json
{
  "scopes": [
    "user-library-read",
    "playlist-read-private",
    "playlist-modify-public",
    "playlist-modify-private"
  ],
  "playlists": [
    {
      "id": "37i9dQZF1DX4JAvHpjsfWs",
      "name": "Rock Nacional",
      "genres": ["mpb", "rock nacional", "axé"],
      "ngenres": ["sertanejo"],
      "aoverride": ["Legião Urbana", "Titãs"]
    },
    {
      "id": "37i9dQZF1DXcBWIGoYBM5M",
      "name": "Hip-Hop",
      "genres": ["hip hop", "rap", "trap"],
      "ngenres": [],
      "aoverride": []
    }
  ]
}
```

### Campos de cada playlist

| Campo | Tipo | Descrição |
|---|---|---|
| `id` | string | ID da playlist no Spotify |
| `name` | string | Nome descritivo (apenas para referência interna) |
| `genres` | array de strings | Gêneros que **incluem** uma faixa — basta um coincidir |
| `ngenres` | array de strings | Gêneros que **excluem** uma faixa — têm precedência absoluta sobre `genres` |
| `aoverride` | array de strings | Artistas incluídos independentemente de gênero |

!!! note "Lógica de classificação"
    A precedência é: `ngenres` > `aoverride` > `genres`. Um artista em `aoverride` entra na playlist, mas se ele também tiver um gênero listado em `ngenres`, o `ngenres` vence e ele é excluído. O primeiro gênero de `genres` é injetado como gênero do artista antes da filtragem quando o artista está em `aoverride`.

### Como obter o ID de uma playlist

O ID está na URL da playlist no Spotify Web Player:

```
https://open.spotify.com/playlist/37i9dQZF1DX4JAvHpjsfWs
                                   ^^^^^^^^^^^^^^^^^^^^^^^
                                   este é o ID
```

Basta copiar o trecho após `/playlist/` e antes de qualquer `?` na URL.

### Configuração via interface web

A aba **Playlists** do app permite editar as playlists direto pelo navegador — sidebar com a lista de playlists, e multiselects de gêneros e artistas fixos para cada uma. Não é preciso editar o JSON manualmente. As alterações ficam salvas em `st.session_state`, isoladas por sessão de navegador.

!!! warning "Sem persistência entre sessões"
    Como não há volume ou banco de dados, a configuração feita pela aba **Playlists** vale apenas enquanto a aba estiver aberta. Fechar o navegador ou reiniciar o app volta para os valores padrão do `config/production.json`.

---

## Verificação

Antes de executar o Soundblend, confirme que a configuração está correta:

### 1. Verificar variáveis de ambiente

```bash
# Confirmar que o .env existe e tem as três variáveis obrigatórias
grep -E "SPOTIFY_CLIENT_ID|SPOTIFY_CLIENT_SECRET|SPOTIFY_REDIRECT_URI" .env
```

A saída deve mostrar as três linhas com valores preenchidos (não vazios).

### 2. Verificar credenciais com o script de diagnóstico

Com o ambiente Python ativado, execute:

```bash
python scripts/diagnostico-spotify.py --sample 20
```

Se as credenciais estiverem corretas, o script abre o navegador para o fluxo OAuth na primeira execução e reporta o resultado de cada estratégia de busca. Um erro `401` indica `SPOTIFY_CLIENT_ID` ou `SPOTIFY_CLIENT_SECRET` incorretos. Um erro `INVALID_CLIENT` indica que a `SPOTIFY_REDIRECT_URI` não está registrada no Dashboard.

### 3. Verificar a estrutura do JSON de playlists

```bash
python -c "import json; json.load(open('config/production.json')); print('JSON válido')"
```

!!! tip "Revisão de gêneros antes de sincronizar"
    Depois de logado no app, use a aba **Configurar** para revisar os gêneros de todos os artistas da biblioteca antes de organizar as playlists. O filtro "Só sem gênero" mostra rápido quem precisa de ajuste manual.
