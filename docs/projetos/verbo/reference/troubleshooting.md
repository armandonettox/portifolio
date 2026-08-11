# Erros comuns

## Instalação e configuração

| Erro | Causa | Solução |
|------|-------|---------|
| `FileNotFoundError` | `.secrets/.env` ausente | Copiar `.env.example` para `.secrets/.env` |
| `ModuleNotFoundError` | Dependência faltando | `pip install -r requirements.txt` (e `tests/requirements.txt` para rodar os testes) |
| `FileNotFoundError: biblia.json` | Arquivo não copiado para `data/` | Copiar o JSON para a pasta `data/` |
| `chroma-db/` corrompido ou desatualizado | Mudança na fonte de dados sem reindexar | Apagar a pasta `chroma-db/` e rodar `python scripts/construir_banco.py` novamente |

## Falhas na chamada à API, em tempo de uso

Cada tipo de falha na chamada à NVIDIA NIM ou ao ChromaDB mostra uma mensagem específica pro usuário (`core/erros.py`), sem travar a tela nem expor detalhes técnicos:

**Falha de autenticação** (chave inválida ou ausente):

![Toast de erro de autenticacao](../assets/screenshots/erro_auth.png)

**Limite de uso da API atingido:**

![Toast de limite de uso atingido](../assets/screenshots/erro_rate_limit.png)

**Falha de conexão:**

![Toast de falha de conexao](../assets/screenshots/erro_conexao.png)

**Banco vetorial indisponível:**

![Toast de banco vetorial indisponivel](../assets/screenshots/erro_chroma.png)

**Qualquer outra falha:**

![Toast de erro generico](../assets/screenshots/erro_generico.png)

## Quando o servidor cai

Se a conexão com o servidor do Streamlit cai (deploy em andamento, processo reiniciando, etc.), a interface passa a mostrar os campos desabilitados e um ícone de sem-conexão no botão de busca, em vez de travar sem explicação:

![Interface com campos desabilitados durante perda de conexao com o servidor](../assets/screenshots/servidor_indisponivel.png)

Esse é o comportamento padrão do Streamlit ao perder o websocket com o servidor — a página tenta reconectar automaticamente quando o servidor volta.
