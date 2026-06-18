# Contexto do Projeto — Portfolio Armando Netto

## O que e este projeto

Portfolio pessoal publicado em armandonetto.com.
Visual minimalista inspirado no site de Dario Amodei (darioamodei.com).
Migrado de HTML/CSS/JS puro para MkDocs em 2026.

## Stack

- MkDocs + Material for MkDocs (tema customizado com CSS override)
- GitHub Pages + GitHub Actions (deploy automatico a cada push em main)
- Fonte: Newsreader (Google Fonts)
- Cloudflare DNS para dominio customizado

## Arquitetura

Site estatico gerado pelo MkDocs a partir de arquivos Markdown em `docs/`.
Conteudo manual — sem integracao com API do GitHub.

Estrutura principal:
- `docs/index.md` — home (bio, projetos, competencias, experiencia, perfis, contato)
- `docs/projetos/*.md` — uma pagina por projeto, conteudo manual
- `docs/stylesheets/extra.css` — toda a estetica: paleta, layout 640px, componentes pf-*
- `overrides/main.html` — carrega Newsreader no head + shim de links antigos (?projeto=X)
- `mkdocs.yml` — config do tema, palette, extensoes markdown
- `.github/workflows/deploy.yml` — build e deploy automatico

## Paleta de cores

Definida como esquemas custom `an-light` e `an-dark` no `extra.css`.
As variaveis `--pf-*` sao a fonte de verdade; os tokens `--md-*` do Material apontam para elas.

```css
/* Light (an-light) */
--pf-bg:     #f0eee6;
--pf-text:   #1f1e1d;
--pf-muted:  #3a3936;
--pf-border: #d1cfc5;
--pf-accent: #4a67b5;

/* Dark (an-dark) */
--pf-bg:     #1f1e1d;
--pf-text:   #f0eee6;
--pf-muted:  #87867f;
--pf-border: #3d3d3a;
--pf-accent: #6b85c4;
```

## Dark mode

Gerenciado nativamente pelo Material for MkDocs (bloco `palette:` no mkdocs.yml).
Toggle na barra superior; persistencia automatica em localStorage (chave `__palette`).
Sem JS proprio para dark mode.

## Controle de conteudo

Todo o conteudo e manual:
- Projetos: editar arquivos em `docs/projetos/` e o `nav:` no `mkdocs.yml`
- Bio, competencias, experiencia: editar `docs/index.md` (HTML embutido com classes pf-*)
- Perfis e contato: editar `docs/index.md`

## Deploy

- GitHub Actions: push em `main` dispara `deploy.yml` que roda `mkdocs build --strict` e publica
- Passo unico de configuracao: Settings > Pages > Source > GitHub Actions
- `docs/CNAME` contem `armandonetto.com` e e copiado para `site/CNAME` pelo MkDocs automaticamente

## Skills disponiveis

Use digitando `/nome` no Claude Code:

| Comando | O que faz |
|---------|-----------|
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
