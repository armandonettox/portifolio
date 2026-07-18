# Playlists

A aba **Playlists** é o coração do Soundblend: nela você define as playlists, os filtros de gênero de cada uma, e dispara a sincronização. Os gêneros dos artistas são revisados antes, na aba **Configurar**.

---

## Interface

Na barra lateral fica a lista das playlists configuradas. Clicar em uma delas abre, na área principal, um painel com:

- **Cards de métrica**: quantos gêneros estão incluídos, quantos artistas da sua biblioteca são mapeados por esses gêneros, e quantas músicas entrariam nessa playlist com a configuração atual.
- **Selectbox — Playlist do Spotify vinculada**: escolhe a playlist da sua conta que recebe as faixas.
- **Multiselect — Gêneros incluídos** (`genres`): artistas com qualquer um desses gêneros entram na playlist.
- **Multiselect — Gêneros excluídos** (`ngenres`): artistas com qualquer um desses gêneros são removidos, mesmo que também tenham um gênero incluído — precedência absoluta.
- **Multiselect — Artistas fixos** (`aoverride`): artistas que entram na playlist independentemente do gênero.

Os três multiselects são preenchidos com os gêneros e artistas encontrados na sua própria biblioteca — não é preciso digitar de cabeça.

### Botões

| Botão | Ação |
|-------|------|
| **+ Adicionar** (sidebar) | Cria uma nova entrada de playlist |
| **Remover** | Remove a playlist selecionada da configuração |
| **Descartar** | Desfaz alterações não salvas nesta sessão |
| **Salvar** | Grava a configuração em `st.session_state`, válida para a sessão atual |
| **Sincronizar ▶** | Sincroniza só a playlist selecionada |
| **Sincronizar tudo** (sidebar) | Sincroniza todas as playlists configuradas de uma vez |

### Mapeamento de gêneros (sinônimos)

Expander opcional para declarar que um gênero é sinônimo de outro — por exemplo, `hip hop` como sinônimo de `rap`. Ao configurar `rap` em `genres`, artistas com `hip hop` também entram. O mapeamento vale tanto para gêneros incluídos quanto para excluídos.

---

## O que a sincronização faz

Ao confirmar, o app executa o fluxo de `commands/reload.py`:

1. Usa a biblioteca e os gêneros já carregados na sessão (sem refetch).
2. Para cada playlist selecionada, filtra as faixas: entra se o artista tiver algum gênero incluído (ou estiver em `aoverride`); sai se tiver algum gênero excluído, mesmo que também bata com `genres` ou `aoverride` — `ngenres` sempre vence.
3. Ordena o resultado por artista e álbum.
4. Compara com o conteúdo atual da playlist e calcula **apenas a diferença**: o que precisa ser adicionado e o que precisa ser removido.

!!! note "Não é destrutivo"
    A sincronização não limpa e reconstrói a playlist do zero — ela aplica só o diff. Faixas que já estavam certas continuam intactas; só entram e saem as que mudaram de status.

---

## Preview e confirmação

Antes de qualquer alteração no Spotify, o app mostra uma tabela de preview com, por playlist: quantas faixas seriam adicionadas, quantas removidas, quantas mantidas e o total final. Só depois de clicar em **Confirmar** a sincronização é de fato aplicada. **Cancelar** volta para a tela de configuração sem mexer em nada.

---

## Desfazer

Antes de aplicar qualquer mudança, o app salva um snapshot do conteúdo atual de cada playlist afetada. Depois de sincronizar, um botão **Desfazer última sincronização** aparece na aba, restaurando cada playlist ao estado anterior. O snapshot vive só na sessão — fechar a aba ou sincronizar de novo substitui o snapshot anterior.

---

## Resultado

Ao finalizar, o app mostra o total final de faixas por playlist:

```
Rock Alternativo  →  47 faixas
Metal             →  31 faixas
Eletrônico        →   0 faixas
```

---

## O que fazer se uma playlist ficou com 0 faixas

1. **Confira `genres` e `ngenres`** no painel da playlist. Os gêneros vêm do MusicBrainz, normalizados em macro-gêneros (`rock`, `metal`, `hip hop`, `mpb` etc.) — não são os gêneros originais do Spotify.
2. **Use a aba Configurar** para inspecionar (e corrigir, se preciso) os gêneros de um artista específico.
3. **Verifique conflitos entre `genres` e `ngenres`**: se um gênero aparece nos dois, `ngenres` sempre vence.
4. **Confira `aoverride`** para garantir a entrada de artistas específicos independentemente do gênero.
5. **Use o mapeamento de sinônimos** se o gênero do artista for uma variação do que está configurado (ex: `hip hop` vs `rap`).

---

## Tempo de execução

A sincronização em si é rápida — reutiliza a biblioteca e os gêneros já carregados na sessão e só aplica o diff (adições e remoções em chunks de 100).

O que pode demorar é o **primeiro login** de uma conta nova: o download das músicas curtidas e a busca de gêneros no MusicBrainz acontecem em sequência, numa única barra de progresso contínua, antes das abas aparecerem.

| Situação | Tempo estimado |
|----------|----------------|
| Gêneros já no cache em disco | segundos |
| Biblioteca nova (~300 artistas sem cache) | ~5 minutos, uma única vez |
| Biblioteca grande (~1000 artistas sem cache) | ~15-18 minutos, uma única vez |

!!! note "Gargalo principal: MusicBrainz"
    O MusicBrainz limita a 1 requisição por segundo, e essa busca acontece uma vez por artista novo. O resultado fica no cache em disco por 30 dias, então esse custo é pago uma vez por artista — não por sessão nem por usuário, já que o cache é compartilhado.

---

## Estrutura de playlist relevante

Referência rápida dos campos que afetam a sincronização:

```json
{
  "id": "ID_SPOTIFY",
  "name": "Nome da Playlist",
  "genres": ["rock", "punk"],
  "ngenres": ["pop"],
  "aoverride": ["Arctic Monkeys"]
}
```

- `genres`: artista entra se tiver **qualquer** um desses gêneros
- `ngenres`: artista **sai** se tiver qualquer um — precedência absoluta
- `aoverride`: artista entra independentemente do gênero (só `ngenres` pode excluí-lo)
