# Configurar

## O que faz

A aba **Configurar** mostra todos os artistas da sua biblioteca numa tabela editável, com o gênero atual de cada um (vindo do cache/MusicBrainz, ou de um override já salvo). É o lugar pra revisar e corrigir gêneros antes de organizar as playlists na aba **Playlists**.

Usa os dados já carregados na sessão — abre em segundos, sem chamada de API.

## Interface

- **Buscar por nome**: filtra a tabela pelo nome do artista.
- **Só sem gênero**: mostra só os artistas cuja coluna Gêneros está vazia.
- **Tabela editável**: colunas Nome (fixa) e Gêneros (editável, separados por vírgula). Dá pra editar qualquer artista, não só os sem gênero.
- **Salvar alterações**: grava as edições como overrides, válidos pra essa conta enquanto a sessão durar.

## Como o override funciona

Editar o campo Gêneros de um artista e salvar cria um override pra aquele artista: da próxima vez que a biblioteca carregar, o gênero editado é usado em vez do que veio do MusicBrainz.

- **Deixar o campo vazio e salvar** também é um override válido — o artista fica explicitamente sem gênero (diferente de nunca ter sido editado). Isso é útil quando o MusicBrainz atribuiu um gênero errado e você não quer nenhum no lugar.
- **Editar de volta pro valor original** remove o override — o artista volta a usar o gênero natural do cache.
- Overrides são aplicados em todo o app: na tabela de Configurar, nos multiselects de gênero da aba Playlists, no preview e na sincronização, e nas Stats.

## Artistas sem gênero no MusicBrainz

!!! note "Gêneros vazios"
    Alguns artistas, especialmente os menores ou recém-cadastrados, não têm gêneros no MusicBrainz. Esses artistas aparecem na tabela com a coluna **Gêneros** vazia.

    Pra incluí-los numa playlist, defina o gênero manualmente aqui, ou use o campo **Artistas fixos** (`aoverride`) na aba Playlists pra incluir o artista independente de gênero.
