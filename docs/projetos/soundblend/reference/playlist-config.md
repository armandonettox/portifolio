# Configuração de playlists

Referência completa do formato de configuração de playlists do Soundblend.

---

## Localização do arquivo

| Ambiente | Caminho | Observação |
|----------|---------|------------|
| Padrão (dev e produção) | `config/production.json` | Arquivo incluído no repositório, carregado no início de cada sessão |
| Override em runtime | `st.session_state.playlists` | Editável pela aba **Playlists**, válido só durante a sessão |

!!! note "Sem persistência entre sessões"
    Alterações feitas pela aba **Playlists** ficam em `st.session_state`, isoladas por sessão de navegador. Fechar a aba ou reiniciar o app volta para os valores de `config/production.json`.

---

## Estrutura JSON

O arquivo é um objeto JSON com a chave `playlists` contendo uma lista de objetos de configuração, e opcionalmente a chave `scopes` com os escopos OAuth do Spotify.

```json
{
  "scopes": [
    "user-library-read",
    "playlist-read-private",
    "playlist-modify-public",
    "playlist-modify-private"
  ],
  "playlists": [
    {
      "id": "37i9dQZF1DX0XUsuxWHRQd",
      "name": "Metal",
      "genres": [
        "melodic metalcore",
        "metalcore",
        "death metal",
        "black metal"
      ],
      "ngenres": [
        "deathcore"
      ],
      "aoverride": [
        "Architects"
      ]
    },
    {
      "id": "37i9dQZF1DXcBWIGoYBM5M",
      "name": "Hip-Hop",
      "genres": [
        "hip hop",
        "trap",
        "rap"
      ],
      "ngenres": [],
      "aoverride": []
    }
  ]
}
```

---

## Campos

### `id`

| Propriedade | Valor |
|-------------|-------|
| Tipo | `string` |
| Obrigatório | Sim |

ID único da playlist no Spotify. É o identificador de 22 caracteres presente na URL da playlist.

**Como obter:**

1. Abra a playlist no Spotify Web ou no aplicativo.
2. Copie o link de compartilhamento. O formato é:
   ```
   https://open.spotify.com/playlist/37i9dQZF1DX0XUsuxWHRQd
   ```
3. O ID é a sequência após `/playlist/`:
   ```
   37i9dQZF1DX0XUsuxWHRQd
   ```

!!! warning "Permissões necessárias"
    Para playlists que o Soundblend vai modificar (adicionar e remover faixas), a conta autenticada precisa ser a dona da playlist ou ter permissão de colaboração. Playlists de terceiros sem permissão causam erro `403 Forbidden` na API.

**Exemplo:**

```json
"id": "37i9dQZF1DX0XUsuxWHRQd"
```

---

### `name`

| Propriedade | Valor |
|-------------|-------|
| Tipo | `string` |
| Obrigatório | Não |

Nome de exibição da playlist na interface do Soundblend. Não precisa coincidir com o nome real da playlist no Spotify — é usado apenas para identificação na UI.

!!! tip "Atualização automática"
    Ao selecionar uma playlist no selectbox da aba **Playlists**, o campo `name` é atualizado automaticamente com o nome real da playlist na sua conta Spotify.

**Exemplo:**

```json
"name": "Metal"
```

---

### `genres`

| Propriedade | Valor |
|-------------|-------|
| Tipo | `array` de `string` |
| Obrigatório | Sim |

Lista de gêneros que definem quais artistas entram na playlist. Uma faixa é incluída se o artista tiver **pelo menos um** dos gêneros listados.

**Comportamento:**

- A comparação é feita contra os macro-gêneros do artista (não da faixa), obtidos do MusicBrainz e normalizados pela taxonomia do app.
- A condição é `OR`: basta um único gênero da lista coincidir.
- Sinônimos configurados no mapeamento de gêneros (aliases) expandem tanto `genres` quanto `ngenres` antes da filtragem.

**Exemplo:**

```json
"genres": [
  "melodic metalcore",
  "metalcore",
  "death metal"
]
```

Artista com gêneros `["metalcore", "post-hardcore"]` seria incluído porque `"metalcore"` está na lista.

---

### `ngenres`

| Propriedade | Valor |
|-------------|-------|
| Tipo | `array` de `string` |
| Obrigatório | Não |

Lista de gêneros que excluem artistas da playlist. Uma faixa é **removida** se o artista tiver **pelo menos um** dos gêneros listados, independentemente de qualquer outra regra.

!!! danger "Precedência absoluta"
    `ngenres` tem precedência sobre `genres` e sobre `aoverride`. Se um artista tiver qualquer gênero presente em `ngenres`, a faixa não entra na playlist — sem exceções.

**Exemplo:**

```json
"ngenres": [
  "deathcore"
]
```

Artista com gêneros `["metalcore", "deathcore"]` seria excluído porque `"deathcore"` está em `ngenres`, mesmo que `"metalcore"` esteja em `genres`.

Array vazio (`[]`) significa que nenhum gênero exclui artistas:

```json
"ngenres": []
```

---

### `aoverride`

| Propriedade | Valor |
|-------------|-------|
| Tipo | `array` de `string` |
| Obrigatório | Não |

Lista de nomes exatos de artistas que devem entrar na playlist independentemente dos gêneros encontrados.

**Comportamento:**

A faixa entra se o artista estiver em `aoverride`, mesmo que nenhum gênero coincida — inclusive quando `genres` está vazio. Com o modo colab ativado, basta qualquer artista da faixa estar na lista. `ngenres` continua tendo precedência.

!!! warning "Nome exato"
    O nome do artista deve ser idêntico ao exibido no Spotify, incluindo capitalização, acentos e caracteres especiais. Exemplo: `"Sepultura"` não corresponde a `"sepultura"`.

**Exemplo:**

```json
"genres": ["metal"],
"aoverride": ["Architects"]
```

O artista `"Architects"` entra na playlist mesmo que o MusicBrainz não o classifique com nenhum gênero da lista.

Array vazio (`[]`) significa que nenhum artista recebe tratamento especial:

```json
"aoverride": []
```

---

## Precedência

A ordem de avaliação para cada faixa é:

```
1. ngenres (exclusão)  -->  artista tem gênero em ngenres? EXCLUI (fim)
2. genres + aoverride  -->  artista tem gênero em genres (ou recebeu via aoverride)? INCLUI
3. sem match           -->  faixa não entra na playlist
```

**Tabela resumo:**

| Cenário | ngenres | genres | aoverride | Resultado |
|---------|---------|--------|-----------|-----------|
| Artista tem gênero em ngenres | Sim | — | — | Excluído |
| Artista tem gênero em genres | Não | Sim | — | Incluído |
| Artista em aoverride, sem gênero em genres | Não | Não | Sim | Incluído (gênero injetado) |
| Artista em aoverride E tem gênero em ngenres | Sim | — | Sim | Excluído (ngenres vence) |
| Artista não tem gênero em genres | Não | Não | Não | Não incluído |

!!! danger "ngenres sempre vence"
    Mesmo que um artista esteja listado em `aoverride`, se ele tiver qualquer gênero presente em `ngenres`, a faixa será excluída. `ngenres` é a regra de maior precedência no sistema.

---

## Macro-gêneros

Os gêneros vêm do MusicBrainz e são normalizados pela taxonomia embutida (`genre_taxonomy.py`) em cerca de 25 macro-gêneros em letras minúsculas. Exemplos:

```
"rock"
"metal"
"hip hop"
"mpb"
"samba"
"funk brasileiro"
"eletronica"
```

**Regras de uso:**

- A comparação é **case-sensitive**. `"Hip Hop"` não corresponde a `"hip hop"`.
- Na UI, os campos de gêneros são multiselects preenchidos com os gêneros encontrados na sua biblioteca — não é preciso digitar de cabeça.
- A aba **Configurar** mostra todos os artistas da biblioteca e seus gêneros numa tabela — use o campo de busca pra achar um artista específico, ou a tabela inteira pra ter uma visão geral.

!!! tip "Gêneros inexistentes"
    Se um gênero em `genres` ou `ngenres` não corresponder a nenhum artista das suas músicas curtidas, ele simplesmente não terá efeito — não causa erro.
