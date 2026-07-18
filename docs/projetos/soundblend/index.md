# Soundblend

Soundblend é um app web construído com Streamlit que lê suas músicas curtidas no Spotify e as distribui automaticamente em playlists organizadas por gênero musical, com suporte a regras de inclusão, exclusão e substituição de artistas.

## O que faz

- **Configurar artistas** — tabela editável com todos os artistas da biblioteca e seus gêneros (MusicBrainz), pra corrigir ou completar antes de sincronizar
- **Organizar playlists** — edita as regras de cada playlist (genres, ngenres, aoverride) direto pela interface, sem precisar editar arquivos manualmente
- **Sincronizar** — lê todas as liked songs e distribui nas playlists conforme as regras configuradas, com preview antes de aplicar e opção de desfazer

## Como funciona

```
Autenticação OAuth (Spotify)
        ↓
Busca liked songs (páginas baixadas em paralelo)
        ↓
Identifica gêneros dos artistas via MusicBrainz
(cache em disco + 1 req/s, normalizados em macro-gêneros)
        ↓
Para cada playlist configurada:
  - Filtra por genres[] (artista entra se tiver qualquer um)
  - Aplica aoverride (artista entra independente de gênero)
  - Exclui por ngenres[] (precedência absoluta)
  - Ordena por artista e álbum
  - Aplica só o diff na playlist do Spotify (chunks de 100)
```

O fluxo completo é executado pelo módulo `commands/reload.py`. As regras de cada playlist são configuradas pela interface e vivem na sessão do navegador (`st.session_state`); o único dado em disco é o cache de gêneros (`genre_cache.json`), que é metadado público de artistas.

## Acesso

O app está disponível em produção em:

**[https://soundblend.streamlit.app](https://soundblend.streamlit.app)**

!!! warning "Sessão sem persistência"
    O Soundblend roda no Streamlit Community Cloud. Cache de artistas, overrides de gênero e token OAuth vivem só na sessão do navegador — fechar a aba ou reiniciar o app reseta esse estado. Para rodar sua própria instância, siga o guia de instalação.

## Começando

!!! tip "Por onde começar"
    Recomenda-se começar pela página de pré-requisitos antes de qualquer outra etapa. Ela cobre a criação do Spotify App, as variáveis de ambiente necessárias e os escopos OAuth obrigatórios.

- [Pré-requisitos](getting-started/prerequisites.md) — Spotify App, credenciais e escopos OAuth
- [Instalação](getting-started/installation.md) — como rodar localmente
- [Configuração de playlists](getting-started/configuration.md) — estrutura do JSON e regras de gênero

## Repositório

Código-fonte em [github.com/armandonettox/soundblend](https://github.com/armandonettox/soundblend).
