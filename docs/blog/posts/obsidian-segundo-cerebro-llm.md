---
date: 2026-07-19
slug: obsidian-como-segundo-cerebro-para-llms
categories:
  - Workflow
---

# Obsidian como segundo cérebro para LLMs

Cheguei nessa ideia quando o uso do Claude Code com Obsidian viralizou — mas não embarquei por modinha. Fui estudar o que havia por trás: estudos publicados, repositórios e ideias de gente bem conceituada, como o Karpathy. O que entendi é que usar o Obsidian como segundo cérebro nada mais é do que ativar a memória do LLM em um lugar diferente — e de uma forma que consome bem menos tokens.

<!-- more -->

## Desmistificando a ideia

- Por algum motivo, LLMs entendem muito bem arquivos `.md` — texto plano com estrutura leve é o formato que eles leem melhor.
- O Obsidian entra pela conveniência: plugins como o de **busca semântica** facilitam o LLM achar a nota certa por significado, não por string exata.
- O grafo de ligar pontos, que tanto atrai nas capturas de tela, é praticamente só apelo visual — não é ele que faz a memória funcionar.
- No fundo, daria pra fazer o mesmo com um repositório de arquivos `.md` organizado em Python com uma lib de busca semântica, ou com qualquer outra ferramenta que trabalhe com Markdown, como o Notion. O Obsidian é a embalagem; a ideia é memória em texto plano.

## Como eu montei o meu

- **MCPs próprios** de leitura e escrita, pra o LLM usar o vault melhor do que um simples "abrir arquivo".
- **Camada principal**: as regras vivem dentro do próprio Obsidian, junto com um arquivo *hot* (~500 palavras) com a informação mais fresca — é a primeira coisa lida em toda sessão.
- **Camada secundária**: índices direcionados por assunto, que dizem ao LLM o que existe antes de ele abrir qualquer nota.
- **Skills personalizadas** que gravam as sessões de trabalho, processam e organizam o vault inteiro.

## A regra de ouro

Eu **nunca edito o vault manualmente**. Se o LLM me traz uma informação errada de lá, eu ensino ele a corrigir — a manutenção da memória também é responsabilidade dele. E ele identifica pontos de aprendizado sozinho, gerando notas específicas de *learnings* que são priorizadas antes de qualquer atitude ou decisão.

O resultado: toda sessão começa de onde a última parou, sem eu gastar 10 minutos reexplicando contexto — e sem depender da memória interna do modelo, que entre conversas simplesmente não existe.
