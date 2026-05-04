# Contexto do Projeto — Portfolio Armando Netto

## O que e este projeto

Portfolio pessoal publicado em armandonetto.com.
Visual minimalista inspirado no site de Dario Amodei (darioamodei.com).

## Stack

- HTML + CSS + JavaScript puro (sem framework)
- GitHub API para busca automatica de projetos, linguagens e bio
- Fonte: Newsreader (Google Fonts)
- Deploy: GitHub Pages (repositorio armandonettox/portifolio)

## Arquitetura

Todo o site esta em um unico arquivo: `index.html`.

Estrutura do arquivo:
1. `<head>` — meta tags, fonte, CSS completo com variaveis de tema
2. `#container-principal` — pagina inicial (header, bio, projetos, competencias, experiencia, perfis, contato)
3. `#pagina-projeto` — pagina de README do projeto (oculta por padrao, exibida via JS)
4. `<script>` — dark mode, saudacao dinamica, chamadas a API do GitHub, roteamento por query param

## Paleta de cores

```css
/* Light mode (:root) */
--bg:     #f0eee6;
--text:   #1f1e1d;
--muted:  #5e5d59;
--border: #d1cfc5;
--accent: #4a67b5;

/* Dark mode (html.dark) */
--bg:     #1f1e1d;
--text:   #f0eee6;
--muted:  #87867f;
--border: #3d3d3a;
--accent: #6b85c4;
```

## Dark mode

Implementado via classe `dark` no elemento `<html>`, persistida em `localStorage`.
O toggle e um `<button>` HTML puro que alterna a classe e salva a preferencia.

## Controle de conteudo

Tudo configuravel no topo do `<script>` em `index.html`:

- `PROJETOS_CONFIG` — sobrescreve titulo/descricao ou oculta repos do GitHub (source of truth para producao)
- `ORDEM_PREFERIDA` — define quais repos aparecem primeiro
- Experiencia e competencias estao hardcoded no HTML

## GitHub API

- Endpoint repos: GET /users/{usuario}/repos
- Endpoint linguagens: GET /repos/{usuario}/{repo}/languages
- Endpoint readme: GET /repos/{usuario}/{repo}/readme
- Sem token — limite de 60 req/hora (suficiente para portfolio)
- Sem cache no lado servidor — browser faz cache natural via HTTP

## Deploy

- Plataforma: GitHub Pages (repositorio armandonettox/portifolio)
- O arquivo `index.html` na raiz e o que e publicado
- Dominio customizado: armandonetto.com (configurado via DNS)

## Skills disponiveis

Use digitando `/nome` no Claude Code:

| Comando | O que faz |
|---------|-----------|
| `/revisar-arquitetura` | Analisa a arquitetura do projeto inteiro ou de um arquivo especifico |
| `/revisar-bugs` | Varre o projeto em busca de bugs e comportamentos inesperados |
| `/revisar-morto` | Identifica codigo, variaveis, funcoes e arquivos que nao sao mais usados |

Os arquivos de cada skill estao em `.claude/commands/`.

## Commits

Formato obrigatorio: tipo(escopo): descricao
Exemplos: feat(portfolio): adiciona secao de contato
          fix(css): corrige cor dos links no dark mode

Apos qualquer alteracao em arquivos, sugerir o commit diretamente sem perguntar antes se o usuario quer a sugestao.
