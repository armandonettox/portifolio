# Portfolio — Armando Netto

Portfolio pessoal construido com Python e Streamlit, com visual minimalista inspirado no site de Dario Amodei.

## Stack

- **Python** + **Streamlit**
- GitHub API (busca de projetos automaticamente)
- CSS customizado com fonte Newsreader (Google Fonts)

## Como rodar localmente

**1. Clone o repositorio**
```bash
git clone https://github.com/armandonettox/portifolio.git
cd portifolio
```

**2. Crie o ambiente virtual e instale as dependencias**
```bash
python -m venv .venv
.venv\Scripts\activate      # Windows
pip install streamlit requests python-dotenv
```

**3. Configure as variaveis de ambiente (opcional)**
```bash
copy .env.example .env
# Abra o .env e adicione seu GITHUB_TOKEN se quiser aumentar o limite da API
```

**4. Rode o app**
```bash
streamlit run app.py
```

## Configuracao

Toda a customizacao de conteudo fica no topo do `app.py`:

| Variavel | O que controla |
|----------|---------------|
| `PROJETOS_CONFIG` | Titulo, descricao e visibilidade dos repos |
| `ORDEM_PREFERIDA` | Ordem de exibicao dos projetos |
| `EXPERIENCIA` | Historico profissional |
| `COMPETENCIAS` | Arvore de linguagens e ferramentas |

## Status

Em desenvolvimento.
