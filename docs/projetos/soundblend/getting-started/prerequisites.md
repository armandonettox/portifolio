# Pré-requisitos

Antes de instalar e executar o Soundblend, certifique-se de que seu ambiente atende a todos os requisitos abaixo.

---

## Python

O Soundblend requer **Python 3.12 ou superior**.

Para verificar a versão instalada:

```bash
python --version
```

A saída esperada é algo como `Python 3.12.x`. Se o comando retornar uma versão anterior ou não for reconhecido, faça o download em:

- [python.org/downloads](https://www.python.org/downloads/)

!!! tip "Recomendação de ambiente virtual"
    Sempre use um ambiente virtual (`.venv`) para isolar as dependências do projeto e evitar conflitos com outros pacotes instalados globalmente.

    ```bash
    python -m venv .venv
    source .venv/bin/activate  # Linux/macOS
    .venv\Scripts\activate     # Windows
    ```

---

## Conta Spotify

É necessário ter uma conta ativa no Spotify.

- Plano **gratuito** ou **premium** funcionam normalmente.
- A conta precisa ter músicas curtidas (biblioteca) para que o Soundblend tenha dados para processar.

Crie sua conta em [spotify.com](https://www.spotify.com) caso ainda não tenha uma.

---

## Spotify App (Developer Dashboard)

O Soundblend se comunica com a API do Spotify via OAuth. Para isso, é necessário registrar um app no Spotify Developer Dashboard e obter as credenciais.

### Passo a passo

**1. Acessar o Dashboard**

Acesse [developer.spotify.com/dashboard](https://developer.spotify.com/dashboard) e faça login com sua conta Spotify.

**2. Criar um novo app**

Clique em **Create app** no canto superior direito.

**3. Preencher nome e descrição**

Preencha os campos obrigatórios:

| Campo | Exemplo |
|---|---|
| App name | Soundblend |
| App description | Organiza músicas curtidas em playlists por gênero |
| Website | *(pode deixar em branco)* |

**4. Adicionar o Redirect URI**

No campo **Redirect URIs**, adicione o endereço abaixo e clique em **Add**:

```
http://localhost:8080/callback
```

!!! warning "Atenção ao Redirect URI"
    O Redirect URI precisa ser **exatamente igual** ao valor configurado na variável de ambiente `SPOTIFY_REDIRECT_URI` do projeto. Qualquer diferença — incluindo barra no final, protocolo ou porta — causará erro de autenticação OAuth com a mensagem `INVALID_CLIENT: Invalid redirect URI`. Não use `https://` para desenvolvimento local.

**5. Selecionar APIs**

Em **Which API/SDKs are you planning to use?**, marque **Web API**.

**6. Aceitar os termos e salvar**

Marque a caixa de aceite dos termos de uso e clique em **Save**.

**7. Obter Client ID e Client Secret**

Após criar o app, você será redirecionado para a página de configurações do app. As credenciais ficam na seção **Basic Information**:

- **Client ID** — visível diretamente na página.
- **Client Secret** — clique em **View client secret** para revelar.

Guarde esses dois valores. Eles serão usados nas variáveis de ambiente `SPOTIFY_CLIENT_ID` e `SPOTIFY_CLIENT_SECRET`.

!!! danger "Não exponha suas credenciais"
    Nunca commite o `Client Secret` diretamente no código ou em arquivos versionados. Armazene sempre em um arquivo `.env` listado no `.gitignore`.

### Scopes necessários

O Soundblend solicita os seguintes scopes durante a autenticação OAuth:

| Scope | Finalidade |
|---|---|
| `user-library-read` | Ler músicas curtidas |
| `playlist-read-private` | Listar playlists privadas |
| `playlist-modify-public` | Editar playlists públicas |
| `playlist-modify-private` | Editar playlists privadas |

São apenas os escopos que o app realmente usa: ler a biblioteca e modificar playlists. O app nunca altera as músicas curtidas nem lê e-mail ou dados privados do perfil.

Esses scopes são solicitados automaticamente no fluxo OAuth na primeira execução. Não é necessário configurá-los manualmente no Dashboard.

---

## Git

Git é necessário para clonar o repositório do projeto.

Para verificar se está instalado:

```bash
git --version
```

Se não estiver instalado, faça o download em [git-scm.com](https://git-scm.com/downloads).

---

## Para deploy (opcional)

O Soundblend em produção roda no [Streamlit Community Cloud](https://share.streamlit.io), sem servidor próprio. Veja o guia de [deploy no Streamlit Cloud](../deploy/streamlit-cloud.md) para os detalhes.
