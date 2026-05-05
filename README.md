# Portfolio — Armando Netto

Portfolio pessoal com visual minimalista inspirado no site de Dario Amodei.

Acesse em: [armandonetto.com](https://armandonetto.com)

## Filosofia

O objetivo deste portfolio e gastar o minimo de tempo possivel em manutencao para sobrar tempo para criar novos projetos. Por isso, a maior parte do conteudo e puxada automaticamente da API do GitHub — basta fazer um novo repo publico e ele aparece aqui sozinho, com linguagens, estrelas e data de atualizacao. A bio tambem vem do README do perfil do GitHub. Na pratica, o portfolio se atualiza sozinho conforme voce trabalha.

## O que e automatico

- **Bio** — lida do README do repo especial `usuario/usuario` no GitHub
- **Lista de projetos** — todos os repos publicos nao-fork do usuario
- **Linguagens de cada projeto** — buscadas via API por repo
- **Estrelas** — campo `stargazers_count` de cada repo
- **Tempo de atualizacao** — campo `pushed_at` de cada repo

## O que e manual (hardcoded no HTML)

- Secao de experiencia (empresas, cargos, periodos)
- Secao de competencias (linguagens e ferramentas)
- Perfis e contato

## Stack

- HTML + CSS + JavaScript puro, sem framework
- GitHub API para busca automatica de projetos, linguagens e bio
- marked.js para renderizacao de README em Markdown
- Fonte Newsreader (Google Fonts)
- Deploy: Netlify com funcao serverless como proxy da GitHub API
- Dominio customizado via Cloudflare DNS

## Funcionalidades

- Dark/light mode com toggle persistido em localStorage
- Saudacao dinamica (bom dia/boa tarde/boa noite) pelo horario de Brasilia
- Projetos buscados automaticamente da API do GitHub com controle manual de visibilidade
- Linguagens de cada projeto exibidas como tags estilizadas
- Ordenacao automatica de projetos por estrelas
- Tempo de atualizacao relativo por projeto (ex: "ha 3 dias")
- Contagem de estrelas por projeto
- Secao de competencias com tags por categoria
- Secao de experiencia com timeline
- Pagina de README por projeto com roteamento via query param
- Favicon SVG customizado
- Cache de chamadas a API com sessionStorage
- Pagina de erro 404 customizada
- Meta tags de SEO e Open Graph (preview no WhatsApp, LinkedIn e Google)
- Animacao de fade-in suave ao carregar

---

## Como criar o seu proprio

Voce pode usar este repositorio como base para o seu proprio portfolio. O processo completo esta descrito abaixo.

### 1. Fork ou clone o repositorio

```bash
git clone https://github.com/armandonettox/portifolio.git meu-portfolio
cd meu-portfolio
```

### 2. Configure o seu usuario do GitHub

No topo do `<script>` em `index.html`, troque o valor da variavel `USUARIO`:

```javascript
const USUARIO = 'seu-usuario-aqui';
```

A partir dai, todos os repos publicos do seu perfil aparecerao automaticamente.

### 3. Crie um README de perfil no GitHub

Crie um repositorio com o mesmo nome do seu usuario (ex: `github.com/seu-usuario/seu-usuario`). O README desse repo e exibido como bio no portfolio. Escreva dois paragrafos descritivos — o portfolio vai exibir os dois primeiros automaticamente.

### 4. Controle quais projetos aparecem

No topo do script, use `PROJETOS_CONFIG` para ocultar repos ou sobrescrever titulos e descricoes:

```javascript
const PROJETOS_CONFIG = {
    'nome-do-repo':    { ocultar: true },
    'outro-repo':      { titulo: 'Titulo customizado', descricao: 'Descricao customizada' },
};
```

Use `ORDEM_PREFERIDA` para fixar alguns projetos no topo da lista:

```javascript
const ORDEM_PREFERIDA = ['projeto-destaque', 'outro-projeto'];
```

### 5. Atualize o conteudo manual

No proprio `index.html`, edite diretamente as secoes:

- **Experiencia** — bloco com classe `pf-exp-list`
- **Competencias** — bloco com classe `pf-skills`
- **Perfis e contato** — blocos com `pf-section-title` correspondente

### 6. Atualize as meta tags

No `<head>` do `index.html`, atualize as meta tags com o seu nome e descricao:

```html
<meta name="description" content="Portfolio de Seu Nome — ...">
<meta property="og:title" content="Seu Nome">
<meta property="og:url" content="https://seudominio.com">
```

---

## Deploy com Netlify

O Netlify e a plataforma de deploy usada por este portfolio. Ele serve o site estatico e tambem executa uma funcao serverless que faz proxy das chamadas a GitHub API — isso e necessario para esconder o token do GitHub e evitar o limite de 60 requisicoes por hora da API publica.

### Por que usar uma funcao serverless?

A GitHub API tem limite de 60 requisicoes por hora para chamadas sem autenticacao. Com um token, o limite sobe para 5.000 por hora. Porem, o token nao pode ficar exposto no codigo do frontend (qualquer um poderia ve-lo). A solucao e criar uma funcao serverless no Netlify que recebe a requisicao do browser, adiciona o token no cabecalho e repassa para a API do GitHub. O token fica salvo apenas nas variaveis de ambiente do Netlify, fora do repositorio.

### Passo a passo

**1. Crie uma conta no Netlify**

Acesse [netlify.com](https://netlify.com) e conecte com o seu GitHub.

**2. Importe o repositorio**

No painel do Netlify, clique em "Add new site" > "Import an existing project" e selecione o repositorio do portfolio. O Netlify detecta automaticamente que e um site estatico e configura o deploy.

**3. Gere um token no GitHub**

Acesse [github.com/settings/tokens](https://github.com/settings/tokens), clique em "Generate new token (classic)" e selecione apenas o escopo `public_repo`. Copie o token gerado — voce so ve ele uma vez.

**4. Configure a variavel de ambiente no Netlify**

No painel do Netlify, va em Site settings > Environment variables e adicione:

```
GITHUB_TOKEN = ghp_seu_token_aqui
```

**5. A funcao serverless**

O arquivo `netlify/functions/github.js` ja esta pronto no repositorio. Ele le o caminho da requisicao via query param `path`, chama a GitHub API com o token e retorna o resultado. Voce nao precisa alterar nada.

**6. Dominio customizado (opcional)**

No painel do Netlify, va em Domain management > Add a domain e adicione o seu dominio. O Netlify gera um certificado SSL automaticamente via Let's Encrypt. Se o seu DNS estiver no Cloudflare, aponte um registro CNAME para o dominio do Netlify (ex: `seu-site.netlify.app`) e desative o proxy do Cloudflare (icone laranja) para que o Netlify consiga emitir o certificado.

### Estrutura de arquivos necessaria para o Netlify

```
portifolio/
    index.html
    404.html
    netlify/
        functions/
            github.js
```

O `404.html` na raiz e detectado automaticamente pelo Netlify e exibido quando uma rota nao existe.

---

## Como rodar localmente

**1. Clone o repositorio**
```bash
git clone https://github.com/armandonettox/portifolio.git
cd portifolio
```

**2. Abra o arquivo no browser**

Abra o `index.html` diretamente no browser. Para que a busca de projetos funcione localmente, rode um servidor local simples:

```bash
npx serve .
```

Ou use a extensao Live Server no VS Code / Cursor.

> As chamadas a GitHub API passam pela funcao Netlify em producao. Localmente, os projetos nao vao carregar sem um servidor configurado com a variavel GITHUB_TOKEN.

---

## Estrutura

```
portifolio/
    index.html                  <- unico arquivo do site
    404.html                    <- pagina de erro customizada
    netlify/
        functions/
            github.js           <- proxy serverless para a GitHub API
    assets/
        favicon.svg             <- favicon SVG do site
        logos/                  <- logos e imagens
```

## Status

Em producao — [armandonetto.com](https://armandonetto.com)
