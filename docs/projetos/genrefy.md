---
title: Genrefy
---

# Genrefy

Organiza automaticamente as musicas curtidas do Spotify em playlists por genero.

**Status:** Em producao | [genrefy.armandonetto.com](https://genrefy.armandonetto.com) | [GitHub](https://github.com/armandonettox/genrefy)

## O que faz

O Genrefy autentica com a conta do Spotify via OAuth, varre todas as musicas curtidas, identifica os generos de cada artista pela API do Spotify e distribui as faixas nas playlists conforme as regras configuradas pelo usuario.

- Configuracao de playlists, generos incluidos, generos excluidos e artistas fixos pelo proprio app
- Lista artistas sem genero mapeado em nenhuma playlist
- Exporta CSV com todos os artistas e seus generos

## Stack

- Python + Streamlit
- spotipy (API do Spotify)
- Podman + podman-compose
- nginx (reverse proxy)
- Oracle Cloud VM
- GitHub Actions (deploy automatico)

[Ver no GitHub](https://github.com/armandonettox/genrefy)
