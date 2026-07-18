# Rodando

## Construir o banco vetorial

Executar uma única vez, antes do primeiro uso (ou sempre que a fonte de dados mudar):

```bash
python data/construir-banco.py
```

Esse script lê `data/biblia-ave-maria.json`, gera os embeddings de cada versículo via NVIDIA NIM e popula o Chroma em `chroma-db/`.

## Iniciar a aplicação

```bash
streamlit run app.py
```

## Como usar

A interface é uma única caixa de pergunta. Ao digitar e enviar:

1. A pergunta é transformada em embedding e comparada com os versículos no Chroma — os 5 mais próximos são retornados.
2. Os versículos encontrados entram no prompt enviado ao modelo de chat da NVIDIA NIM, que responde usando exclusivamente esse contexto.
3. A resposta aparece na tela, seguida da lista dos versículos consultados (com referência).

!!! note "Sem invenção"
    O prompt instrui o modelo a responder só com base nos versículos fornecidos, e a dizer explicitamente quando eles não respondem à pergunta.
