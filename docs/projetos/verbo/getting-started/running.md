# Rodando

## Construir o banco vetorial

Executar uma única vez, antes do primeiro uso (ou sempre que a fonte de dados mudar):

```bash
python scripts/construir_banco.py
```

Esse script lê `data/biblia.json`, agrupa os versículos por capítulo em blocos de até 1.500 caracteres, gera o embedding de cada bloco via NVIDIA NIM e popula o Chroma em `chroma-db/` (via `upsert`, então rodar de novo não duplica registros).

## Iniciar a aplicação

```bash
streamlit run app.py
```

## Rodar os testes

```bash
pytest tests/unit
```

Só testa `core/` — sem rede nem Streamlit, roda em segundos (é o que o GitHub Actions executa a cada push). `tests/integration/teste_conexao.py` faz uma chamada real à API e roda manualmente, fora do CI:

```bash
python tests/integration/teste_conexao.py
```

## Como usar

A tela inicial traz a caixa de busca e o versículo do dia. Ao perguntar algo:

1. A pergunta é transformada em embedding e comparada com os blocos de texto no Chroma — até 40 resultados voltam, descartando qualquer um abaixo de 40% de similaridade.
2. Os trechos encontrados entram no prompt enviado ao modelo de chat da NVIDIA NIM, que responde usando exclusivamente esse contexto.
3. A resposta aparece na tela, com botões para ouvir em áudio, copiar ou compartilhar, seguida da lista de referências consultadas na barra lateral.
4. Dá pra continuar a conversa com perguntas de acompanhamento, sem precisar repetir a busca.

Pela barra lateral também é possível escolher um livro e capítulo para ler o texto completo, com áudio narrado e barra de progresso.

!!! note "Sem invenção"
    O prompt instrui o modelo a responder só com base nos trechos fornecidos, e a dizer explicitamente quando eles não respondem à pergunta.
