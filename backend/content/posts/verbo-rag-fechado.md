---
title: "Verbo: o RAG que nasceu na crisma"
date: 2026-07-19
summary: "O Verbo não estava nos meus planos. Ele surgiu quando comecei a fazer a crisma na igreja católica junto com a minha namorada — e ela comentou que sentia falta de uma IA, ou algo parecido, pra aprimorar os conhecimentos bíblicos dela. Aproveitei esse desejo pra criar o projeto e aprender, na prática, todo o processo de um RAG: da criação ao funcionamento. Com uma regra clara: ele só responde com base na tradução da Bíblia que ela escolheu, a mesma que usamos na crisma."
tags: [projetos]
---

O Verbo não estava nos meus planos. Ele surgiu quando comecei a fazer a crisma na igreja católica junto com a minha namorada — e ela comentou que sentia falta de uma IA, ou algo parecido, pra aprimorar os conhecimentos bíblicos dela. Aproveitei esse desejo pra criar o projeto e aprender, na prática, todo o processo de um RAG: da criação ao funcionamento. Com uma regra clara: ele só responde com base na tradução da Bíblia que ela escolheu, a mesma que usamos na crisma.


## Por que RAG fechado

Quando você pergunta "o que a Bíblia fala sobre X?" pra um LLM sem restrição, ele responde com uma mistura de trechos reais que memorizou no treino, paráfrases que acha que fazem sentido e conhecimento geral que parece plausível mas não está em versículo nenhum. Para um texto religioso, onde cada palavra carrega peso teológico, isso é inaceitável — "inventar" um versículo é o pior cenário possível.

Por isso o Verbo é um RAG **fechado**: o LLM é expressamente proibido de usar conhecimento de treino. Se a resposta não estiver nos trechos recuperados, ele diz que não encontrou.

## Como funciona

1. **Indexação** — os 35.450 versículos são agrupados por capítulo em blocos de até 1.500 caracteres, sem quebrar um versículo no meio. Cada bloco vira um vetor via NVIDIA NIM e é guardado em ChromaDB local.
2. **Pergunta** — a pergunta do usuário também vira vetor.
3. **Busca por similaridade** — ChromaDB retorna até 40 blocos próximos no espaço semântico, descartando qualquer um abaixo de 40% de similaridade.
4. **Geração** — o prompt enviado pro LLM contém só a pergunta + os trechos encontrados, com instrução explícita: "responda só com base nos trechos fornecidos".

Toda resposta traz o livro e o capítulo dos trechos usados — se o modelo tentar alucinar, dá pra conferir na Bíblia em 5 segundos.

## O que aprendi

- "RAG fechado" não é só RAG com poucos documentos — é RAG onde o LLM é proibido de usar conhecimento de treino. A instrução no prompt é o que separa isso de um RAG comum.
- Indexar por capítulo, e não versículo por versículo, preserva o contexto ao redor da resposta.
- O melhor projeto pra aprender uma tecnologia é o que resolve a necessidade real de alguém do seu lado — o retorno é imediato e a régua de qualidade é alta, porque tem gente de verdade usando.

Código no [repositório do Verbo](https://github.com/armandonettox/verbo).
