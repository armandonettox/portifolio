# Erros comuns

| Erro | Causa | Solução |
|------|-------|---------|
| `FileNotFoundError` | `.env` ausente | Copiar `.env.example` para `.env` |
| `AuthenticationError` | `NVIDIA_API_KEY` inválida | Verificar o valor no `.env` |
| `ModuleNotFoundError` | Dependência faltando | `pip install -r requirements.txt` |
| `FileNotFoundError: biblia-ave-maria.json` | Arquivo não copiado para `data/` | Copiar o JSON para a pasta `data/` |
