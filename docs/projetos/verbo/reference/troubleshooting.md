# Erros comuns

| Erro | Causa | Solução |
|------|-------|---------|
| `FileNotFoundError` | `.secrets/.env` ausente | Copiar `.env.example` para `.secrets/.env` |
| `AuthenticationError` | `NVIDIA_API_KEY` inválida | Verificar o valor no `.secrets/.env` (ou em `st.secrets`, em produção) |
| `ModuleNotFoundError` | Dependência faltando | `pip install -r requirements.txt` (e `tests/requirements.txt` para rodar os testes) |
| `FileNotFoundError: biblia.json` | Arquivo não copiado para `data/` | Copiar o JSON para a pasta `data/` |
| Busca fica presa em "Buscando" | Falha na chamada à API da NVIDIA NIM (ex.: `503` sob uso intenso do free tier) | Tratada com toast de erro e nova tentativa; se persistir, aguardar e tentar de novo mais tarde |
| `chroma-db/` corrompido ou desatualizado | Mudança na fonte de dados sem reindexar | Apagar a pasta `chroma-db/` e rodar `python scripts/construir_banco.py` novamente |
