# Rodando localmente

## Iniciando o app

Com o ambiente virtual ativado e as variáveis de ambiente configuradas no `.env`, inicie o Streamlit:

```bash
streamlit run app.py
```

O app ficará disponível em:

```
http://localhost:8501
```

## Primeiro login

No primeiro acesso, o Soundblend não encontra token na sessão e inicia o fluxo OAuth com o Spotify.

**Fluxo passo a passo:**

1. O app detecta a ausência de token em `st.session_state`
2. A interface exibe o botão **"Conectar ao Spotify"**
3. O clique no botão abre a página de autorização do Spotify no navegador
4. O usuário revisa e autoriza os scopes solicitados (leitura de biblioteca, modificação de playlists, etc.)
5. O Spotify redireciona para a `SPOTIFY_REDIRECT_URI` configurada, com o parâmetro `?code=` na URL
6. O app captura o código de autorização e o troca por um token de acesso
7. O token é salvo em `st.session_state`, isolado por sessão de navegador
8. O app recarrega já autenticado e exibe as abas da interface principal

Nas sessões seguintes (mesma aba/navegador), o token é lido diretamente da sessão e renovado automaticamente quando expirado. Fechar a aba ou reiniciar o app perde o token — é necessário logar de novo.

!!! warning "redirect_uri deve ser idêntico ao cadastrado no Spotify Dashboard"
    O valor de `SPOTIFY_REDIRECT_URI` no `.env` precisa ser **exatamente igual** ao que está registrado no [Spotify Developer Dashboard](https://developer.spotify.com/dashboard) — incluindo protocolo, host, porta e caminho. Qualquer diferença (ex: `http` vs `https`, porta a mais ou a menos, barra final) resulta em erro `INVALID_CLIENT: Invalid redirect URI` e o fluxo OAuth falha sem autenticar.

    Valor padrão usado na configuração base:
    ```
    SPOTIFY_REDIRECT_URI=http://localhost:8080/callback
    ```

## Resolução de problemas comuns

### redirect_uri não bate

**Sintoma:** Spotify retorna `INVALID_CLIENT: Invalid redirect URI` após autorizar.

**Solução:**

1. Acesse o [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Selecione o seu app
3. Vá em **Settings** > **Redirect URIs**
4. Confirme que o valor cadastrado é idêntico ao valor de `SPOTIFY_REDIRECT_URI` no `.env`
5. Salve as alterações no Dashboard e reinicie o app

### Credenciais inválidas

**Sintoma:** Erro `401 Unauthorized` ou `INVALID_CLIENT` ao tentar autenticar.

**Solução:**

1. Acesse o [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Copie novamente o **Client ID** e o **Client Secret** do seu app
3. Verifique o `.env` na raiz do projeto:

```env
SPOTIFY_CLIENT_ID=seu_client_id_aqui
SPOTIFY_CLIENT_SECRET=seu_client_secret_aqui
SPOTIFY_REDIRECT_URI=http://localhost:8080/callback
```

4. Certifique-se de que não há espaços extras, aspas ou quebras de linha nos valores
5. Reinicie o app após corrigir o `.env`

### Token corrompido ou expirado manualmente

Se o token tiver sido revogado no Spotify ou parar de funcionar, use o botão **Sair** na interface (limpa a sessão) e refaça o login. Como o token vive só em `st.session_state`, um simples reload da página com sessão nova também resolve.
