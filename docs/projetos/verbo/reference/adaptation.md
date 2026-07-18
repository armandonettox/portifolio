# Adaptação para outra fonte

O Verbo foi construído em torno da Bíblia Ave Maria, mas a arquitetura (Chroma + NVIDIA NIM + Streamlit) serve para qualquer RAG fechado sobre um texto fixo. Para adaptar:

1. **Substituir a fonte** — trocar `data/biblia-ave-maria.json` pelo arquivo desejado.
2. **Ajustar o parser** — `data/construir-banco.py` espera a estrutura específica do JSON da Bíblia Ave Maria; ajustar conforme o formato do novo arquivo.
3. **Atualizar o prompt** — `modules/resposta.py` tem uma instrução de sistema específica ("responda usando exclusivamente os versículos da Bíblia"); reescrever para refletir a nova fonte.

!!! tip "O que não muda"
    A lógica de busca por similaridade (`modules/busca.py`) e a integração com a NVIDIA NIM são genéricas — não dependem do conteúdo da Bíblia especificamente, só da estrutura `{texto, referencia}` de cada trecho indexado.
