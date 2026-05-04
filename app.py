import os
import streamlit as st
import requests
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv

load_dotenv()

# Token do GitHub — opcional, mas aumenta o limite de 60 para 5000 req/hora
_GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
_GITHUB_HEADERS = {"Authorization": f"Bearer {_GITHUB_TOKEN}"} if _GITHUB_TOKEN else {}

st.set_page_config(
    page_title="Armando Netto",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Dark mode via query param: ?dark=1
dark = st.query_params.get("dark", "0") == "1"
toggle_href = "?dark=0" if dark else "?dark=1"

# ─── Controle manual dos projetos ────────────────────────────────────────────
#
# Adicione entradas pelo nome exato do repositorio no GitHub.
#
# Campos disponiveis:
#   titulo      -> nome exibido no portfolio (padrao: nome do repo formatado)
#   descricao   -> texto exibido  (padrao: descricao do GitHub)
#   ocultar     -> True para nao exibir o repo
#
# Repos nao listados aqui aparecem automaticamente com dados do GitHub.
#
PROJETOS_CONFIG = {
    "transcol_opex_analytics": {
        "titulo": "Transcol OPEX Analytics",
        "descricao": "Analise de custos operacionais do sistema de transporte coletivo do Espirito Santo.",
    },
    "Armandonettox": {"ocultar": True},
    "armandonettox": {"ocultar": True},
    "portifolio": {"ocultar": True},
    # Para ocultar um repo: "nome_do_repo": {"ocultar": True}
    # Para sobrescrever titulo/descricao: "nome_do_repo": {"titulo": "...", "descricao": "..."}
}

# Repos listados aqui aparecem primeiro, na ordem definida.
# Os demais aparecem depois, ordenados por data de atualizacao no GitHub.
ORDEM_PREFERIDA = [
    "transcol_opex_analytics",
]

USUARIO_GITHUB = "armandonettox"

# ─── Competencias ─────────────────────────────────────────────────────────────
COMPETENCIAS = {
    "Python": {
        "Analise de dados": ["pandas", "numpy"],
        "Visualizacao": ["matplotlib", "seaborn", "plotly"],
        "Automacao": ["selenium"],
    },
    "SQL": {
        "Consulta e transformacao": ["BigQuery", "AWS Athena"],
    },
    "R": {
        "Analise estatistica": ["ggplot2", "dplyr"],
    },
    "Ferramentas": {
        "Dashboards": ["Streamlit", "Power BI", "Tableau"],
        "Versionamento": ["Git", "GitHub"],
        "Cloud": ["AWS", "Google Cloud"],
    },
}

# ─── Experiencia profissional ─────────────────────────────────────────────────
EXPERIENCIA = [
    {
        "empresa": "Best Senior",
        "cargo": "Analista de Dados",
        "periodo": "jan 2026 — presente",
    },
    {
        "empresa": "Best Senior",
        "cargo": "Assistente de Credenciamento",
        "periodo": "jun 2023 — dez 2025",
    },
    {
        "empresa": "AutoGiva",
        "cargo": "Assistente Administrativo",
        "periodo": "nov 2021 — ago 2022",
    },
]

# ─── Saudacao dinamica por horario (Brasilia UTC-3) ──────────────────────────
_hora = datetime.now(timezone(timedelta(hours=-3))).hour
if 5 <= _hora < 12:
    SAUDACAO = "Bom dia."
elif 12 <= _hora < 18:
    SAUDACAO = "Boa tarde."
else:
    SAUDACAO = "Boa noite."

# ─── Paleta de cores (mesma do darioamodei.com) ───────────────────────────────
if dark:
    bg       = "#1f1e1d"   # slate-dark
    text     = "#f0eee6"   # ivory-medium
    muted    = "#87867f"   # cloud-dark
    border   = "#3d3d3a"   # slate-medium
    hover    = "#b0aea5"   # cloud-medium
    toggle_l = "#b0aea5"
else:
    bg       = "#f0eee6"   # ivory-medium
    text     = "#1f1e1d"   # slate-dark
    muted    = "#5e5d59"   # slate-light
    border   = "#d1cfc5"   # cloud-light
    hover    = "#5e5d59"
    toggle_l = "#5e5d59"

# ─── Fonte — injetada como <link> para garantir carregamento ─────────────────
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,300;0,6..72,400;0,6..72,500;1,6..72,300;1,6..72,400&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# ─── CSS ──────────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>

/* Esconder chrome do Streamlit */
#MainMenu, header, footer                   {{ display: none !important; }}
[data-testid="stToolbar"]                  {{ display: none !important; }}
[data-testid="stDecoration"]               {{ display: none !important; }}
[data-testid="stStatusWidget"]             {{ display: none !important; }}
.stDeployButton                            {{ display: none !important; }}
section[data-testid="stSidebar"]           {{ display: none !important; }}
[data-testid="stAppViewBlockContainer"]    {{ padding-top: 0 !important; }}

/* Body, fundo e fonte global */
html, body, .stApp, [data-testid="stAppViewContainer"] {{
    background-color: {bg} !important;
    font-family: 'Newsreader', Georgia, 'Times New Roman', serif !important;
    color: {text} !important;
}}

/* Forca a fonte em todos os elementos de texto do Streamlit */
p, span, div, li, a, h1, h2, h3, h4, h5, h6, label, button {{
    font-family: 'Newsreader', Georgia, 'Times New Roman', serif !important;
}}

/* Container principal — estreito como o site do Dario */
.block-container {{
    max-width: 640px !important;
    padding: 3.5rem 1.5rem 6rem !important;
    margin: 0 auto !important;
    background-color: {bg} !important;
}}

/* Transparencia em todos os wrappers intermediarios */
.stMarkdown, div[data-testid="column"],
div[data-testid="stVerticalBlock"],
div[data-testid="stHorizontalBlock"] {{
    background: transparent !important;
}}

/* Reset global de links — evita o azul padrao do browser/Streamlit */
a, a:visited, a:active,
.stMarkdown a,
.stMarkdown a:visited,
.stMarkdown a:active {{
    color: inherit !important;
    text-decoration: none !important;
}}

/* ── Componentes do portfolio ── */

.pf-header {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 0;
}}

.pf-name {{
    font-family: 'Newsreader', Georgia, serif;
    font-size: 1.05rem;
    font-weight: 500;
    color: {text} !important;
    text-decoration: none !important;
    letter-spacing: -0.01em;
    line-height: 1;
}}
.pf-name:hover {{
    color: {muted} !important;
}}

.pf-nav-link {{
    font-family: 'Newsreader', Georgia, serif;
    font-size: 0.9rem;
    font-weight: 300;
    color: {muted} !important;
    text-decoration: none !important;
    transition: color 0.15s;
}}
.pf-nav-link:hover {{ color: {text} !important; }}

/* Toggle dark/light — pill HTML puro, sem Streamlit */
.pf-toggle {{
    display: inline-flex;
    align-items: center;
    text-decoration: none !important;
    cursor: pointer;
}}
.pf-toggle-track {{
    display: inline-block;
    width: 44px;
    height: 24px;
    background-color: {'#555' if dark else border};
    border-radius: 12px;
    position: relative;
    transition: background-color 0.2s;
    flex-shrink: 0;
}}
.pf-toggle-thumb {{
    position: absolute;
    top: 3px;
    left: {'23px' if dark else '3px'};
    width: 18px;
    height: 18px;
    background-color: {'#fff' if dark else text};
    border-radius: 50%;
    transition: left 0.2s;
}}

/* Elimina gap extra entre elementos Streamlit */
.stMarkdown + .stMarkdown {{
    margin-top: 0 !important;
}}
div[data-testid="stVerticalBlock"] > div {{
    gap: 0 !important;
}}

/* Bio */
.pf-bio {{
    font-family: 'Newsreader', Georgia, serif;
    font-size: 1rem;
    font-weight: 300;
    line-height: 1.75;
    color: {text};
    margin-top: 1.2rem;
}}
.pf-bio strong {{
    font-weight: 500;
}}

/* Secao */
.pf-section {{
    margin-top: 1.2rem;
}}

.pf-section-title {{
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: {muted};
    margin-bottom: 0.6rem;
    padding-bottom: 0.4rem;
    border-bottom: 1px solid {border};
}}

/* Lista de itens */
.pf-list {{
    list-style: none;
    padding: 0;
    margin: 0;
}}

.pf-item {{
    display: flex;
    align-items: baseline;
    flex-wrap: wrap;
    column-gap: 0.45rem;
    row-gap: 0;
    padding: 0.32rem 0;
    font-family: 'Newsreader', Georgia, serif;
    font-size: 0.97rem;
    font-weight: 300;
    line-height: 1.5;
    border-bottom: 1px solid transparent;
}}
.pf-item:last-child {{ border-bottom: none; }}

.pf-bullet {{
    color: {muted};
    flex-shrink: 0;
    font-size: 0.75em;
    line-height: 2;
    user-select: none;
}}

a.pf-link,
a.pf-link:link,
a.pf-link:visited,
a.pf-link:active {{
    color: {text} !important;
    text-decoration: none !important;
    border-bottom: 1px solid {border};
    transition: border-color 0.15s, color 0.15s;
}}
a.pf-link:hover {{
    color: {muted} !important;
    border-bottom-color: {muted};
}}

.pf-desc {{
    color: {muted};
    font-size: 0.9rem;
    font-style: italic;
}}

.pf-meta {{
    color: {muted};
    font-size: 0.8rem;
    font-weight: 300;
    white-space: nowrap;
    flex-shrink: 0;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    font-style: normal;
}}

/* Experiencia — timeline */
.pf-exp-list {{
    list-style: none;
    padding: 0;
    margin: 0;
    display: flex;
    flex-direction: column;
    gap: 1.2rem;
}}
.pf-exp-group {{
    display: flex;
    flex-direction: column;
    gap: 0;
}}
.pf-exp-empresa {{
    font-family: 'Newsreader', Georgia, serif;
    font-size: 0.88rem;
    font-weight: 500;
    color: {muted};
    text-transform: uppercase;
    letter-spacing: 0.04em;
    margin-bottom: 0.4rem;
}}
.pf-exp-roles {{
    display: flex;
    flex-direction: column;
    position: relative;
    padding-left: 1.4rem;
}}
/* linha vertical */
.pf-exp-roles::before {{
    content: '';
    position: absolute;
    left: 5px;
    top: 7px;
    bottom: 7px;
    width: 1px;
    background-color: {border};
}}
.pf-exp-role {{
    position: relative;
    padding: 0 0 0.9rem 0;
}}
.pf-exp-role:last-child {{
    padding-bottom: 0;
}}
/* dot */
.pf-exp-role::before {{
    content: '';
    position: absolute;
    left: -1.4rem;
    top: 6px;
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background-color: {border};
    border: 1.5px solid {muted};
}}
.pf-exp-cargo {{
    font-family: 'Newsreader', Georgia, serif;
    font-size: 0.97rem;
    font-weight: 400;
    color: {text};
    display: block;
}}
.pf-exp-periodo {{
    font-family: 'Newsreader', Georgia, serif;
    font-size: 0.85rem;
    font-weight: 300;
    color: {muted};
    display: block;
    margin-top: 0.1rem;
}}

/* Competencias — arvore colapsavel */
.pf-tree {{
    list-style: none;
    padding: 0;
    margin: 0;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}}
.pf-tree details {{
    border: none;
    outline: none;
}}
.pf-tree summary {{
    font-family: 'Newsreader', Georgia, serif;
    font-size: 0.97rem;
    font-weight: 500;
    color: {text};
    cursor: pointer;
    list-style: none;
    display: flex;
    align-items: center;
    gap: 0.4rem;
    user-select: none;
    padding: 0.1rem 0;
}}
.pf-tree summary::-webkit-details-marker {{ display: none; }}
.pf-tree summary::before {{
    content: '▸';
    font-size: 0.6rem;
    color: {muted};
    transition: transform 0.15s;
    flex-shrink: 0;
    line-height: 1;
}}
.pf-tree details[open] summary::before {{
    transform: rotate(90deg);
}}
.pf-tree summary:hover {{
    color: {muted};
}}
.pf-tree-subcategories {{
    list-style: none;
    padding: 0;
    margin: 0.3rem 0 0.2rem 1rem;
    border-left: 1px solid {border};
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
}}
.pf-tree-sub {{
    position: relative;
    padding-left: 0.9rem;
}}
.pf-tree-sub::before {{
    content: '';
    position: absolute;
    left: 0;
    top: 0.6em;
    width: 0.6rem;
    height: 1px;
    background-color: {border};
}}
.pf-tree-sublabel {{
    font-family: 'Newsreader', Georgia, serif;
    font-size: 0.88rem;
    font-weight: 300;
    color: {muted};
    font-style: italic;
}}
.pf-tree-items {{
    display: inline;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    font-size: 0.78rem;
    color: {muted};
    font-weight: 300;
}}

/* Estado de carregamento / erro */
.pf-status {{
    font-family: 'Newsreader', Georgia, serif;
    font-size: 0.9rem;
    font-style: italic;
    color: {muted};
    padding: 0.4rem 0;
}}
</style>
""", unsafe_allow_html=True)

# ─── Busca repos do GitHub ────────────────────────────────────────────────────
@st.cache_data(ttl=3600)
def buscar_repos(usuario: str):
    try:
        r = requests.get(
            f"https://api.github.com/users/{usuario}/repos",
            params={"per_page": 100, "sort": "updated"},
            headers=_GITHUB_HEADERS,
            timeout=5,
        )
        r.raise_for_status()
        return r.json(), None
    except requests.exceptions.Timeout:
        return None, "Tempo limite ao conectar com o GitHub."
    except Exception as e:
        return None, str(e)


@st.cache_data(ttl=3600)
def buscar_linguagens(usuario: str, repo_nome: str) -> list[str]:
    """Retorna lista de linguagens usadas no repo, ordenadas por uso."""
    try:
        r = requests.get(
            f"https://api.github.com/repos/{usuario}/{repo_nome}/languages",
            headers=_GITHUB_HEADERS,
            timeout=5,
        )
        r.raise_for_status()
        langs = r.json()  # {"Python": 12345, "Shell": 678, ...}
        return list(langs.keys())
    except Exception:
        return []


def _formatar(nome: str, repo: dict, cfg: dict) -> dict:
    titulo_raw = nome.replace("_", " ").replace("-", " ").title()
    # Usa descricao do config se existir; senao usa a do GitHub so se parecer util
    desc_github = repo.get("description") or ""
    desc_cfg    = cfg.get("descricao", "")
    descricao   = desc_cfg if desc_cfg else desc_github
    return {
        "titulo": cfg.get("titulo", titulo_raw),
        "descricao": descricao,
        "url": repo["html_url"],
        "nome": nome,
    }


def montar_projetos(repos_raw: list) -> list:
    repos = {r["name"]: r for r in repos_raw if not r.get("fork")}
    projetos, vistos = [], set()

    for nome in ORDEM_PREFERIDA:
        cfg = PROJETOS_CONFIG.get(nome, {})
        vistos.add(nome)
        if cfg.get("ocultar") or nome not in repos:
            continue
        projetos.append(_formatar(nome, repos[nome], cfg))

    for nome, repo in repos.items():
        if nome in vistos:
            continue
        cfg = PROJETOS_CONFIG.get(nome, {})
        if cfg.get("ocultar"):
            continue
        projetos.append(_formatar(nome, repo, cfg))

    return projetos


def render_lista(projetos: list, usuario: str) -> str:
    items = ""
    for p in projetos:
        langs = buscar_linguagens(usuario, p["nome"])
        meta  = f'<span class="pf-meta">({", ".join(langs)})</span>' if langs else ""
        desc  = f'<span class="pf-desc"> — {p["descricao"]}</span>' if p["descricao"] else ""
        items += f"""
        <li class="pf-item">
            <span class="pf-bullet">&#x2022;</span>
            <a href="{p['url']}" target="_blank" class="pf-link">{p['titulo']}</a>{desc}{meta}
        </li>"""
    return f'<ul class="pf-list">{items}</ul>'

# ─── Header ───────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="pf-header">
    <a href="/" class="pf-name">Armando Netto</a>
    <a href="{toggle_href}" class="pf-toggle" title="Alternar modo escuro">
        <span class="pf-toggle-track">
            <span class="pf-toggle-thumb"></span>
        </span>
    </a>
</div>
""", unsafe_allow_html=True)

# ─── Bio ──────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="pf-bio">
    <p>
        <span style="font-style:italic; color:{muted};">{SAUDACAO}</span>
    </p>
    <p>
        Graduando em Ci&ecirc;ncia de Dados e entusiasta do universo anal&iacute;tico,
        possuo s&oacute;lida base em matem&aacute;tica. Sou um entusiasta da
        democratiza&ccedil;&atilde;o de dados, priorizando o desenvolvimento de solu&ccedil;&otilde;es
        de alto impacto atrav&eacute;s de ferramentas open-source e arquiteturas de baixo custo.
    </p>
    <p>
        Minha atua&ccedil;&atilde;o combina o poder anal&iacute;tico de
        <strong>Python</strong>, <strong>R</strong> e <strong>SQL</strong>
        para arquitetar solu&ccedil;&otilde;es que v&atilde;o al&eacute;m do convencional.
        Seja explorando padr&otilde;es com Pandas e Seaborn ou automatizando processos
        com Selenium, meu objetivo &eacute; um s&oacute;: transformar dados em ativos
        estrat&eacute;gicos. Sou um defensor do uso de ferramentas de c&oacute;digo aberto
        para democratizar a an&aacute;lise de dados, entregando resultados de impacto real
        com o menor custo operacional poss&iacute;vel.
    </p>
</div>
""", unsafe_allow_html=True)

# ─── Projetos ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="pf-section">
    <div class="pf-section-title">Projetos</div>
""", unsafe_allow_html=True)

repos_raw, erro = buscar_repos(USUARIO_GITHUB)

if erro:
    st.markdown(f'<div class="pf-status">Erro ao buscar projetos: {erro}</div>', unsafe_allow_html=True)
elif not repos_raw:
    st.markdown('<div class="pf-status">Nenhum repositorio encontrado.</div>', unsafe_allow_html=True)
else:
    projetos = montar_projetos(repos_raw)
    if projetos:
        st.markdown(render_lista(projetos, USUARIO_GITHUB), unsafe_allow_html=True)
    else:
        st.markdown('<div class="pf-status">Nenhum projeto para exibir.</div>', unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ─── Competencias ─────────────────────────────────────────────────────────────
def render_competencias(comp: dict) -> str:
    items = ""
    for lang, subcats in comp.items():
        subs = ""
        for sublabel, libs in subcats.items():
            libs_str = " · ".join(libs)
            subs += f"""
            <li class="pf-tree-sub">
                <span class="pf-tree-sublabel">{sublabel}</span>
                <span class="pf-tree-items"> — {libs_str}</span>
            </li>"""
        items += f"""
        <li>
            <details>
                <summary>{lang}</summary>
                <ul class="pf-tree-subcategories">{subs}</ul>
            </details>
        </li>"""
    return f'<ul class="pf-tree">{items}</ul>'

st.markdown(f"""
<div class="pf-section">
    <div class="pf-section-title">Competências</div>
    {render_competencias(COMPETENCIAS)}
</div>
""", unsafe_allow_html=True)

# ─── Experiencia ──────────────────────────────────────────────────────────────
def render_experiencia(exp: list) -> str:
    # Agrupa mantendo a ordem de aparicao
    grupos: dict[str, list] = {}
    for e in exp:
        grupos.setdefault(e["empresa"], []).append(e)

    html = '<ul class="pf-exp-list">'
    for empresa, roles in grupos.items():
        roles_html = ""
        for r in roles:
            roles_html += f"""
            <div class="pf-exp-role">
                <span class="pf-exp-cargo">{r['cargo']}</span>
                <span class="pf-exp-periodo">{r['periodo']}</span>
            </div>"""
        html += f"""
        <li class="pf-exp-group">
            <div class="pf-exp-empresa">{empresa}</div>
            <div class="pf-exp-roles">{roles_html}</div>
        </li>"""
    html += "</ul>"
    return html

st.markdown(f"""
<div class="pf-section">
    <div class="pf-section-title">Experiência</div>
    {render_experiencia(EXPERIENCIA)}
</div>
""", unsafe_allow_html=True)

# ─── Perfis ───────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="pf-section">
    <div class="pf-section-title">Perfis</div>
    <ul class="pf-list">
        <li class="pf-item">
            <span class="pf-bullet">&#x2022;</span>
            <a href="https://github.com/{USUARIO_GITHUB}" target="_blank" class="pf-link">GitHub</a>
            <span class="pf-meta">(github.com/{USUARIO_GITHUB})</span>
        </li>
        <li class="pf-item">
            <span class="pf-bullet">&#x2022;</span>
            <a href="https://www.linkedin.com/in/armandonettox/" target="_blank" class="pf-link">LinkedIn</a>
            <span class="pf-meta">(linkedin.com/in/armandonettox)</span>
        </li>
    </ul>
</div>
""", unsafe_allow_html=True)

# ─── Contato ──────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="pf-section">
    <div class="pf-section-title">Contato</div>
    <ul class="pf-list">
        <li class="pf-item">
            <span class="pf-bullet">&#x2022;</span>
            <a href="mailto:contato@armandonetto.com" class="pf-link">contato@armandonetto.com</a>
        </li>
    </ul>
</div>
""", unsafe_allow_html=True)
