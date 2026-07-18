# Variáveis de ambiente

## Resumo

| Variável | Obrigatória | Padrão | Descrição |
|---|---|---|---|
| `SPOTIFY_CLIENT_ID` | Sim | — | Client ID do Spotify App |
| `SPOTIFY_CLIENT_SECRET` | Sim | — | Client Secret do Spotify App |
| `SPOTIFY_REDIRECT_URI` | Sim | `http://localhost:8080/callback` | URI de redirect OAuth |
| `YTMUSIC_CLIENT_ID` | Não | — | Client ID OAuth do YouTube Music (habilita o login alternativo) |
| `YTMUSIC_CLIENT_SECRET` | Não | — | Client Secret OAuth do YouTube Music |

Em produção (Streamlit Community Cloud), essas chaves ficam em `st.secrets` (seções `[spotify]` e `[ytmusic]`) em vez de variáveis de ambiente — veja [Configuração em produção](#configuracao-em-producao).

---

## Detalhes por variável

### SPOTIFY_CLIENT_ID

O identificador público do seu Spotify App, gerado automaticamente pelo Spotify Developer Dashboard ao criar o app. É uma string alfanumérica de 32 caracteres.

**Onde obter:** [Spotify Developer Dashboard](https://developer.spotify.com/dashboard) → selecione seu app → aba *Settings* → campo *Client ID*.

**Exemplo:**

```env
SPOTIFY_CLIENT_ID=a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4
```

**O que acontece se ausente:** o app lança `spotipy.exceptions.SpotifyOauthError` na inicialização e não consegue montar o fluxo OAuth. Nenhuma aba do Streamlit funciona.

---

### SPOTIFY_CLIENT_SECRET

A chave secreta do Spotify App, usada para autenticar o servidor no fluxo OAuth 2.0. Deve ser tratada como senha — nunca exposta publicamente.

**Onde obter:** mesmo local do Client ID → clique em *View client secret*.

**Exemplo:**

```env
SPOTIFY_CLIENT_SECRET=z9y8x7w6v5u4z9y8x7w6v5u4z9y8x7w6
```

**O que acontece se ausente:** mesmo comportamento do `SPOTIFY_CLIENT_ID` — a autenticação falha imediatamente.

---

### SPOTIFY_REDIRECT_URI

A URI para a qual o Spotify redireciona o navegador após o usuário autorizar o app. Deve estar cadastrada exatamente igual no Spotify Developer Dashboard, caso contrário o Spotify rejeita o callback com erro `INVALID_CLIENT: Invalid redirect URI`.

**Onde obter/configurar:** Spotify Developer Dashboard → *Settings* → *Redirect URIs* → adicione a URI exata que você usará.

**Exemplo (desenvolvimento local):**

```env
SPOTIFY_REDIRECT_URI=http://localhost:8080/callback
```

**Exemplo (produção no Streamlit Cloud):**

```env
SPOTIFY_REDIRECT_URI=https://seuapp.streamlit.app/
```

**O que acontece se ausente:** o fluxo OAuth não consegue completar o handshake e o token nunca é gerado.

---

### YTMUSIC_CLIENT_ID e YTMUSIC_CLIENT_SECRET

Credenciais OAuth de um cliente do tipo **TVs e dispositivos com entrada limitada**, criado no Google Cloud Console. Habilitam o botão **Conectar ao YouTube Music** na tela de login — veja o passo a passo em [YouTube Music (experimental)](../getting-started/youtube-music.md).

**O que acontece se ausente:** nada quebra. O botão de conectar ao YouTube Music simplesmente não aparece; o app funciona normalmente só com Spotify.

---

## Configuração em produção

Em produção, o app roda no Streamlit Community Cloud, que não tem `.env`. As credenciais ficam em **Settings → Secrets**, no formato `.toml`:

```toml
[spotify]
client_id = "seu_client_id_aqui"
client_secret = "seu_client_secret_aqui"
redirect_uri = "https://seuapp.streamlit.app/"

# Opcional
[ytmusic]
client_id = "seu_ytmusic_client_id_aqui"
client_secret = "seu_ytmusic_client_secret_aqui"
```

O código lê primeiro `st.secrets['spotify']`/`st.secrets['ytmusic']`; se não existir (por exemplo, rodando localmente sem `secrets.toml`), cai para a variável de ambiente / `.env` correspondente. Veja o passo a passo completo em [Deploy no Streamlit Cloud](../deploy/streamlit-cloud.md).

---

## Fallback de credenciais

!!! note "Ordem de precedência"
    O app tenta ler cada credencial primeiro de `st.secrets['spotify']`, depois da variável de ambiente (`.env` local). Se nenhuma das duas existir, a aplicação não inicia o fluxo OAuth.

---

!!! danger "Nunca comite o arquivo .env"
    O arquivo `.env` contém o `SPOTIFY_CLIENT_SECRET`, que dá acesso completo ao seu Spotify App. Ele já está listado no `.gitignore`, mas fique atento ao usar `git add .` ou ao configurar novos ambientes — verifique sempre se o `.env` aparece no `git status` antes de commitar.

    Se o secret vazar para um repositório público, revogue-o imediatamente no [Spotify Developer Dashboard](https://developer.spotify.com/dashboard) e gere um novo.
