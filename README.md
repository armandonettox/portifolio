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

Portfolio pessoal com visual minimalista inspirado no site de Dario Amodei. Conteudo escrito
em Markdown puro — projetos, bio, competencias e experiencia sao mantidos manualmente.

Acesse em: [armandonetto.com](https://armandonetto.com)

## Forma de entrega

Site estatico gerado pelo MkDocs e publicado via GitHub Pages com dominio customizado.

## Stack

- MkDocs + Material for MkDocs
- GitHub Pages + GitHub Actions (deploy automatico a cada push em main)
- Fonte Newsreader (Google Fonts)
- Cloudflare DNS para dominio customizado

## Estrutura do projeto

```
portifolio/
    mkdocs.yml              <- config principal do MkDocs
    requirements.txt        <- dependencias Python do build
    .python-version         <- versao do Python
    docs/
        index.md            <- pagina inicial (bio, projetos, competencias, experiencia)
        CNAME               <- dominio customizado para o GitHub Pages
        404.md              <- pagina de erro
        projetos/           <- uma pagina por projeto
            netto-bot.md
            netto-malware.md
            portifolio.md
        stylesheets/
            extra.css       <- estilos customizados (paleta, layout, componentes pf-*)
        assets/
            favicon.svg     <- favicon SVG do site
    overrides/
        main.html           <- carrega Newsreader e shim de links ?projeto=X
    .github/
        workflows/
            deploy.yml      <- build MkDocs e deploy no GitHub Pages
```

## Instalacao

### Rodar localmente

```bash
git clone https://github.com/armandonettox/portifolio.git
cd portifolio
pip install -r requirements.txt
mkdocs serve
```

Acesse em `http://127.0.0.1:8000`.

### Deploy (automatico)

Qualquer push na branch `main` dispara o workflow `deploy.yml`, que gera o site com
`mkdocs build` e publica no GitHub Pages.

Passo unico (feito uma vez): em Settings > Pages > Source, selecionar **GitHub Actions**.

## Configuracao

### Adicionar ou editar um projeto

Crie ou edite um arquivo em `docs/projetos/<nome>.md`. Adicione a entrada no `nav:` do
`mkdocs.yml` para que apareca na navegacao.

### Editar bio, competencias ou experiencia

Edite `docs/index.md` diretamente — todo o conteudo esta escrito como HTML embutido com
as classes `.pf-*` do `extra.css`.

## Como usar

1. Edite o Markdown em `docs/` conforme necessario
2. `git push` dispara o deploy automatico
3. Acesse armandonetto.com

## Output

Site publicado em armandonetto.com com:
- Pagina inicial: bio, projetos, competencias, experiencia, perfis e contato
- Pagina individual por projeto
- Dark/light mode nativo (toggle do Material, persistido em localStorage)
- Meta tags de SEO e Open Graph
- Pagina de erro 404

## Funcionamento

### Dark mode

Gerenciado nativamente pelo Material for MkDocs. O toggle na barra superior alterna entre
os esquemas `an-light` e `an-dark`, definidos em `docs/stylesheets/extra.css`.
A preferencia e persistida automaticamente em localStorage.

### Layout

O CSS em `extra.css` sobrescreve o tema Material para virar uma coluna unica de 640px,
sem sidebars, sem footer de docs e sem barra de busca. A estetica (tipografia, paleta e
componentes `.pf-*`) e portada do site anterior (HTML/CSS puro).

### Links antigos

O shim em `overrides/main.html` redireciona links no formato `?projeto=X` (formato do
site anterior) para `/projetos/X/` automaticamente.

## Adaptacao

Para usar como base para seu proprio portfolio:

1. Clone o repositorio
2. Edite `mkdocs.yml`: `site_name`, `site_url`, `site_description`
3. Substitua o conteudo de `docs/index.md` com seus dados
4. Adicione seus projetos em `docs/projetos/`
5. Atualize `docs/CNAME` com seu dominio
6. Aponte o DNS do seu dominio para o GitHub Pages

## Erros comuns

| Erro | Causa | Solucao |
|------|-------|---------|
| `mkdocs build --strict` falha com link quebrado | Pagina referenciada no nav nao existe | Criar o arquivo .md correspondente em docs/ |
| Fonte Newsreader nao carrega localmente | Bloqueio de rede ou offline | Normal em ambiente sem internet; cai para Georgia |
| Dominio custom some apos deploy | CNAME nao esta em docs/ | Garantir que docs/CNAME existe e contem o dominio |
| Dark mode nao persiste | Cache do browser | Limpar localStorage e testar novamente |

## Status

Em producao — [armandonetto.com](https://armandonetto.com)
