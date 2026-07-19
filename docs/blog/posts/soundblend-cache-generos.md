---
date: 2026-07-19
categories:
  - Soundblend
---

# Cache de gêneros no Soundblend: MusicBrainz com taxa de 1 req/s

O Soundblend precisa saber o gênero de cada artista da biblioteca do Spotify pra distribuir as músicas em playlists por gênero. O problema: o Spotify não expõe gênero no endpoint de artista de forma confiável, e a biblioteca de um usuário pode ter centenas de artistas diferentes.

<!-- more -->

## Por que MusicBrainz

MusicBrainz é uma base aberta de metadados musicais. Tem API gratuita, mas com um limite explícito: **1 requisição por segundo** por IP. Para um usuário com 300 artistas, isso significa 5 minutos só pra montar o cache na primeira execução.

## As decisões que tomei

1. **Cache em disco** — um `genre_cache.json` guarda `artist_id -> [generos]`. Uma vez populado, execuções seguintes não refazem as requisições. É metadado público de artista, então não precisava de banco nem encriptação.
2. **Rate limit de 1 req/s** — implementado com `time.sleep(1)` entre chamadas. Simples e suficiente pra respeitar a política do MusicBrainz.
3. **Normalização em macro-gêneros** — MusicBrainz retorna tags livres (`heavy metal`, `death metal`, `thrash metal`). O Soundblend normaliza tudo pra `metal`, pra que o usuário configure regras em cima de categorias escutáveis e não em 47 subgêneros.
4. **Busca paralela das liked songs** — o gargalo de rede fica isolado no MusicBrainz. As músicas curtidas do Spotify são baixadas em paralelo, porque o endpoint `/me/tracks` não tem o mesmo rate limit restrito.

## O que aprendi

- Cache em disco resolve 90% do problema de rate limit quando os dados são públicos e imutáveis. Não vale a pena subir um Redis pra isso.
- Macros de gênero são subjetivos, mas necessários. Sem normalização, o usuário passa mais tempo configurando regras do que ouvindo música.
- 1 req/s parece lixo, mas com cache é só custo da primeira execução. Depois disso o app responde instantaneamente.

Código no [repositório do Soundblend](https://github.com/armandonettox/soundblend).