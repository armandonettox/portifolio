# Arquitetura

## Visão geral

O Soundblend é uma aplicação Streamlit de página única que conecta o usuário ao Spotify via OAuth, busca as músicas curtidas e redistribui automaticamente em playlists por gênero musical.

```
                                          ┌─────────────────────┐
                                          │     Spotify API      │
                                          │  (api.spotify.com)   │
                                          └──────────┬──────────┘
                                                     │ HTTPS / OAuth 2.0
                        ┌────────────────────────────┼────────────────────────────┐
                        │                            │                            │
               ┌────────┴────────┐      ┌────────────▼───────────┐               │
               │   Browser do    │      │    spotify_client.py    │               │
               │    usuário      │◄────►│  (autenticação, dados)  │               │
               └────────┬────────┘      └────────────┬───────────┘               │
                        │ HTTP :8501                  │                           │
               ┌────────▼────────┐                   │                           │
               │    app.py       │◄──────────────────┘                           │
               │  Streamlit UI   │                                                │
               │  (3 abas)       │                                                │
               └────────┬────────┘                                                │
                        │                                                         │
                 ┌──────▼──────┐                                                  │
                 │ commands/   │                                                  │
                 │ reload.py   │                                                  │
                 │ (sincroniza)│                                                  │
                 └─────────────┘                                                  │
└────────────────────────────────────────────────────────────────────────────────┘
```

As abas **Configurar** e **Stats** não têm módulo próprio em `commands/` — a edição de gêneros/overrides e a agregação de estatísticas são feitas direto em `app.py` a partir do cache de artistas da sessão.

---

## Módulos

### `app.py` — Interface principal

**Responsabilidade:** ponto de entrada da aplicação. Gerencia o ciclo de autenticação OAuth, renderiza as três abas da UI e despacha ações para `commands/reload.py`.

**Funções/abas principais:**

| Aba | Função |
|-----|--------|
| Configurar | Tabela editável com todos os artistas da biblioteca e seus gêneros; editar e salvar grava um override por artista |
| Playlists | Edita playlists, gêneros e artistas fixos, e dispara `plan_reload()`/`run_reload()` — preview, sincronização incremental e undo |
| Stats | Cobertura de gênero da biblioteca e top gêneros por número de artistas |

**Dependências:** `streamlit`, `spotify_client.py`, `commands/*`, variáveis de ambiente via `.env`.

**Observações:** carrega CSS customizado com a identidade visual da marca (roxo `#7B2FBE`, laranja `#E8611A`). Toda a sessão do usuário é mantida via `st.session_state`.

---

### `spotify_client.py` — Camada de acesso ao Spotify

**Responsabilidade:** encapsula toda comunicação com a API do Spotify. Gerencia autenticação OAuth, busca paginada de faixas salvas, enriquecimento de artistas com gêneros e leitura de playlists.

**Funções principais:**

| Função | O que faz |
|--------|-----------|
| `create_auth_manager()` | Configura o fluxo OAuth 2.0 com escopos mínimos e `show_dialog=True` |
| `get_saved_tracks(sp)` | Busca todas as músicas curtidas; a primeira página informa o total e as demais são baixadas em paralelo por offset |
| `extract_artists_from_tracks(tracks)` | Extrai artistas únicos (todos os artistas de cada faixa) sem chamar a API |
| `enrich_artists_with_genres(artists)` | Preenche gêneros via cache em disco e MusicBrainz (1 req/s) |
| `decorate_artist_genres(tracks, artist_map)` | Anexa a lista de gêneros do artista a cada faixa |
| `get_user_playlists(sp)` | Lista todas as playlists do usuário autenticado |

**Dependências:** `spotipy`, `requests` (MusicBrainz), `concurrent.futures.ThreadPoolExecutor`, `.env` (credenciais).

!!! note "Fonte dos gêneros: MusicBrainz"
    A API do Spotify não retorna mais gêneros de artista (campo deprecado). O Soundblend busca o artista por nome no MusicBrainz, prefere match exato de nome entre os resultados e lê o campo `genres` (curado pela comunidade). Tags cruas só entram como fallback, filtradas pela taxonomia de `genre_taxonomy.py`, que colapsa tudo em ~25 macro-gêneros.

---

### `commands/reload.py` — Sincronização de playlists

**Responsabilidade:** implementa a lógica central do Soundblend — calcula o diff entre o estado atual de cada playlist e o que as regras de gênero determinam, e aplica só a diferença.

**Funções principais:** `plan_reload(sp, playlists)` calcula o preview sem alterar nada; `run_reload(sp, playlists, plan=...)` aplica o diff calculado.

**Dependências:** `spotify_client.py`, configuração de playlists da sessão.

Detalhamento do fluxo em [Fluxo de sincronização](#fluxo-de-sincronizacao).

---

## Fluxo OAuth

O Soundblend usa o fluxo Authorization Code do OAuth 2.0 via `spotipy.SpotifyOAuth`, com um `CacheHandler` customizado (`StreamlitSessionCacheHandler`) que guarda o token em `st.session_state` em vez de disco.

```
app.py (init)
    │
    ▼
Verifica st.session_state
    │
    ├── [token presente e não expirado]
    │       │
    │       ▼
    │   Instancia sp com token da sessão
    │       │
    │       ▼
    │   Renderiza UI autenticada
    │
    └── [sem token ou token expirado]
            │
            ▼
        Gera URL de autorização Spotify
            │
            ▼
        Exibe link para o usuário
            │
            ▼
        Browser → accounts.spotify.com
            │
            ▼
        Usuário aprova escopos
            │
            ▼
        Spotify redireciona para SPOTIFY_REDIRECT_URI
        (ex: https://seuapp.streamlit.app/?code=ABC123)
            │
            ▼
        app.py captura o parâmetro `code` via query string
            │
            ▼
        Troca `code` por access_token + refresh_token
            │
            ▼
        Salva tokens em st.session_state
            │
            ▼
        st.rerun() — recarrega sessão autenticada
```

!!! note "Cache de token em sessão"
    O token (access token + refresh token) fica em `st.session_state`, isolado por sessão de navegador — nunca é gravado em disco. Quando o access token expira (1h), ele é renovado com o refresh token de forma transparente, sem derrubar a sessão. Fechar a aba ou reiniciar o app perde o token, exigindo novo login.

!!! note "show_dialog e escopos mínimos"
    O `SpotifyOAuth` usa `show_dialog=True`: todo login passa pela tela de autorização do Spotify, impedindo que outra pessoa no mesmo navegador reconecte com um clique após o logout. Os escopos pedidos são só os usados: `user-library-read`, `playlist-read-private`, `playlist-modify-public` e `playlist-modify-private`.

!!! warning "Redirect URI"
    A `SPOTIFY_REDIRECT_URI` definida no `.env` deve estar cadastrada exatamente igual no painel do Spotify Developer App. Qualquer diferença (trailing slash, http vs https) resulta em erro 400.

---

## Fluxo de sincronização

A sincronização é incremental e em duas fases: `plan_reload` calcula o diff de cada playlist sem modificar nada (é o preview mostrado ao usuário), e `run_reload` aplica o diff confirmado.

### Passo a passo

**1. Biblioteca já carregada na sessão**

As músicas curtidas e o mapa artista→gêneros são carregados na abertura da sessão e reutilizados pela sincronização — nenhum refetch.

**2. Decoração das faixas com gêneros**

```python
decorated = decorate_artist_genres(tracks, artist_map=artist_map, multi_artist=...)
# Anexa os gêneros do artista a cada faixa
# Com multi_artist, une os gêneros de todos os artistas da faixa
```

**3. Para cada playlist configurada:**

- **Filtro por `genres`** (expandido com aliases): a faixa entra se qualquer gênero bater.
- **`aoverride`**: a faixa entra se o artista estiver na lista de fixos, independente de gênero.
- **Exclusão por `ngenres`** (também expandido com aliases): precedência absoluta — remove mesmo que `genres` ou `aoverride` batam.
- **Ordenação**: artista → álbum.
- **Diff**: compara com o conteúdo atual da playlist e calcula só o que adicionar e o que remover.

**4. Snapshot e aplicação**

Antes de aplicar, o estado atual de cada playlist é salvo em um snapshot na sessão (botão "Desfazer última sincronização"). Depois, remoções e adições são aplicadas em chunks de 100 (limite da API).

!!! danger "Precedência do ngenres"
    Se um artista tiver gêneros que batem tanto com `genres` quanto com `ngenres`, ele **sempre** será excluído. O `ngenres` é executado por último e sua decisão é final.

---

## Performance e limites de API

- **Músicas curtidas:** a primeira página informa o total; as demais são baixadas em paralelo por offset (`ThreadPoolExecutor`, 5 workers), preservando a ordem.
- **MusicBrainz:** o limite é **1 requisição por segundo**. Um throttle global espaça as requisições mesmo com várias sessões enriquecendo ao mesmo tempo; 503 recebe retry com backoff. Por isso o primeiro enriquecimento de uma biblioteca grande leva minutos — as sessões seguintes leem do cache em disco.
- **Spotify:** adições e remoções de playlist em chunks de 100 (limite da API).

---

## Persistência

O Soundblend não guarda nenhum dado de usuário em disco. A única exceção é o cache de gêneros, que é metadado público.

### Cache de gêneros (`genre_cache.json`)

| Atributo | Valor |
|----------|-------|
| Arquivo | `genre_cache.json` na raiz do app (gitignored) |
| Conteúdo | `{artist_id: {name, genres_raw, ts}}` — gênero de artista é metadado público, não identifica nenhum usuário |
| TTL | 30 dias por entrada |
| Compartilhamento | Global entre usuários e sessões — o enriquecimento MusicBrainz é pago uma vez por artista |
| Normalização | `genres_raw` guarda as tags cruas; os macro-gêneros são recalculados na leitura, então melhorias na taxonomia valem retroativamente |

No Streamlit Cloud o disco é efêmero: o cache sobrevive entre sessões, mas se perde em cada redeploy ou restart do container e é reconstruído sob demanda.

Todo o resto vive em `st.session_state`, isolado por sessão de navegador e perdido ao fechar a aba ou reiniciar o app.

### Token OAuth

| Atributo | Valor |
|----------|-------|
| Armazenamento | `st.session_state` (chave interna do `StreamlitSessionCacheHandler`) |
| Conteúdo | `access_token`, `refresh_token`, `expires_at`, `scope` |
| Gerado por | `spotipy.SpotifyOAuth` automaticamente |
| Escopo | Por sessão de navegador — não compartilhado entre usuários nem persistido entre reinícios |

### Configuração de playlists

| Atributo | Valor |
|----------|-------|
| Arquivo base | `config/production.json` (versionado no repositório) |
| Override em runtime | `st.session_state.playlists`, editável pela aba **Playlists** |
| Conteúdo | JSON com array de playlists (id, name, genres, ngenres, aoverride) |

O arquivo base `config/production.json` é o padrão carregado no início da sessão. Qualquer edição feita pela aba **Playlists** sobrescreve `st.session_state.playlists` só para aquela sessão — não persiste entre reinícios do app nem entre usuários diferentes.

Cache de artistas, overrides de gênero, aliases e snapshot de sync seguem o mesmo padrão: dicts guardados em `st.session_state`, chaveados por `user_id`.

**Estrutura de uma entrada de playlist:**

```json
{
  "id": "37i9dQZF1DX...",
  "name": "Rock Nacional",
  "genres": ["mpb", "brazilian rock", "pagode"],
  "ngenres": ["funk carioca", "sertanejo"],
  "aoverride": ["Legião Urbana", "Titãs"]
}
```
