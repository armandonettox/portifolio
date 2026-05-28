# Portfolio — Armando Netto

## Indice

- [Objetivo](#objetivo)
- [Forma de entrega](#forma-de-entrega)
- [Stack](#stack)
- [Estrutura do projeto](#estrutura-do-projeto)
- [Instalacao](#instalacao)
- [Configuracao](#configuracao)
- [Como usar](#como-usar)
- [Output](#output)
- [Funcionamento](#funcionamento)
- [Adaptacao](#adaptacao)
- [Erros comuns](#erros-comuns)

## Objetivo

Portfolio pessoal com visual minimalista inspirado no site de Dario Amodei. O objetivo e gastar o minimo de tempo possivel em manutencao para sobrar tempo para criar novos projetos. A maior parte do conteudo e puxada automaticamente da API do GitHub — basta criar um novo repo publico que ele aparece sozinho, com linguagens, estrelas e data de atualizacao. A bio tambem vem do README do perfil do GitHub.

Acesse em: [armandonetto.com](https://armandonetto.com)

## Forma de entrega

Site estatico publicado via Netlify com dominio customizado.

## Stack

- HTML + CSS + JavaScript puro (sem frameworks)
- GitHub API para busca automatica de projetos, linguagens e bio
- marked.js para renderizacao de README em Markdown
- Netlify com funcao serverless como proxy da GitHub API
- Cloudflare DNS para dominio customizado
- Fonte Newsreader (Google Fonts)

## Estrutura do projeto

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

## Instalacao

### Rodar localmente

```bash
git clone https://github.com/armandonettox/portifolio.git
cd portifolio
```

Abra o `index.html` diretamente no browser ou use um servidor local:

```bash
npx serve .
```

Ou use a extensao Live Server no VS Code / Cursor.

> As chamadas a GitHub API passam pela funcao Netlify em producao. Localmente, os projetos nao vao carregar sem um servidor configurado com a variavel GITHUB_TOKEN.

### Deploy no Netlify

1. Crie uma conta no Netlify e conecte com seu GitHub
2. Importe o repositorio (o Netlify detecta automaticamente que e um site estatico)
3. Gere um token no GitHub em `github.com/settings/tokens` com escopo `public_repo`
4. No painel do Netlify, va em Site settings > Environment variables e adicione `GITHUB_TOKEN`
5. Configure dominio customizado em Domain management > Add a domain

## Configuracao

### Usuario do GitHub

No topo do `<script>` em `index.html`, troque o valor da variavel `USUARIO`:

```javascript
const USUARIO = 'seu-usuario-aqui';
```

### Controle de projetos

Use `PROJETOS_CONFIG` para ocultar repos ou sobrescrever titulos e descricoes:

```javascript
const PROJETOS_CONFIG = {
    'nome-do-repo':    { ocultar: true },
    'outro-repo':      { titulo: 'Titulo customizado', descricao: 'Descricao customizada' },
};
```

Use `ORDEM_PREFERIDA` para fixar projetos no topo da lista:

```javascript
const ORDEM_PREFERIDA = ['projeto-destaque', 'outro-projeto'];
```

### Conteudo manual

No `index.html`, edite diretamente as secoes:
- **Experiencia** — bloco com classe `pf-exp-list`
- **Competencias** — bloco com classe `pf-skills`
- **Perfis e contato** — blocos com `pf-section-title` correspondente

## Como usar

O portfolio funciona de forma automatica. Acesse armandonetto.com para:

1. Visualizar a lista de projetos publicos do GitHub, ordenados por estrelas
2. Clicar em um projeto para ver o README completo
3. Alternar entre tema claro e escuro
4. Navegar pelas secoes de experiencia, competencias e contato

Para adicionar um novo projeto ao portfolio, basta criar um repo publico no GitHub.

## Output

Site publicado em armandonetto.com com:
- Pagina inicial com bio, projetos, competencias, experiencia e contato
- Pagina de README por projeto com roteamento via query param
- Dark/light mode com toggle persistido
- Meta tags de SEO e Open Graph para compartilhamento
- Pagina de erro 404 customizada

## Funcionamento

### Conteudo automatico

- **Bio** — lida do README do repo especial `usuario/usuario` no GitHub
- **Lista de projetos** — todos os repos publicos nao-fork do usuario
- **Linguagens de cada projeto** — buscadas via API por repo
- **Estrelas** — campo `stargazers_count` de cada repo
- **Tempo de atualizacao** — campo `pushed_at` de cada repo

### Funcionalidades

- Dark/light mode com toggle persistido em localStorage
- Saudacao dinamica (bom dia / boa tarde / boa noite) pelo horario de Brasilia
- Tags de linguagens por projeto
- Ordenacao automatica de projetos por estrelas
- Cache de chamadas a API com sessionStorage (TTL de 2 horas)
- Animacao de fade-in suave ao carregar
- Scroll suave com CSS (scroll-behavior: smooth)

### Proxy da GitHub API

A funcao serverless em `netlify/functions/github.js` recebe a requisicao do browser com o path da API, adiciona o token GITHUB_TOKEN no cabecalho e faz a chamada real a GitHub API. Isso evita expor o token no frontend e aumenta o limite de 60 req/h para 5000 req/h.

### Controle de visibilidade

Tudo configuravel no topo do `<script>` em `index.html`:
- `PROJETOS_CONFIG` — sobrescreve titulo/descricao ou oculta repos
- `ORDEM_PREFERIDA` — define quais repos aparecem primeiro
- Experiencia e competencias estao hardcoded no HTML

## Adaptacao

Para usar este repositorio como base para seu proprio portfolio:

1. Clone ou fork o repositorio
2. Crie um README de perfil no GitHub (repo com mesmo nome do usuario)
3. Atualize a variavel `USUARIO` no topo do script em `index.html`
4. Configure `PROJETOS_CONFIG` e `ORDEM_PREFERIDA` conforme necessario
5. Atualize as meta tags no `<head>` com seu nome e descricao
6. Faca deploy no Netlify e configure o GITHUB_TOKEN nas variaveis de ambiente
7. Aponte seu dominio via Cloudflare DNS com CNAME para o dominio Netlify

## Erros comuns

| Erro | Causa | Solucao |
|------|-------|---------|
| Projetos nao carregam localmente | Sem GITHUB_TOKEN no ambiente local | Usar npx serve e configurar variavel, ou testar em producao |
| API retorna 403 | Limite de 60 req/h excedido (sem token) | Configurar GITHUB_TOKEN no Netlify |
| Certificado SSL nao emite | Cloudflare com proxy (icone laranja) ativo | Desativar proxy do Cloudflare (icone cinza) para o CNAME do Netlify |
| Projeto aparece com titulo estranho | Nome do repo nao foi sobrescrito no PROJETOS_CONFIG | Adicionar entrada com `titulo` customizado |

## Status

Em producao — [armandonetto.com](https://armandonetto.com)
