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

## Comentarios no codigo

- Comentarios devem ser simples, sem caracteres especiais como `──`, `→`, `—` ou acentos
- Escrever como se um humano tivesse digitado normalmente, sem formatacao decorativa
- Exemplos corretos: `// Dark mode`, `/* Lista de projetos */`, `// Roteamento por query param`
- Exemplos errados: `// ── Dark mode ──`, `/* ── Lista de projetos ── */`

## Commits

Formato obrigatorio: tipo(escopo): descricao
Exemplos: feat(portfolio): adiciona secao de contato
          fix(css): corrige cor dos links no dark mode

Apos qualquer alteracao em arquivos, sugerir o commit diretamente sem perguntar antes se o usuario quer a sugestao.

## Regras

1. **Comentarios no codigo naturais e commits sem atribuicao de IA.**
   Comentarios claros, simples, sem caracteres especiais forcados (──, →, —, ■).
   Commits em portugues, formato `tipo(escopo): descricao`.
   Nunca atribuir autoria a IA (co-authored-by, "feito por Claude").
   **Motivacao:** comentarios decorativos entregam que foram gerados por IA.
   Commits com atribuicao poluem o historico e parecem amadores.

2. **Fazer uma pergunta por vez, com sugestao de resposta.**
   Nunca duas ou mais perguntas na mesma mensagem. Incluir sugestao
   com motivo resumido de cada opcao.
   **Motivacao:** TDAH torna multiplas perguntas paralisantes.

3. **Nao despejar informacao de uma vez.**
   Apresentar planos em etapas, confirmar antes de prosseguir.
   **Motivacao:** sobrecarga cognitiva impede absorcao.

4. **Nunca pular para proxima etapa sem autorizacao.**
   Sugerir o proximo passo, mas aguardar confirmacao explicita.
   **Motivacao:** TDAH precisa de pausas entre etapas para processar.

5. **Sempre ler o arquivo antes de editar.**
   **Motivacao:** editar sem contexto quebra mais do que conserta.

6. **Toda regra e toda skill deve ter motivacao.**
   Ao criar regra ou skill nova, incluir secao de motivacao.
   Verificar se ja existe similar no mesmo nivel ou superiores.
   **Motivacao:** regras sem motivacao viram tarefa robotica que a IA segue cegamente.

7. **Nomenclatura de arquivos e pastas: priorizar hifen como separador.**
   Nomes minusculo, sem acentos. Hifen padrao, underscore so quando
   linguagem exigir (Python vars, __init__.py).
   **Motivacao:** padrao unico evita confusao entre projetos.

8. **Memoria e registro de informacoes.**
   Vault do Obsidian e a unica fonte de memoria.
   Hierarquia: root _index.md -> pasta _index.md -> nota individual.
   Quando surgir informacao importante: verificar se ja existe no vault,
   se existir nao duplicar, se nao existir sugerir criar com aprovacao.
   Nao registrar informacoes efemeras.
   **Motivacao:** memorias separadas criam duplicacao. _index.md como MOC
   garante que a IA encontre o que precisa.

9. **Manter artefatos do projeto atualizados.**
   - **CLAUDE.md e README.md:** manter sincronizados com o estado real.
     Atualizar conforme a tabela:
     | Mudanca | CLAUDE.md | README.md |
     |---|---|---|
     | Stack, LLM, banco, infra ou servico externo | Sim | Sim |
     | Variavel de ambiente nova/removida | Sim (obrigatorias) | Sim (completa) |
     | Arquivo novo/removido na estrutura | Sim (se essencial) | Sim (arvore) |
     | Tabela nova no banco | Sim | Sim |
     | Funcionalidade ou fluxo novo | Sim | Sim |
     | Regra de seguranca ou comportamento | Sim | Nao |
     | Comando, job ou trigger novo | Sim (se afetar fluxo) | Sim |
     | Bug corrigido | Nao (so vault) | Nao |
     | Refatoracao interna | Nao | Nao |
   - **Criterio:** CLAUDE.md e o que a IA precisa saber. README.md e o
     que um humano precisa para usar o projeto.
   **Motivacao:** roadmap desatualizado perde utilidade. Decisoes nao
   registradas viram retrabalho. Documentos defasados geram erros.

10. **Seguir o modelo padrao de README.md definido pela skill `/novo-projeto`.**
    Secoes na ordem padrao: Indice, Objetivo, Forma de entrega, Stack,
    Estrutura, Instalacao, Configuracao, Como usar, Output, Funcionamento,
    Adaptacao, Erros comuns.
    Nenhum path local, credencial, token ou dado sensivel no README.
    **Motivacao:** consistencia entre projetos. Modelo unico facilita
    navegacao e evita vazamento de informacoes sensiveis.

## Memoria do projeto

Use `~/armandonettox/vault-armandonettox/projects/portifolio/` como memoria.
Contexto, decisoes e aprendizados sao registrados la.
Consultar antes de alteracoes significativas.
