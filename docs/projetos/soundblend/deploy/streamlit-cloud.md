# Deploy no Streamlit Community Cloud

O Soundblend roda no [Streamlit Community Cloud](https://share.streamlit.io), sem servidor próprio, sem Docker e sem volume persistente. Cada sessão de navegador guarda seu próprio estado (token OAuth, cache de artistas, overrides) em `st.session_state` — nada é gravado em disco entre deploys.

## Criar o app

1. Acesse [share.streamlit.io](https://share.streamlit.io) e faça login com a conta do GitHub.
2. Clique em **New app** → **Deploy a public app from GitHub**.
3. Selecione o repositório `armandonettox/soundblend`, branch `master`, main file `app.py`.
4. Escolha o subdomínio da app (define a URL final `https://<nome>.streamlit.app`).
5. Clique em **Deploy**.

## Configurar os secrets

No painel do app, em **Settings → Secrets**, cole:

```toml
[spotify]
client_id = "seu_client_id"
client_secret = "seu_client_secret"
redirect_uri = "https://<nome-escolhido>.streamlit.app/"
```

## Atualizar o Spotify Developer Dashboard

No [Spotify Developer Dashboard](https://developer.spotify.com/dashboard), no app registrado, adicione a mesma URL em **Redirect URIs**: `https://<nome-escolhido>.streamlit.app/`.

## Limitações do modelo sem disco

Como não há volume persistente, o que era salvo em arquivo antes (cache de artistas, overrides de gênero, aliases, snapshot de sync) agora vive só na sessão do navegador. Isso significa:

- Fechar a aba ou reiniciar o app perde o cache e os overrides configurados.
- Não há mais sincronização agendada automática (o antigo fluxo via GitHub Actions + `sync_cli.py` foi removido).

A única exceção é o cache de gêneros (`genre_cache.json`), que fica no disco do container — sobrevive entre sessões, mas se perde a cada redeploy ou restart do container e é reconstruído sob demanda.
