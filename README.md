# Portfolio — Armando Netto

Portfolio pessoal construido com Python e Streamlit, com visual minimalista inspirado no site de Dario Amodei.

Acesse em: [armandonetto.com](https://armandonetto.com)

## Stack

- **Python** + **Streamlit 1.55**
- GitHub API — busca projetos e linguagens automaticamente
- CSS customizado com fonte Newsreader (Google Fonts)
- Deploy: Render + dominio proprio via Cloudflare

## Funcionalidades

- Dark/light mode com toggle pill
- Saudacao dinamica (bom dia/boa tarde/boa noite) por horario de Brasilia
- Projetos buscados automaticamente da API do GitHub com controle manual
- Secao de competencias em arvore hierarquica colapsavel
- Secao de experiencia com timeline por empresa
- Favicon personalizado

## Como rodar localmente

**1. Clone o repositorio**
```bash
git clone https://github.com/armandonettox/portifolio.git
cd portifolio
```

**2. Crie o ambiente virtual e instale as dependencias**
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

**3. Configure as variaveis de ambiente (opcional)**
```bash
copy .env.example .env
# Adicione seu GITHUB_TOKEN para aumentar o limite da API de 60 para 5000 req/hora
```

**4. Rode o app**
```bash
streamlit run app.py
```

## Configuracao de conteudo

Toda a customizacao fica no topo do `app.py`:

| Variavel | O que controla |
|----------|---------------|
| `PROJETOS_CONFIG` | Titulo, descricao e visibilidade dos repos do GitHub |
| `ORDEM_PREFERIDA` | Ordem de exibicao dos projetos |
| `EXPERIENCIA` | Historico profissional com timeline |
| `COMPETENCIAS` | Arvore de linguagens, subcategorias e ferramentas |
| `USUARIO_GITHUB` | Nome de usuario do GitHub para busca automatica |

## Estrutura

```
portifolio/
    app.py              <- codigo principal
    requirements.txt    <- dependencias
    .env.example        <- template de variaveis de ambiente
    .gitignore
    assets/
        logos/          <- favicon e logos
```

## Status

Em producao — [armandonetto.com](https://armandonetto.com)
