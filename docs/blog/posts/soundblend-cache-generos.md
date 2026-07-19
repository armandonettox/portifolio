---
date: 2026-07-19
slug: soundblend-o-app-que-nasceu-de-uma-frustracao-com-playlists
categories:
  - Projetos
---

# Soundblend: o app que nasceu de uma frustração com playlists

Curtir música no Spotify é um clique — e eu clicava muito. Minhas músicas curtidas viravam uma biblioteca gigante, mas as playlists, que eu organizo por uma lógica de gênero, viviam pobres: distribuir centenas de curtidas manualmente pelas playlists certas era um trabalho que nunca saía do lugar. A frustração de abrir o Spotify e encontrar playlists minguadas, com tanta música curtida acumulada, foi o ponto de partida do Soundblend.

<!-- more -->

## Da frustração à API

Fui estudar a API do Spotify, e ela resolve boa parte do problema: dá pra ler todas as músicas curtidas, administrar as playlists e ver os artistas por trás de cada faixa. Mas no meio do caminho apareceu a dificuldade: **o Spotify não entrega o gênero das músicas nem dos artistas** de forma confiável. A saída foi cruzar com o [MusicBrainz](https://musicbrainz.org/), uma base aberta de metadados musicais, usando as tags que a própria comunidade dá aos artistas.

## As decisões técnicas

1. **Cache em disco** — um `genre_cache.json` guarda `artist_id -> [generos]`. A API do MusicBrainz limita a 1 requisição por segundo, então a primeira execução é lenta (300 artistas = 5 minutos), mas as seguintes são instantâneas.
2. **Normalização em macro-gêneros** — o MusicBrainz retorna tags livres (`heavy metal`, `death metal`, `thrash metal`); o Soundblend normaliza tudo pra `metal`, pra que as regras de playlist sejam configuradas em categorias escutáveis, não em 47 subgêneros.
3. **Busca paralela das curtidas** — as liked songs do Spotify baixam em paralelo; o gargalo de rede fica isolado só no MusicBrainz.
4. **Sincronização com preview** — antes de mexer nas playlists, o app mostra o que vai mudar e aplica só o diff, com opção de desfazer.

## O que aprendi

- Cache em disco resolve 90% do problema de rate limit quando os dados são públicos e imutáveis. Não vale a pena subir um Redis pra isso.
- Macro-gêneros são subjetivos, mas necessários. Sem normalização, o usuário passa mais tempo configurando regras do que ouvindo música.
- 1 req/s parece pouco, mas com cache é só o custo da primeira execução.

O Soundblend nunca teve finalidade de ganhar dinheiro — ele existe pra cumprir uma necessidade minha. E é justamente por isso que ele funciona: eu sou o primeiro usuário e o primeiro a reclamar quando algo não está bom.

Código no [repositório do Soundblend](https://github.com/armandonettox/soundblend).
