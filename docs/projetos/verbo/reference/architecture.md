# Arquitetura

## Estrutura do projeto

```
verbo/
    data/
        biblia.json              <- fonte validada (73 livros, 35.450 versículos)
        construir-banco.py       <- agrupa por capítulo, gera embeddings e popula o Chroma
    modules/
        busca.py                 <- consulta o Chroma, retorna trechos próximos
        resposta.py              <- monta prompt, chama NVIDIA NIM e sustenta a conversa
        leitura.py                <- carrega a Bíblia inteira para a tela de leitura
        plano_livre.py            <- seletor de livro e capítulo na barra lateral
        plano_versiculo_dia.py    <- versículo do dia, sem repetir no ciclo
        audio_widget.py           <- narração via Web Speech API (botão simples e com progresso)
        acoes_chat.py              <- copiar e compartilhar a resposta
        fuso_horario.py            <- detecta o fuso do navegador para timestamps do chat
    assets/
        estilo.css                <- CSS externo, com variáveis para os dois temas
        templates/                 <- HTML/JS embutidos via components.html
    app.py                       <- interface Streamlit
    config.py                    <- configurações, nomes de modelo, paths
    tests/                       <- suite pytest
```

## Módulos

### `app.py` — Interface

Ponto de entrada Streamlit. Monta a tela de busca (com o formulário de pergunta e o versículo do dia), o chat de acompanhamento, a tela de leitura de capítulo e a barra lateral, alternando entre esses estados via `st.session_state`.

### `modules/busca.py` — Busca por similaridade

**`buscar_versiculos(pergunta)`**

1. Gera o embedding da pergunta via NVIDIA NIM (`EMBEDDING_MODEL`).
2. Consulta a coleção do Chroma (`CHROMA_DB_PATH` / `COLLECTION_NAME`) com esse vetor, pedindo até `TOP_K` resultados.
3. Converte a distância L2 (embeddings normalizados) em similaridade de cosseno e descarta qualquer resultado abaixo de `SIMILARIDADE_MINIMA`. Como os resultados já vêm ordenados por distância crescente, o primeiro abaixo do limiar garante que os seguintes também estão.

Cliente OpenAI e coleção Chroma são inicializados uma única vez (lazy, via `_init()`) e reutilizados entre chamadas.

### `modules/resposta.py` — Geração da resposta

**`gerar_resposta(pergunta, versiculos)`** monta um prompt com os trechos encontrados como contexto e uma instrução explícita para responder **exclusivamente** com base neles, chama o modelo de chat da NVIDIA NIM (`CHAT_MODEL`) e retorna o texto da resposta.

**`continuar_conversa(...)`** reaproveita a pergunta e os trechos da busca original, mais o histórico de mensagens trocadas até agora, para responder a uma pergunta de acompanhamento sem rodar uma nova busca semântica.

### `modules/leitura.py` — Texto completo

Carrega `biblia.json` inteiro e organiza por capítulo, com o texto formatado em markdown (`**1.** texto do versículo`). Usado tanto pela tela de leitura quanto por `texto_para_audio()`, que remove a marcação de número de versículo para gerar um texto corrido, adequado à narração.

### `modules/plano_livre.py` — Navegação por livro e capítulo

Monta a lista de livros a partir dos capítulos carregados e renderiza os seletores de livro/capítulo na barra lateral, abrindo a tela de leitura no capítulo escolhido.

### `modules/plano_versiculo_dia.py` — Versículo do dia

Calcula qual versículo mostrar em cada data a partir de uma época fixa (1º de janeiro de 2026), percorrendo a lista completa de versículos em ordem e usando o resto da divisão pelos dias — garante um versículo diferente por dia sem repetir até esgotar o ciclo.

### `modules/audio_widget.py` — Narração

Renderiza botões de áudio via Web Speech API do navegador (não depende de nenhuma API externa de texto-para-fala). `renderizar_audio()` é o botão simples usado nas respostas do chat e no versículo do dia; `renderizar_audio_com_progresso()` adiciona uma estimativa de duração e barra de progresso, usada na leitura de capítulos.

### `modules/acoes_chat.py` — Copiar e compartilhar

Botões de ícone que copiam a resposta para a área de transferência ou abrem o menu de compartilhamento nativo do dispositivo (`navigator.share`, com fallback para copiar).

### `modules/fuso_horario.py` — Fuso horário do usuário

O servidor roda em UTC. Esse módulo detecta o offset de fuso do navegador via JavaScript (usando um campo de texto escondido preenchido por script) para exibir os horários das mensagens do chat no horário local de quem está usando o app.

### `data/construir-banco.py` — Indexação

Lê `biblia.json`, agrupa os versículos de cada capítulo em blocos de até 1.500 caracteres sem quebrar um versículo no meio, gera o embedding de cada bloco via NVIDIA NIM e popula a coleção do Chroma. Roda uma única vez, ou sempre que a fonte de dados mudar.

## Fluxo de uma pergunta

```
Usuário digita a pergunta (app.py)
        ↓
busca.buscar_versiculos(pergunta)
  - embedding da pergunta (NVIDIA NIM)
  - query no Chroma → até 40 trechos, cortando abaixo de 40% de similaridade
        ↓
resposta.gerar_resposta(pergunta, trechos)
  - monta prompt com os trechos como contexto
  - chat completion (NVIDIA NIM)
        ↓
app.py exibe resposta + referências consultadas
        ↓
(opcional) pergunta de acompanhamento
  - resposta.continuar_conversa reaproveita trechos + histórico, sem nova busca
```

## API usada

Todos os módulos que falam com a NVIDIA NIM usam o cliente `openai.OpenAI` apontado para o endpoint da NVIDIA (`base_url="https://integrate.api.nvidia.com/v1"`), autenticado com `NVIDIA_API_KEY`. É a mesma API para embeddings e chat completions, só muda o modelo.
