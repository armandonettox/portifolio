# Arquitetura

## Estrutura do projeto

O código é organizado em `src/verbo/`, separando regras de negócio (testáveis sem depender do Streamlit) da camada de interface:

```
verbo/
    app.py                       <- entrypoint Streamlit (fino, so chama a UI)
    src/verbo/
        config.py                 <- variaveis de ambiente, nomes de modelo, paths
        core/                      <- regras de negocio, sem depender de streamlit
            busca.py                <- embeddings + busca semantica no ChromaDB
            resposta.py              <- chamadas ao LLM (resposta inicial e continuacao)
            erros.py                 <- mapeia falhas da API pra mensagens claras
            leitura.py                <- parsing dos capitulos e texto pra narracao
            plano_livre.py             <- agrupamento de capitulos por livro
            versiculo_dia.py           <- versiculo do dia, deterministico por data
            ingestao.py                <- chunking usado na construcao do banco vetorial
            util.py                     <- helpers puros (busca de capitulo, resumo de texto)
        ui/                        <- tudo que depende do streamlit
            pagina.py                <- composicao da pagina principal
            cache.py                  <- cache dos dados carregados do disco
            plano_livre.py             <- seletor de livro/capitulo na barra lateral
            audio_widget.py             <- narracao via Web Speech API
            acoes_chat.py                <- copiar e compartilhar a resposta
            fuso_horario.py               <- detecta o fuso do navegador
    scripts/
        construir_banco.py        <- roda uma unica vez pra popular o ChromaDB
    data/
        biblia.json              <- fonte validada (73 livros, 35.450 versiculos)
    assets/
        estilo.css                <- CSS externo, com variaveis para os dois temas
        templates/                 <- HTML/JS embutidos via components.html
    tests/
        unit/                    <- testam so o core, sem rede nem streamlit
        integration/               <- chamada real a API, roda manualmente
```

A separação existe pra deixar a lógica de negócio (busca, geração de resposta, regras do versículo do dia, ingestão) testável sem precisar simular o Streamlit ou fazer chamada de rede. `app.py` na raiz é só um entrypoint de poucas linhas — mantém o deploy no Streamlit Community Cloud sem reconfiguração, enquanto todo o código real vive no pacote.

## Módulos

### `app.py` — Entrypoint

Adiciona `src/` ao `sys.path` e chama `verbo.ui.pagina.render()`. Não contém lógica própria.

### `core/busca.py` — Busca por similaridade

**`buscar_versiculos(pergunta)`**

1. Gera o embedding da pergunta via NVIDIA NIM (`EMBEDDING_MODEL`).
2. Consulta a coleção do Chroma (`CHROMA_DB_PATH` / `COLLECTION_NAME`) com esse vetor, pedindo até `TOP_K` resultados.
3. Converte a distância L2 (embeddings normalizados) em similaridade de cosseno e descarta qualquer resultado abaixo de `SIMILARIDADE_MINIMA`. Como os resultados já vêm ordenados por distância crescente, o primeiro abaixo do limiar garante que os seguintes também estão.

### `core/resposta.py` — Geração da resposta

**`gerar_resposta(pergunta, versiculos)`** monta um prompt com os trechos encontrados como contexto e uma instrução explícita para responder **exclusivamente** com base neles, chama o modelo de chat da NVIDIA NIM (`CHAT_MODEL`) e retorna o texto da resposta.

**`continuar_conversa(...)`** reaproveita a pergunta e os trechos da busca original, mais o histórico de mensagens trocadas até agora, para responder a uma pergunta de acompanhamento sem rodar uma nova busca semântica.

### `core/erros.py` — Mensagens de erro

**`mensagem_erro_ia(excecao)`** mapeia o tipo da exceção pra uma mensagem específica em português, sem expor detalhes técnicos nem citar o provedor de IA:

| Exceção | Mensagem exibida |
|---|---|
| `openai.AuthenticationError` | Falha de autenticação com o serviço de IA |
| `openai.RateLimitError` | Limite de uso atingido, tentar em alguns minutos |
| `openai.APIConnectionError` / `APITimeoutError` | Falha de conexão, verificar a internet |
| `chromadb.errors.ChromaError` | Base de versículos indisponível |
| qualquer outra exceção | Mensagem genérica de busca não concluída |

`app.py` usa essa função em todo `except Exception` que envolve uma chamada à API, exibindo o resultado num `st.toast`.

### `core/leitura.py` — Texto completo

Carrega `biblia.json` inteiro e organiza por capítulo, com o texto formatado em markdown (`**1.** texto do versículo`). Usado tanto pela tela de leitura quanto por `texto_para_audio()`, que remove a marcação de número de versículo para gerar um texto corrido, adequado à narração.

### `core/plano_livre.py` — Navegação por livro e capítulo

**`listar_livros(capitulos)`** agrupa a lista de capítulos por livro. É lógica pura — a renderização do seletor (que depende do Streamlit) fica em `ui/plano_livre.py`.

### `core/versiculo_dia.py` — Versículo do dia

**`obter_versiculo_do_dia(versiculos, data)`** calcula qual versículo mostrar em cada data a partir de uma época fixa (1º de janeiro de 2026), usando o resto da divisão pelos dias — garante um versículo diferente por dia sem repetir até esgotar o ciclo. Recebe a lista de versículos já carregada (a leitura do arquivo, com cache, é responsabilidade de `ui/cache.py`).

### `core/ingestao.py` — Chunking

**`montar_chunks_capitulo(...)`** agrupa versículos de um capítulo em blocos de até 1.500 caracteres sem quebrar um versículo no meio. Usado por `scripts/construir_banco.py`.

### `ui/cache.py` — Cache dos dados

Envolve os carregadores puros de `core/leitura.py` e `core/versiculo_dia.py` com `@st.cache_data`, mantendo o `core/` livre de qualquer dependência do Streamlit.

### `ui/audio_widget.py` — Narração

Renderiza botões de áudio via Web Speech API do navegador (não depende de nenhuma API externa de texto-para-fala). `renderizar_audio()` é o botão simples usado nas respostas do chat e no versículo do dia; `renderizar_audio_com_progresso()` adiciona uma estimativa de duração e barra de progresso, usada na leitura de capítulos.

### `ui/acoes_chat.py` — Copiar e compartilhar

Botões de ícone que copiam a resposta para a área de transferência ou abrem o menu de compartilhamento nativo do dispositivo (`navigator.share`, com fallback para copiar).

### `ui/fuso_horario.py` — Fuso horário do usuário

O servidor roda em UTC. Esse módulo detecta o offset de fuso do navegador via JavaScript (usando um campo de texto escondido preenchido por script) para exibir os horários das mensagens do chat no horário local de quem está usando o app.

### `scripts/construir_banco.py` — Indexação

Lê `biblia.json` via `core/ingestao.py`, gera o embedding de cada bloco via NVIDIA NIM e popula a coleção do Chroma. Roda uma única vez, ou sempre que a fonte de dados mudar.

## Fluxo de uma pergunta

```
Usuario digita a pergunta (ui/pagina.py)
        ↓
core.busca.buscar_versiculos(pergunta)
  - embedding da pergunta (NVIDIA NIM)
  - query no Chroma -> até 40 trechos, cortando abaixo de 40% de similaridade
        ↓
core.resposta.gerar_resposta(pergunta, trechos)
  - monta prompt com os trechos como contexto
  - chat completion (NVIDIA NIM)
        ↓
ui/pagina.py exibe resposta + referencias consultadas
  - qualquer falha nas chamadas acima cai num except que usa
    core.erros.mensagem_erro_ia() pra mostrar um toast especifico
        ↓
(opcional) pergunta de acompanhamento
  - core.resposta.continuar_conversa reaproveita trechos + historico, sem nova busca
```

## Testes

`tests/unit/` cobre só `core/` — lógica pura, sem chamada de rede nem dependência do Streamlit, roda em segundos e no CI (GitHub Actions, a cada push). `tests/integration/teste_conexao.py` faz uma chamada real à API da NVIDIA e roda manualmente, fora do CI.

## API usada

Todo o pacote fala com a NVIDIA NIM através do client `openai.OpenAI`, apontado para o endpoint da NVIDIA (`base_url="https://integrate.api.nvidia.com/v1"`) e autenticado com `NVIDIA_API_KEY`. É a mesma API para embeddings e chat completions, só muda o modelo.
