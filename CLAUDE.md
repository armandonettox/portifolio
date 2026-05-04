# Contexto do Projeto — Portfolio Armando Netto

## O que e este projeto

Portfolio pessoal em Python/Streamlit publicado em armandonetto.com.
Visual minimalista inspirado no site de Dario Amodei (darioamodei.com).

## Stack

- Python + Streamlit 1.55
- GitHub API para busca automatica de projetos e linguagens
- CSS customizado injetado via st.markdown (unsafe_allow_html=True)
- Fonte: Newsreader (Google Fonts, carregada via link tag)
- Deploy: Render (armandonetto.onrender.com) com dominio customizado via Cloudflare

## Arquitetura

Todo o app esta em um unico arquivo: `app.py`.

Estrutura do arquivo:
1. Imports e configuracao da pagina
2. Dark mode via st.query_params (?dark=1)
3. Configs de conteudo (PROJETOS_CONFIG, EXPERIENCIA, COMPETENCIAS)
4. Paleta de cores (duas variacoes: light e dark)
5. Injecao de fonte via link tag
6. CSS completo via st.markdown
7. Funcoes de busca na API do GitHub (com @st.cache_data ttl=3600)
8. Funcoes de render de HTML (render_lista, render_experiencia, render_competencias)
9. Secoes do portfolio em ordem: Header, Bio, Projetos, Competencias, Experiencia, Perfis, Contato

## Paleta de cores

```python
# Light mode
bg     = "#f0eee6"   # ivory (mesma do darioamodei.com)
text   = "#1f1e1d"
muted  = "#5e5d59"
border = "#d1cfc5"

# Dark mode
bg     = "#1f1e1d"
text   = "#f0eee6"
muted  = "#87867f"
border = "#3d3d3a"
```

## Dark mode

Implementado via query param (?dark=1 / ?dark=0).
O toggle e um elemento HTML puro (nao st.button) para evitar conflito com CSS do Streamlit.
O CSS inteiro e regenerado a cada mudanca de modo porque usa f-string com as variaveis de cor.

## Controle de conteudo

Tudo configuravel no topo do app.py sem mexer no resto do codigo:

- `PROJETOS_CONFIG` — sobrescreve titulo/descricao ou oculta repos do GitHub
- `ORDEM_PREFERIDA` — define quais repos aparecem primeiro
- `EXPERIENCIA` — lista de dicts com empresa, cargo e periodo
- `COMPETENCIAS` — dict aninhado: linguagem > subcategoria > lista de ferramentas

## Regras de CSS

- Todo CSS e injetado via st.markdown com unsafe_allow_html=True
- Usar !important em quase tudo — o Streamlit tem seletores agressivos
- Links: resetar com `a, a:visited, a:active { color: inherit !important; }`
- Nunca tentar estilizar componentes nativos do Streamlit (st.button, st.toggle) — usar HTML puro

## GitHub API

- Endpoint repos: GET /users/{usuario}/repos
- Endpoint linguagens: GET /repos/{usuario}/{repo}/languages
- Token opcional via GITHUB_TOKEN no .env — sem token: 60 req/hora, com token: 5000 req/hora
- Cache de 1 hora em todas as chamadas (@st.cache_data ttl=3600)

## Deploy

- Plataforma: Render (free tier)
- Start command: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
- Variavel de ambiente GITHUB_TOKEN configurada no painel do Render
- DNS: Cloudflare com dois CNAMEs (@ e www) apontando para armandonetto.onrender.com, proxy desligado

## Commits

Formato obrigatorio: tipo(escopo): descricao
Exemplos: feat(portfolio): adiciona secao de contato
          fix(css): corrige cor dos links no dark mode
