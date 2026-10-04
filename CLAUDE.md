# Contexto do Projeto — Portfolio Armando Netto

## O que e este projeto

Portfolio pessoal publicado em armandonetto.com. Backend em Python (FastAPI) e frontend em
React com TypeScript (Vite). A primeira versao era em MkDocs (Material); foi removida em
out/2026 e continua no historico do git (commit `00ae06a` e anteriores).

Paginas: inicio (apresentacao, foto, links), projetos (repositorios publicos do GitHub, com busca
e filtros) e blog (posts como discussoes do GitHub, com comentarios pelo giscus).

A documentacao tecnica de cada projeto fica no repositorio do proprio projeto. O portfolio so
apresenta (a pagina de projetos vem do GitHub, sem texto escrito aqui).

## Stack

- Backend: FastAPI, httpx, pytest (`backend/`)
- Frontend: React 19, TypeScript, Vite, react-router, react-markdown, oxlint (`frontend/`)
- Fontes: Newsreader (texto) e Inter (rotulos), pelo pacote `@fontsource-variable`
- Container: Dockerfile em duas etapas (compila o frontend, o backend serve tudo)
- Imagem: GitHub Actions compila para ARM64 e publica em `ghcr.io/armandonettox/portfolio`
- Servidor: VM pessoal da Oracle (Ubuntu, ARM64), Podman (quadlet) atras do nginx e do Cloudflare
- Comentarios: giscus, ligado ao repositorio `armandonettox/blog`

## Arquitetura

```
backend/app/main.py         rotas da API, sitemap e entrega do site compilado
backend/app/github.py       projetos publicos do GitHub (cache de 1 hora, lista de escondidos)
backend/app/discussions.py  posts das discussoes do GitHub (cache de 10 minutos)
backend/app/seo.py          titulo, meta tags e dados estruturados de cada pagina
backend/content/            github.json (repos escondidos) e blog.json (ids do repo e da categoria)
frontend/src/pages/         Home, Projects, Posts, PostPage (cada uma com seu CSS quando precisa)
frontend/src/components/    AnimatedName, TechFloat, SiteNav, ThemeToggle, Comments, TagList
frontend/src/index.css      paleta, tema claro/escuro (data-theme) e estilos globais
```

Pontos que nao sao obvios:
- O backend escreve as meta tags de cada pagina no `index.html` (marcador
  `<meta name="seo-head">`), porque o LinkedIn e o Google nao executam JavaScript.
- Posts: so viram post as discussoes da categoria Posts escritas pelo dono do repo. A primeira
  linha pode ser `<!-- data: AAAA-MM-DD -->` para mostrar uma data original (o GitHub nao deixa
  mudar a data de criacao). O GitHub nao mostra comentarios HTML.
- O backend precisa de `GITHUB_TOKEN` (leitura de repositorios publicos) para listar discussoes,
  porque a API GraphQL exige autenticacao. No servidor ele fica em um arquivo de variaveis fora do
  git e fora da imagem. Sem ele, os projetos funcionam e os posts respondem 503.
- Arquivo que nao existe (robots.txt, imagem...) responde 404 de verdade; so rota sem extensao
  cai no `index.html` do React Router.

## Paleta e visual

Navy como cor de destaque, nunca verde (decisao do usuario em out/2026).

| Papel | Claro | Escuro |
|-------|-------|--------|
| Fundo | `#f8f9fa` | `#111111` |
| Superficie | `#ffffff` | `#0f1a2e` |
| Texto | `#171717` | `#f1f5f9` |
| Apagado | `#6b7280` | `#94a3b8` |
| Borda | `#d9e2ec` | `#1f3358` |
| Destaque | `#1e3a6b` | `#8fb0e8` |

Logos de tecnologias (Python, TypeScript, PostgreSQL) mantem as cores oficiais de marca.
Visual editorial, sem cara de template: serifa no texto, monoespacada nos caminhos do menu e
nos rotulos, sem gradientes nem emojis.

## Conteudo publico

- A home nao cita empregador nem cargo de lideranca (decisao do usuario). Isso inclui os dados
  estruturados (`seo.py`): sem `worksFor`.
- Texto dos posts e da home e do usuario: nao reescrever sem pedir, e sem travessoes nem frases de
  efeito.

## Publicacao

- Push em `main` que mexe em `backend/`, `frontend/` ou `Dockerfile` dispara
  `.github/workflows/publish-image.yml`, que publica a imagem.
- A VM atualiza sozinha: o timer `portfolio-refresh.timer` (a cada 5 minutos) baixa a imagem e,
  se mudou, reinicia so o `portfolio.service`, espera `/api/health` e volta para a versao anterior
  se a nova nao ficar saudavel. Os arquivos estao em `deploy/`. Depois de um push, esperar ate
  uns 7 minutos antes de testar o site no ar.
- Nao mexer em containers, servicos ou timers de outros projetos na VM (Hera, Hermes, Verbo): o
  script do portfolio so conhece o `portfolio`. O nginx do servidor tambem serve o Hera e o Hermes;
  sempre rodar `nginx -t` antes de recarregar.
- A origem exige o certificado do Cloudflare (acesso direto ao IP responde 400, como no Hera).
- O Cloudflare guarda arquivos estaticos por 4 horas: depois de mudar um arquivo estatico, limpar
  o cache dele no painel.
- Push usa a conta pessoal `armandonettox`; a conta ativa do `gh` neste notebook e a da empresa.

## Skills disponiveis

Use digitando `/nome` no Claude Code (arquivos em `.claude/commands/`):

| Comando | O que faz |
|---------|-----------|
| `/revisar-arquitetura` | Analisa a arquitetura do projeto inteiro ou de um arquivo especifico |
| `/revisar-bugs` | Varre o projeto em busca de bugs e comportamentos inesperados |
| `/revisar-morto` | Identifica codigo, variaveis, funcoes e arquivos que nao sao mais usados |

`/nova-pagina-projeto` ainda existe em `.claude/commands/`, mas e do MkDocs e nao serve mais.

## Comentarios no codigo

- Comentarios devem ser simples, sem caracteres especiais como `──`, `→`, `—` ou acentos
- Escrever como se um humano tivesse digitado normalmente, sem formatacao decorativa

## Commits

Formato obrigatorio: tipo(escopo): descricao
Exemplos: feat(frontend): adiciona busca na pagina de projetos
          fix(backend): aceita HEAD e responde 404 para arquivos inexistentes

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
