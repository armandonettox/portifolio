from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, HRFlowable
)
from pathlib import Path

ACCENT = HexColor("#4a67b5")
DARK = HexColor("#1f1e1d")
MID = HexColor("#555555")
LIGHT = HexColor("#d1cfc5")

dst = Path(__file__).resolve().parent.parent / "docs" / "assets" / "cv.pdf"

doc = SimpleDocTemplate(
    str(dst),
    pagesize=A4,
    leftMargin=1.6*cm, rightMargin=1.6*cm,
    topMargin=1.2*cm, bottomMargin=1.2*cm,
    title="Armando Soares Lopes Netto - Curriculo",
    author="Armando Soares Lopes Netto",
)

styles = getSampleStyleSheet()

def s(name, parent=None, **kw):
    return ParagraphStyle(name, parent=parent or styles['Normal'], **kw)

style_h1 = s("h1", fontName="Helvetica-Bold", fontSize=19, leading=23, textColor=DARK,
             spaceAfter=2, alignment=TA_LEFT)
style_role = s("role", fontName="Helvetica-Bold", fontSize=10, textColor=ACCENT,
               spaceAfter=4, alignment=TA_LEFT)
style_contact = s("contact", fontName="Helvetica", fontSize=8.2, textColor=MID,
                  leading=11, spaceAfter=2, alignment=TA_LEFT)
style_h2 = s("h2", fontName="Helvetica-Bold", fontSize=10.5, textColor=DARK,
             spaceBefore=9, spaceAfter=1, alignment=TA_LEFT)
style_entry = s("entry", fontName="Helvetica", fontSize=9.3, textColor=DARK,
                leading=12, spaceBefore=4, spaceAfter=1)
style_body = s("body", fontName="Helvetica", fontSize=9.3, textColor=DARK,
               leading=12.5, alignment=TA_LEFT, spaceAfter=2)
style_bullet = s("bullet", fontName="Helvetica", fontSize=9.3, textColor=DARK,
                 leading=12, leftIndent=14, spaceAfter=1)
style_stack = s("stack", fontName="Helvetica-Oblique", fontSize=8.3, textColor=MID,
                leading=11, spaceAfter=2)

story = []

def rule(color=LIGHT, thickness=0.6, before=1, after=3):
    story.append(HRFlowable(width="100%", thickness=thickness, color=color,
                            spaceBefore=before, spaceAfter=after))

def section(title):
    story.append(Paragraph(title, style_h2))
    rule()

def entry(titulo, periodo):
    story.append(Paragraph(
        f'<font name="Helvetica-Bold">{titulo}</font> '
        f'<font name="Helvetica-Oblique" color="#777777" size="8.3">{periodo}</font>',
        style_entry))

def bullet(texto):
    story.append(Paragraph('<bullet>&#8226;</bullet>' + texto, style_bullet))

def stack(texto):
    story.append(Paragraph(f"Stack: {texto}", style_stack))

# Cabecalho
story.append(Paragraph("Armando Soares Lopes Netto", style_h1))
story.append(Paragraph("Cientista de Dados", style_role))
story.append(Paragraph(
    "Vitória, ES | (27) 99955-2186 | contato@armandonetto.com | "
    "linkedin.com/in/armandonettox | github.com/armandonettox | armandonetto.com",
    style_contact))

# Resumo
section("RESUMO")
story.append(Paragraph(
    "Cientista de Dados com base sólida em análise de dados e experiência prática levando "
    "estatística, machine learning e IA generativa a projetos reais — de previsão com "
    "scikit-learn a sistemas RAG em produção. Atua na Best Senior estruturando análises e "
    "automações para operadora de saúde. Cursando Ciência de Dados na Estácio.",
    style_body))

# Experiencia
section("EXPERIÊNCIA")
entry("Best Senior — Analista de Dados", "jan 2026 – atual")
bullet("Construção de análises, dashboards e indicadores para apoiar decisão de negócio em operadora de saúde.")
bullet("Estruturação de fluxos automatizados que eliminam etapas manuais repetitivas.")
entry("Best Senior — Assistente de Credenciamento", "jun 2023 – dez 2025")
bullet("Atuação em processos de credenciamento de prestadores de saúde.")
entry("AutoGiva — Assistente Administrativo", "nov 2021 – ago 2022")
bullet("Suporte administrativo e operacional.")

# Projetos
section("PROJETOS")
entry("FIFA World Cup — análise histórica e previsão de desempenho (1930–2026)", "")
bullet("Análise exploratória e modelagem preditiva com scikit-learn sobre dataset histórico de "
       "Copas do Mundo, com pipeline de dados brutos -&gt; tratados -&gt; dashboard.")
bullet("Dashboard interativo em Streamlit para apresentar padrões e previsões de desempenho de seleções.")
stack("Python, pandas, scikit-learn, Streamlit")
entry("Verbo — RAG fechado sobre a Bíblia Ave Maria (35.450 versículos, 73 livros)", "")
bullet("Pipeline RAG completo: banco vetorial ChromaDB, embeddings e geração via NVIDIA NIM, "
       "busca por similaridade (top-5) e resposta restrita à fonte, citando livro/capítulo/versículo.")
stack("Python, ChromaDB, NVIDIA NIM, Streamlit")
entry("Soundblend — automação de organização de playlists via API do Spotify", "")
bullet("App Streamlit com OAuth que identifica gênero musical via MusicBrainz e distribui "
       "músicas curtidas entre playlists por regras configuráveis.")
bullet("Sincronização incremental em lotes de 100 itens, com preview e desfazer.")
stack("Python, Streamlit, Spotify API, OAuth")
entry("Hera (em desenvolvimento) — assistente pessoal via Telegram/WhatsApp", "")
bullet("Automação de organização financeira pessoal com portal web de acompanhamento.")

# Formacao
section("FORMAÇÃO")
entry("Estácio — CST Ciência de Dados", "jan 2025 – dez 2027 (cursando)")

# Cursos
section("CURSOS E CERTIFICAÇÕES")
story.append(Paragraph("Formação Cientista de Dados: O Curso Completo — Udemy, 2025", style_body))
story.append(Paragraph("Data Science: explorando e analisando dados — Alura, 2026", style_body))
story.append(Paragraph("Introdução à Análise de Dados com a Randstad — DIO, 2025", style_body))

# Habilidades
section("HABILIDADES")
for cat, itens in [
    ("SQL", "BigQuery, AWS Athena, PostgreSQL, Oracle"),
    ("Python", "pandas, numpy, scikit-learn, matplotlib, seaborn, plotly, Streamlit"),
    ("R", "ggplot2, dplyr"),
    ("IA / LLM", "RAG, embeddings, ChromaDB, NVIDIA NIM, OpenAI API"),
    ("BI", "Power BI, Tableau, Metabase"),
    ("Engenharia", "FastAPI, Docker, OAuth, APIs REST, Git, GitHub Actions, Nginx, Selenium, htmx, systemd"),
]:
    story.append(Paragraph(f'<font name="Helvetica-Bold">{cat}:</font> {itens}', style_body))

# Idiomas
section("IDIOMAS")
story.append(Paragraph("Português: Nativo", style_body))
story.append(Paragraph("Inglês: Intermediário", style_body))

doc.build(story)
print(f"PDF gerado: {dst} ({dst.stat().st_size} bytes)")
