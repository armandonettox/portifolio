# Portfolio — Armando Netto

Portfolio pessoal com visual minimalista inspirado no site de Dario Amodei.

Acesse em: [armandonetto.com](https://armandonetto.com)

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
- Linguagens de cada projeto exibidas como tags
- Secao de competencias com tags por categoria
- Secao de experiencia com timeline
- Pagina de README por projeto com roteamento via query param
- Favicon SVG customizado

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

## Configuracao de conteudo

Toda a customizacao fica no topo do `<script>` em `index.html`:

| Variavel | O que controla |
|----------|----------------|
| `PROJETOS_CONFIG` | Titulo, descricao e visibilidade dos repos do GitHub |
| `ORDEM_PREFERIDA` | Ordem de exibicao dos projetos |
| `USUARIO` | Nome de usuario do GitHub para busca automatica |

Experiencia e competencias estao hardcoded no HTML, na secao correspondente.

## Estrutura

```
portifolio/
    index.html                  <- unico arquivo do site
    netlify/
        functions/
            github.js           <- proxy serverless para a GitHub API
    assets/
        favicon.svg             <- favicon do site
        logos/                  <- logos e imagens
```

## Status

Em producao — [armandonetto.com](https://armandonetto.com)
