# Migração do Portfólio para MkDocs (estático, conteúdo manual)

## Contexto

O portfólio (armandonetto.com) é hoje um único `index.html` com HTML+CSS+JS puro: um SPA
que busca projetos, bio e READMEs da API do GitHub em runtime (via Cloudflare Worker proxy),
com cache em localStorage, roteamento por `?projeto=X`, dark mode e saudação dinâmica.

O objetivo é **migrar para MkDocs mantendo a mesma ideia visual** (minimalismo estilo Dario
Amodei: coluna estreita, fonte Newsreader serifada, paleta `#f0eee6`/`#4a67b5`, dark mode),
mas **removendo a busca automática do GitHub**. Os projetos passam a ser **escritos à mão em
Markdown** (uma página por projeto); bio, competências e experiência viram conteúdo manual.

**Decisões travadas:**
- MkDocs + tema **Material for MkDocs** (com override pesado de CSS).
- **Sem** API do GitHub, **sem** Cloudflare Worker, **sem** cron, **sem** marked.js.
- Conteúdo manual em Markdown.
- **Dark mode nativo** do Material.
- Hosting continua **GitHub Pages** em `armandonettox/portifolio`, domínio **armandonetto.com**.
- Preservar a paleta atual do `index.html` (não a "Netto Code v2").
- Push somente após autorização do usuário.

---

## O que sai

- `index.html` (raiz) — o SPA inteiro
- `404.html` (raiz) — vira 404 do MkDocs
- `netlify/` (pasta inteira) — código morto
- `assets/logos/logo_an.png` e `logo_armando_netto.png` — ~6.6 MB, não referenciados

## Estrutura final

```
portifolio/
├── mkdocs.yml
├── requirements.txt                # mkdocs==1.6.1, mkdocs-material==9.6.21
├── .python-version                 # 3.12
├── docs/
│   ├── index.md                    # HOME: bio, projetos, competências, experiência, perfis, contato
│   ├── CNAME                       # armandonetto.com
│   ├── 404.md
│   ├── projetos/
│   │   ├── netto-bot.md
│   │   ├── netto-malware.md
│   │   └── portifolio.md
│   ├── stylesheets/
│   │   └── extra.css               # replica a estética Dario Amodei
│   └── assets/
│       └── favicon.svg
├── overrides/
│   └── main.html                   # Newsreader no <head> + shim ?projeto=X
└── .github/workflows/deploy.yml    # build MkDocs + deploy GitHub Pages (on push)
```

---

## mkdocs.yml

```yaml
site_name: Armando Netto
site_url: https://armandonetto.com/
site_description: Portfolio de Armando Netto — Analista de Dados.

theme:
  name: material
  custom_dir: overrides
  language: pt-BR
  font: false
  favicon: assets/favicon.svg
  features:
    - navigation.instant
    - navigation.instant.progress
  palette:
    - media: "(prefers-color-scheme: light)"
      scheme: an-light
      toggle: { icon: material/weather-sunny, name: Modo escuro }
    - media: "(prefers-color-scheme: dark)"
      scheme: an-dark
      toggle: { icon: material/weather-night, name: Modo claro }

plugins: []

extra_css:
  - stylesheets/extra.css

markdown_extensions:
  - tables
  - admonition
  - attr_list
  - md_in_html
  - pymdownx.highlight: { anchor_linenums: false }
  - pymdownx.superfences
  - pymdownx.inlinehilite
```

---

## CSS (extra.css) — estratégia

- Definir esquemas `an-light`/`an-dark` com as variáveis `--pf-*` ligadas às `--md-*` do Material.
- Paleta light: `--pf-bg:#f0eee6`, `--pf-text:#1f1e1d`, `--pf-muted:#3a3936`, `--pf-border:#d1cfc5`, `--pf-accent:#4a67b5`.
- Paleta dark: `--pf-bg:#1f1e1d`, `--pf-text:#f0eee6`, `--pf-muted:#87867f`, `--pf-border:#3d3d3a`, `--pf-accent:#6b85c4`.
- Esconder chrome do Material: sidebars, footer, header title/logo/search.
- Manter só o toggle de tema no canto superior direito (dentro do header esvaziado).
- Container 640px via `.md-grid { max-width:640px }`.
- Portar componentes `.pf-*` do index.html (linhas 134–479) trocando variáveis.
- NÃO portar o reset global `*{margin:0;padding:0}`.
- Portar media query `@media (max-width:560px)`.

---

## overrides/main.html

```html
{% extends "base.html" %}
{% block extrahead %}
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,300;0,6..72,400;0,6..72,500;1,6..72,300;1,6..72,400&display=swap" rel="stylesheet">
  <script>
    (function(){var p=new URLSearchParams(location.search).get('projeto');
     if(p){location.replace('/projetos/'+p+'/');}})();
  </script>
{% endblock %}
```

---

## Conteúdo manual — Home

Portar do index.html:
- Bio: parágrafos das linhas 498–499
- Competências: linhas 511–547
- Experiência: linhas 553–576 (Best Senior + AutoGiva)
- Perfis: linhas 582–593 (GitHub + LinkedIn)
- Contato: linha 602
- Remover saudação dinâmica (dependia de JS)

## Conteúdo manual — Projetos

Criar docs/projetos/ com páginas para os projetos públicos do GitHub:
- netto-bot.md
- netto-malware.md
- portifolio.md (este próprio site)
Cada uma: título, descrição, conteúdo resumido, link "ver no GitHub".

---

## Deploy

```yaml
name: deploy
on: { push: { branches: [main] }, workflow_dispatch: {} }
permissions: { contents: read, pages: write, id-token: write }
concurrency: { group: pages, cancel-in-progress: true }
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version-file: .python-version }
      - run: pip install -r requirements.txt
      - run: mkdocs build --strict
      - uses: actions/upload-pages-artifact@v3
        with: { path: site }
  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment: { name: github-pages, url: "${{ steps.deployment.outputs.page_url }}" }
    steps:
      - { id: deployment, uses: actions/deploy-pages@v4 }
```

Passo manual único após merge: Settings → Pages → Source → GitHub Actions.

---

## Execução e segurança

- Trabalhar em branch `feat/mkdocs` (main fica intocada; site atual continua no ar).
- Criar tag `pre-mkdocs` antes de começar.
- Cada grupo de arquivos = 1 commit descritivo.
- Push somente após autorização explícita do usuário.
- Rollback: `git revert` do merge + voltar Source para "Deploy from a branch".
