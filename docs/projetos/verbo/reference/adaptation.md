# Adaptação para outra fonte

O Verbo foi construído em torno de uma Bíblia específica, mas a arquitetura (Chroma + NVIDIA NIM + Streamlit) serve para qualquer RAG fechado sobre um texto fixo dividido em unidades menores (versículos, artigos, parágrafos numerados). Para adaptar:

1. **Substituir a fonte** — trocar `data/biblia.json` pelo arquivo desejado.
2. **Ajustar o parser** — `scripts/construir_banco.py` chama `carregar_capitulos_para_ingestao()` (em `src/verbo/core/ingestao.py`), que espera a estrutura específica do JSON atual (testamentos, livros, capítulos, versículos); ajustar conforme o formato do novo arquivo. A lógica de agrupamento em blocos (`montar_chunks_capitulo()`, no mesmo módulo) é genérica e pode ser reaproveitada.
3. **Atualizar o prompt** — `src/verbo/core/resposta.py` tem instruções específicas ("responda usando exclusivamente os versículos da Bíblia"); reescrever para refletir a nova fonte.
4. **Ajustar `core/leitura.py` e `core/plano_livre.py`** — a navegação por livro/capítulo e a formatação do texto de leitura também assumem a estrutura da Bíblia; adaptar para a hierarquia do novo conteúdo (ou remover, se a nova fonte não precisar de leitura completa).

!!! tip "O que não muda"
    A lógica de busca por similaridade (`core/busca.py`) e a integração com a NVIDIA NIM são genéricas — não dependem do conteúdo da Bíblia especificamente, só da estrutura `{texto, referencia}` de cada bloco indexado. Os módulos de UI (`ui/audio_widget.py`, `ui/acoes_chat.py`) também são independentes do conteúdo, e funcionam com qualquer texto.
