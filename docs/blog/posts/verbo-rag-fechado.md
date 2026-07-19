---
date: 2026-07-19
slug: por-que-o-verbo-e-rag-fechado-e-nao-usa-conhecimento-geral-do-llm
categories:
  - Projetos
---

# Verbo: o RAG que nasceu na crisma

O Verbo não estava nos meus planos. Ele surgiu quando comecei a fazer a crisma na igreja católica junto com a minha namorada — e ela comentou que sentia falta de uma IA, ou algo parecido, pra aprimorar os conhecimentos bíblicos dela. Aproveitei esse desejo pra criar o projeto e aprender, na prática, todo o processo de um RAG: da criação ao funcionamento. Com uma regra clara: ele só responde com base na Bíblia que ela escolheu, a Ave Maria — a mesma que usamos na crisma.

<!-- more -->

## Por que RAG fechado

Quando você pergunta "o que a Bíblia fala sobre X?" pra um LLM sem restrição, ele responde com uma mistura de trechos reais que memorizou no treino, paráfrases que acha que fazem sentido e conhecimento geral que parece plausível mas não está em versículo nenhum. Para um texto religioso, onde cada palavra carrega peso teológico, isso é inaceitável — "inventar" um versículo é o pior cenário possível.

Por isso o Verbo é um RAG **fechado**: o LLM é expressamente proibido de usar conhecimento de treino. Se a resposta não estiver nos trechos recuperados, ele diz que não encontrou.

## Como funciona

1. **Indexação** — cada versículo (35.450 no total, Bíblia Ave Maria) vira um vetor via NVIDIA NIM e é guardado em ChromaDB local.
2. **Pergunta** — a pergunta do usuário também vira vetor.
3. **Busca por similaridade** — ChromaDB retorna os 5 versículos mais próximos no espaço semântico.
4. **Geração** — o prompt enviado pro LLM contém só a pergunta + os 5 versículos, com instrução explícita: "responda só com base nos trechos fornecidos".

Toda resposta traz `livro capítulo:versículo` — se o modelo tentar alucinar, dá pra conferir na Bíblia em 5 segundos.

## O que aprendi

- "RAG fechado" não é só RAG com poucos documentos — é RAG onde o LLM é proibido de usar conhecimento de treino. A instrução no prompt é o que separa isso de um RAG comum.
- 5 versículos é um número mágico: pouco contexto, custa pouco, e quase sempre é suficiente pra responder perguntas temáticas.
- O melhor projeto pra aprender uma tecnologia é o que resolve a necessidade real de alguém do seu lado — o retorno é imediato e a régua de qualidade é alta, porque tem gente de verdade usando.

Código no [repositório do Verbo](https://github.com/armandonettox/verbo).
