---
date: 2026-07-19
categories:
  - Workflow
---

# Obsidian como segundo cérebro para LLMs

Uso o Obsidian como memória persistente para os LLMs com que trabalho (Claude, opencode). Não é só anotação — é o lugar onde o contexto vive entre sessões. O LLM esquece tudo entre conversas; o vault não.

<!-- more -->

## O problema

Toda sessão com um LLM começa do zero. Ele não lembra o que decidimos semana passada, não sabe a arquitetura do projeto, não conhece as convenções que fixamos. Repetir isso a cada sessão é caro (tokens) e frágil (depende de eu lembrar de dizer tudo).

## O que está no vault

Cada projeto tem uma pasta no vault correspondente. O que vive lá:

- **Contexto do projeto** — stack, decisões arquiteturais, por que escolhemos X em vez de Y
- **Decisões e aprendizados** — registry datado de "tentamos A, não funcionou porque B, fomos de C"
- **Sessões** — rascunho cru do que aconteceu em cada sessão de trabalho, antes de ser lapidado em nota permanente
- **Índices** — `_index.md` de cada pasta funcionando como sumário navegável

Os LLMs leem isso no início da sessão (via CLAUDE.md do projeto + skills que consultam o vault) e partem de onde paramos.

## Como o LLM acessa

Uso o MCP do Obsidian no opencode/Claude. O LLM consegue:

- **Buscar semanticamente** — pergunta ao vault por significado, não por string exata
- **Ler notas específicas** — quando uma decisão precisa ser consultada
- **Escrever no vault** — registra decisões e aprendizados durante a sessão

Isso transforma o LLM de "ferramenta amnésica que preciso reensinar toda vez" pra "parceiro que lembra do projeto".

## A diferença na prática

Antes do vault, eu perdia 10–15 minutos por sessão só explicando contexto. Depois, o LLM lê o `CLAUDE.md` do projeto, consulta o vault quando precisa, e Parte direto pra tarefa.

Outro efeito: eu também escrevo mais. Como sei que o LLM vai ler, registro decisões que eu mesmo ia esquecer. O vault deixa de ser diário e vira documentação viva.

## O que aprendi

- **Memória TRANSFORMA LLM.** A diferença entre "qualquer LLM" e "meu LLM" é só contexto persistente. Não é fine-tuning, não é RAG sobre documentos públicos — é memória privada do projeto.
- **O vault não é pra guardar a web nem pra estudar torto.** É um registro operacional: decisões, contexto, aprendizados. Vira bagulho genérico, perde utilidade.
- **Indices (`_index.md`) são decisivos.** Sem índice, o LLM acessar notas se torna chamado aleatório a arquivos soltos. Com índice, ele consegue saber o que existe antes de abrir.
- **Hierarquia de configuracao:** CLAUDE.md do projeto aponta pro vault; o vault aponta pros artefatos. O LLM navega essa hierarquia sem eu explicar.

## Stack no caso de uso

- Obsidian (vaults pessoais e de trabalho)
- opencode + MCP do Obsidian (busca semântica, leitura, escrita)
- Skills locais que encapsulam fluxos (processar inbox, gerar dailies, auditar orphans)
- `CLAUDE.md` por projeto apontando parâmetros e memória

A ideia central: o LLM precisa de memória. Se não é você quem dá, ele vive amnésico. Nada de depender da memória interna do modelo — isso não existe entre sessões.