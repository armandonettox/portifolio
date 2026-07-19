# Contexto do Projeto — Portfolio Armando Netto

## O que e este projeto

Portfolio pessoal publicado em armandonetto.com.
Visual minimalista inspirado no site de Dario Amodei (darioamodei.com), construido em cima do
chrome nativo do Material for MkDocs (cabecalho, abas, sidebar, busca) em vez de tentar imitar
um SPA escondendo o tema — tentativa anterior de esconder o chrome foi revertida por nao agradar.
Migrado de HTML/CSS/JS puro para MkDocs em 2026.

E tambem a unica fonte de documentacao dos meus projetos: cada projeto (soundblend, verbo, etc.)
tem sua documentacao completa aqui, em `docs/projetos/<slug>/`. O README de cada projeto so
descreve objetivamente o que ele faz e linka pra ca — nao duplica a documentacao.

## Stack

- MkDocs + Material for MkDocs (chrome nativo, paleta e tipografia customizadas via CSS override)
- Plugin `blog` do Material para o blog (`docs/blog/posts/`)
- GitHub Pages + GitHub Actions (deploy automatico a cada push em main)
- Fonte: Newsreader (Google Fonts)
- Cloudflare DNS para dominio customizado

## Arquitetura

Site estatico gerado pelo MkDocs a partir de arquivos Markdown em `docs/`.
Conteudo manual — sem integracao com API do GitHub.

Estrutura principal:
- `docs/index.md` — home (so a bio; sem chrome customizado, usa o template padrao do Material)
- `docs/projetos/index.md` — lista de projetos com link pra cada um
- `docs/projetos/<slug>/` — documentacao completa de cada projeto (uma pasta por projeto,
  estrutura tipica: `index.md` + `getting-started/` + `reference/`, ver `/nova-pagina-projeto`)
- `docs/blog/posts/*.md` — posts do blog (plugin `blog` gera o index automaticamente)
- `docs/competencias.md`, `docs/experiencia.md`, `docs/contato.md` — paginas proprias com abas
  horizontais no topo (`navigation.tabs`)
- `docs/stylesheets/extra.css` — paleta an-light/an-dark (conjunto completo de variaveis `--md-*`,
  nao so as principais — variaveis derivadas como `--md-typeset-color` "congelam" se so as
  variaveis base forem sobrescritas), componentes `pf-*` (bio, listas, skills, experiencia)
- `docs/javascripts/extra.js` — JS das paginas (saudacao da home, botao copiar e-mail do contato),
  registrado via `extra_javascript`; usa `document$` do Material porque com `navigation.instant`
  o `DOMContentLoaded` so dispara no primeiro carregamento
- `overrides/main.html` — extrahead com fonte Newsreader, Open Graph com `assets/og-image.png`
  (imagem social dedicada 1200x630), remove o footer padrao do Material,
  fixa o `<title>` da aba em "Armando Netto" pra toda pagina (bloco `htmltitle`)
- `mkdocs.yml` — tema, palette, nav aninhado (primeira aba chama "Sobre"), plugins,
  extensoes markdown
- `.github/workflows/deploy.yml` — build (`mkdocs build --strict`) e deploy automatico

## Paleta de cores e chrome

Esquemas custom `an-light` e `an-dark` no `extra.css`, com o conjunto completo de variaveis do
Material (nao so `--md-default-fg-color`/`--md-default-bg-color`) para evitar variaveis derivadas
congeladas no valor errado.

```css
/* an-light */
--md-default-bg-color: #f0eee6;
--md-default-fg-color: #1f1e1d;
--md-accent-fg-color:  #4a67b5;
--md-primary-fg-color: #4a67b5;   /* fundo do cabecalho/abas, mesmo tom nos dois modos */
--md-primary-bg-color: #ffffff;   /* texto do cabecalho/abas */
--md-typeset-color:    #4a67b5;   /* corpo do texto */

/* an-dark */
--md-default-bg-color: #1f1e1d;
--md-default-fg-color: #f0eee6;
--md-accent-fg-color:  #6b85c4;
--md-primary-fg-color: #4a67b5;
--md-primary-bg-color: #ffffff;
--md-typeset-color:    #6b85c4;
```

Logo (`assets/logo.png`), favicon (`assets/favicon.png`) e og-image (`assets/og-image.png`)
sao gerados a partir das artes em `assets/logo-*.{png,jpeg}` (fora de `docs/`, sao os
arquivos-fonte de design). Logo e favicon ficam redimensionados pro tamanho de uso
(128px) pra nao pesar no carregamento.

O curriculo em PDF (`docs/assets/cv.pdf`) e gerado por `assets/build_cv.py` (reportlab);
rodar `python assets/build_cv.py` na raiz apos qualquer mudanca de conteudo. Os fontes do CV
(`build_cv.py`, `cv-src.html`) ficam fora de `docs/` de proposito, pra nao serem publicados
no site.

## Dark mode

Gerenciado nativamente pelo Material for MkDocs (bloco `palette:` no mkdocs.yml).
Toggle no cabecalho; persistencia automatica em localStorage (chave `__palette`).
Sem JS proprio para dark mode.

## Controle de conteudo

Todo o conteudo e manual:
- Projetos: usar a skill `/nova-pagina-projeto` — cria a pasta em `docs/projetos/<slug>/`,
  atualiza o `nav:` do `mkdocs.yml` e a lista em `docs/projetos/index.md`
- Blog: novo arquivo em `docs/blog/posts/`, front matter com `date:` e `categories:`.
  Categorias permitidas (enforced via `categories_allowed` no mkdocs.yml): Projetos,
  Workflow, Bastidores — o build quebra se um post usar categoria fora dessa lista
- Empregador: grafia oficial e "Best Senior" em todas as paginas e metadados
- Competencias, experiencia, contato: editar o `.md` correspondente (HTML embutido com classes
  `pf-*` pra manter a estetica)
- Bio da home: `docs/index.md`

## Deploy

- GitHub Actions: push em `main` dispara `deploy.yml`, que instala `requirements.txt`, roda
  `mkdocs build --strict` e publica o conteudo de `site/`
- Passo unico de configuracao: Settings > Pages > Source > GitHub Actions
- `docs/CNAME` contem `armandonetto.com` e e copiado para `site/CNAME` pelo MkDocs automaticamente

## Skills disponiveis

Use digitando `/nome` no Claude Code:

| Comando | O que faz |
|---------|-----------|
| `/nova-pagina-projeto` | Cria a documentacao de um projeto em `docs/projetos/<slug>/` |
| `/revisar-arquitetura` | Analisa a arquitetura do projeto inteiro ou de um arquivo especifico |
| `/revisar-bugs` | Varre o projeto em busca de bugs e comportamentos inesperados |
| `/revisar-morto` | Identifica codigo, variaveis, funcoes e arquivos que nao sao mais usados |

Os arquivos de cada skill estao em `.claude/commands/`.

## Comentarios no codigo

- Comentarios devem ser simples, sem caracteres especiais como `──`, `→`, `—` ou acentos
- Escrever como se um humano tivesse digitado normalmente, sem formatacao decorativa

## Commits

Formato obrigatorio: tipo(escopo): descricao
Exemplos: feat(projetos): adiciona pagina do netto-bot
          fix(css): corrige cor dos links no dark mode

Apos qualquer alteracao em arquivos, sugerir o commit diretamente sem perguntar antes.

## Regras

1. **Comentarios no codigo naturais e commits sem atribuicao de IA.**

2. **Fazer uma pergunta por vez, com sugestao de resposta.**

3. **Nao despejar informacao de uma vez.**

4. **Nunca pular para proxima etapa sem autorizacao.**

5. **Sempre ler o arquivo antes de editar.**

6. **Toda regra e toda skill deve ter motivacao.**

7. **Nomenclatura de arquivos e pastas: priorizar hifen como separador.**

8. **Memoria e registro de informacoes.**
   Vault do Obsidian e a unica fonte de memoria.
   Memória do projeto: `~/armandonettox/vault-armandonettox/projects/portifolio/`

9. **Manter artefatos do projeto atualizados.**
   CLAUDE.md e README.md devem refletir o estado real da stack.

10. **Seguir o modelo padrao de README.md definido pela skill `/novo-projeto`.**

## Memoria do projeto

Use `~/armandonettox/vault-armandonettox/projects/portifolio/` como memoria.
Contexto, decisoes e aprendizados sao registrados la.
Consultar antes de alteracoes significativas.
