# YouTube Music (experimental)

!!! warning "Só a conexão existe por enquanto"
    O Soundblend já permite conectar uma conta do YouTube Music na tela de login, mas a organização de playlists por esse caminho ainda não foi construída — é a base para uma sincronização Spotify ↔ YouTube Music futura. Sem essa configuração, o botão de conectar simplesmente não aparece e o app funciona normalmente só com Spotify.

## Por que isso é diferente do Spotify

Não existe API pública oficial do YouTube Music. O Soundblend usa [ytmusicapi](https://ytmusicapi.readthedocs.io/), uma biblioteca que reimplementa a API interna usada pelo site, autenticando via OAuth no fluxo "TVs e dispositivos com entrada limitada" do Google — o mesmo usado por apps de TV: o app mostra um código, você autoriza numa outra aba, e a conexão se completa quando você confirma.

## Obter as credenciais

**1. Criar (ou reutilizar) um projeto no Google Cloud**

Acesse o [Google Cloud Console](https://console.cloud.google.com/) e crie um projeto, ou use um existente.

**2. Ativar a YouTube Data API v3**

No menu **APIs e serviços → Biblioteca**, procure por **YouTube Data API v3** e clique em **Ativar**.

**3. Configurar a tela de consentimento OAuth**

Em **APIs e serviços → Tela de consentimento OAuth**, configure um app do tipo **Externo** (ou Interno, se disponível na sua organização) com um nome e e-mail de contato. Não precisa de verificação do Google para uso pessoal.

**4. Criar as credenciais OAuth**

Em **APIs e serviços → Credenciais → Criar credenciais → ID do cliente OAuth**, selecione o tipo de aplicativo **TVs e dispositivos com entrada limitada**.

Guarde o **Client ID** e o **Client Secret** gerados.

!!! danger "Não exponha suas credenciais"
    Mesmo cuidado do Client Secret do Spotify: nunca commite esses valores. Use `.env` local ou `st.secrets` em produção.

## Configurar no Soundblend

**Local (`.env`):**

```env
YTMUSIC_CLIENT_ID=seu_client_id_aqui
YTMUSIC_CLIENT_SECRET=seu_client_secret_aqui
```

**Streamlit Cloud (`Settings → Secrets`):**

```toml
[ytmusic]
client_id = "seu_client_id_aqui"
client_secret = "seu_client_secret_aqui"
```

## Como funciona a conexão

1. Na tela de login, abaixo do botão do Spotify, aparece **Conectar ao YouTube Music**.
2. Ao clicar, o app mostra um código e um link para `google.com/device`.
3. Você abre o link em outra aba, digita o código e autoriza com sua conta Google.
4. De volta ao Soundblend, clica em **Verificar conexão** — o token fica só em `st.session_state`, mesma política de zero persistência do resto do app.
5. Conectado, você vê uma tela confirmando a conta e avisando que a sincronização de playlists ainda está em construção.

!!! note "API não oficial"
    Por reimplementar a API interna do YouTube Music, esse fluxo pode quebrar se o Google mudar algo internamente — é uma limitação conhecida de quem depende do ytmusicapi, não um bug do Soundblend.
