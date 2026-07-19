---
date: 2026-07-19
categories:
  - Projetos
---

# Por que o Verbo é RAG fechado (e não usa conhecimento geral do LLM)

O Verbo responde perguntas sobre a Bíblia usando só o texto da Bíblia como fonte. Poderia ter sido um wrapper simples em volta da API da OpenAI ou do NVIDIA NIM, mas escolhi bloquear o conhecimento geral do LLM de propósito.

<!-- more -->

## O problema

Quando você pergunta "o que a Bíblia fala sobre X?" pra um LLM sem restrição, ele responde com uma mistura de:
- Trechos reais que ele memorizou no treino
- Paráfrases que ele acha que fazem sentido
- Conhecimento geral que parece plausível mas não está em versículo nenhum

Para um texto religioso, onde cada palavra carrega peso teológico, isso é inaceitável. "Inventar" um versículo é o pior cenário possível.

## A solução: RAG fechado

O fluxo é:

1. **Indexação** — cada versículo (35.450 no total, Bíblia Ave Maria) vira um vetor via NVIDIA NIM e é guardado em ChromaDB local.
2. **Pergunta** — a pergunta do usuário também vira vetor.
3. **Busca por similaridade** — ChromaDB retorna os 5 versículos mais próximos no espaço semântico.
4. **Geração** — o prompt enviado pro LLM contém só a pergunta + os 5 versículos. A instruçao é explícita: "responda só com base nos trechos fornecidos. Se não houver resposta neles, diga que não encontrou."

## O que isso custa

- **Latência** — duas chamadas de embedding (pergunta) + uma chamada de chat completion. Em média 3–4 segundos por resposta.
- **Precisão de citação** — toda resposta traz `livro capítulo:versículo`. Se o LLM tentar alucinar, o usuário consegue conferir em 5 segundos.
- **Free tier do NVIDIA NIM** — suficiente pra desenvolvimento e uso pessoal. Escalar pra muitos usuários precisaria de orçamento.

## O que aprendi

- "RAG fechado" não é só RAG com poucos documentos — é RAG onde o LLM é **expressamente proibido** de usar conhecimento de treino. A instrução no prompt é o que separa isso de um RAG comum.
- 5 versículos é um número mágico: pouco contexto, custa pouco, e quase sempre é suficiente pra responder perguntas temáticas.
- Embedding e chat completion não precisam vir do mesmo fornecedor. Funciona separar, desde que ambos usem um modelo de qualidade compatível.

Código no [repositório do Verbo](https://github.com/armandonettox/verbo).