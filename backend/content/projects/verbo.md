---
title: Verbo
stack: [Python, RAG, ChromaDB, NVIDIA NIM, Streamlit]
summary: RAG fechado sobre a Bíblia Católica, em português. Responde só com base no texto-fonte, sem inventar com conhecimento geral do LLM.
repo: https://github.com/armandonettox/verbo
---

Verbo é um RAG fechado sobre a Bíblia Católica, em português. Responde perguntas usando só o texto da Bíblia como fonte e diz claramente quando não encontra nada relevante. Projeto público, em produção no Streamlit Community Cloud. O nome vem de João 1:1, "no princípio era o Verbo".

## Origem

Nasceu de uma necessidade real: na preparação para a crisma, surgiu a vontade de ter uma ferramenta para estudar a Bíblia sem o risco de uma IA generalista inventar interpretações. Isso virou a regra central do projeto.

## O que faz

- Busca semântica: a pergunta em linguagem natural é respondida a partir dos versículos mais próximos por significado, não por palavra-chave.
- Conversa de acompanhamento, mantendo o contexto da busca original.
- Leitura completa por livro e capítulo, com áudio narrado.
- Versículo do dia e modo escuro.

## Como funciona

1. Os versículos são agrupados por capítulo em blocos de até 1.500 caracteres e cada bloco vira um embedding guardado no ChromaDB.
2. A pergunta também vira embedding e é comparada com os blocos indexados.
3. O modelo de chat recebe só os trechos encontrados, com instrução explícita de não usar conhecimento próprio.
4. Toda resposta cita livro e capítulo, para o usuário conferir o texto original.

## Documentação

A documentação técnica (instalação, configuração, arquitetura e erros comuns) fica junto do código, no repositório do projeto.
