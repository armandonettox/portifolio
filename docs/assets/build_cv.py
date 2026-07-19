from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor, black
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether
)
from pathlib import Path

ACCENT = HexColor("#4a67b5")
DARK = HexColor("#1f1e1d")
MID = HexColor("#555555")
LIGHT = HexColor("#d1cfc5")

dst = Path("docs/assets/cv.pdf")

doc = SimpleDocTemplate(
    str(dst),
    pagesize=A4,
    leftMargin=1.8*cm, rightMargin=1.8*cm,
    topMargin=1.6*cm, bottomMargin=1.6*cm,
    title="Armando Netto - Curriculo",
    author="Armando Netto",
)

styles = getSampleStyleSheet()

def s(name, parent=None, **kw):
    return ParagraphStyle(name, parent=parent or styles['Normal'], **kw)

style_h1 = s("h1", fontName="Helvetica", fontSize=22, leading=26, textColor=DARK,
             spaceAfter=2, alignment=TA_LEFT)
style_role = s("role", fontName="Helvetica-Bold", fontSize=9.5, textColor=ACCENT,
               spaceAfter=6, alignment=TA_LEFT)
style_contact = s("contact", fontName="Helvetica", fontSize=8.5, textColor=MID,
                  spaceAfter=2, alignment=TA_LEFT)
style_h2 = s("h2", fontName="Helvetica-Bold", fontSize=11, textColor=ACCENT,
             spaceBefore=12, spaceAfter=4, alignment=TA_LEFT)
style_h3 = s("h3", fontName="Helvetica-Bold", fontSize=9.5, textColor=MID,
             spaceBefore=6, spaceAfter=2, alignment=TA_LEFT)
style_body = s("body", fontName="Helvetica", fontSize=10, textColor=DARK,
               leading=14, alignment=TA_LEFT, spaceAfter=4)
style_bullet_title = s("btitle", fontName="Helvetica-Bold", fontSize=10,
                       textColor=DARK, leading=13)
style_bullet_period = s("bperiod", fontName="Helvetica", fontSize=8.5,
                         textColor=MID)
style_bullet_desc = s("bdesc", fontName="Helvetica", fontSize=9.5,
                       textColor=DARK, leading=12, spaceAfter=4)
style_skill_cat = s("skillcat", fontName="Helvetica-Bold", fontSize=8.5,
                    textColor=ACCENT, spaceAfter=1)
style_skill_items = s("skillitems", fontName="Helvetica", fontSize=9.5,
                      textColor=DARK, leading=12, spaceAfter=4)
style_footer = s("footer", fontName="Helvetica-Oblique", fontSize=8,
                 textColor=MID, alignment=TA_CENTER, spaceBefore=12)

story = []

# Cabeecalho
story.append(Paragraph("Armando Netto", style_h1))
story.append(Paragraph("Analista de Dados . Cientista de Dados . Engenheiro de Dados", style_role))
story.append(Paragraph("contato@armandonetto.com  |  linkedin.com/in/armandonettox  |  github.com/armandonettox  |  armandonetto.com", style_contact))
story.append(HRFlowable(width="100%", thickness=1.4, color=ACCENT, spaceBefore=2, spaceAfter=10))

# Resumo
story.append(Paragraph("Resumo", style_h2))
story.append(HRFlowable(width="100%", thickness=0.4, color=LIGHT, spaceBefore=0, spaceAfter=4))
story.append(Paragraph(
    "Profissional de dados com atuacao em analise, automacao, IA aplicada e Machine Learning. "
    "Experiencia construindo dashboards, fluxos automatizados e produtos internos em contexto de "
    "operadora de saude. Desenvolve projetos pessoais que conectam dados e aplicacoes web.",
    style_body))

# Experiencia
story.append(Paragraph("Experiencia", style_h2))
story.append(HRFlowable(width="100%", thickness=0.4, color=LIGHT, spaceBefore=0, spaceAfter=4))

story.append(Paragraph("BEST SENIOR", style_h3))

role_line_best_an = Paragraph(
    '<bullet color="#4a67b5">&#8226;</bullet>&nbsp;&nbsp;'
    '<font name="Helvetica-Bold" color="#1f1e1d">Analista de Dados</font> '
    '<font color="#777777" size="8.5">jan 2026 - presente</font>',
    style_bullet_desc)
role_desc_best_an = Paragraph(
    "Construcao de analises, dashboards e fluxos automatizados no contexto de operadora de saude.",
    style_bullet_desc)

role_line_best_as = Paragraph(
    '<bullet color="#4a67b5">&#8226;</bullet>&nbsp;&nbsp;'
    '<font name="Helvetica-Bold" color="#1f1e1d">Assistente de Credenciamento</font> '
    '<font color="#777777" size="8.5">jun 2023 - dez 2025</font>',
    style_bullet_desc)
role_desc_best_as = Paragraph(
    "Atuacao em processos de credenciamento de prestadores.",
    style_bullet_desc)

story.append(role_line_best_an)
story.append(role_desc_best_an)
story.append(role_line_best_as)
story.append(role_desc_best_as)

story.append(Paragraph("AUTOGIVA", style_h3))
story.append(Paragraph(
    '<bullet color="#4a67b5">&#8226;</bullet>&nbsp;&nbsp;'
    '<font name="Helvetica-Bold" color="#1f1e1d">Assistente Administrativo</font> '
    '<font color="#777777" size="8.5">nov 2021 - ago 2022</font>',
    style_bullet_desc))
story.append(Paragraph(
    "Atividades administrativas de apoio operacional.",
    style_bullet_desc))

# Competencias (2 colunas)
story.append(Paragraph("Competencias", style_h2))
story.append(HRFlowable(width="100%", thickness=0.4, color=LIGHT, spaceBefore=0, spaceAfter=4))

col_left = [
    [Paragraph("SQL", style_skill_cat), Paragraph("BigQuery, AWS Athena, PostgreSQL, Oracle", style_skill_items)],
    [Paragraph("PYTHON", style_skill_cat), Paragraph("pandas, numpy, matplotlib, seaborn, plotly, Streamlit", style_skill_items)],
    [Paragraph("R", style_skill_cat), Paragraph("ggplot2, dplyr", style_skill_items)],
]
col_right = [
    [Paragraph("BI", style_skill_cat), Paragraph("Power BI, Tableau, Metabase", style_skill_items)],
    [Paragraph("IA / LLM", style_skill_cat), Paragraph("RAG, embeddings, ChromaDB, NVIDIA NIM, OpenAI API", style_skill_items)],
    [Paragraph("ENGENHARIA", style_skill_cat), Paragraph("FastAPI, Docker, OAuth, APIs REST, Git, GitHub Actions, Nginx, selenium, htmx, systemd", style_skill_items)],
]

def stack_rows(rows):
    flow = []
    for cat, items in rows:
        flow.append(cat)
        flow.append(items)
    return flow

left_col = stack_rows(col_left)
right_col = stack_rows(col_right)

skills_table = Table(
    [[left_col, right_col]],
    colWidths=[8.5*cm, 8.5*cm]
)
skills_table.setStyle(TableStyle([
    ("VALIGN", (0,0), (-1,-1), "TOP"),
    ("LEFTPADDING", (0,0), (-1,-1), 0),
    ("RIGHTPADDING", (0,0), (-1,-1), 12),
    ("TOPPADDING", (0,0), (-1,-1), 0),
    ("BOTTOMPADDING", (0,0), (-1,-1), 0),
]))
story.append(skills_table)

# Idiomas
story.append(Paragraph("Idiomas", style_h2))
story.append(HRFlowable(width="100%", thickness=0.4, color=LIGHT, spaceBefore=0, spaceAfter=4))
story.append(Paragraph(
    '<strong><font color="#4a67b5">Portugues:</font></strong> Nativo',
    style_body))
story.append(Paragraph(
    '<strong><font color="#4a67b5">Ingles:</font></strong> '
    'Leitura intermediario . Escrita intermediario . Conversa iniciante . Escuta iniciante',
    style_body))

# Projetos
story.append(Paragraph("Projetos", style_h2))
story.append(HRFlowable(width="100%", thickness=0.4, color=LIGHT, spaceBefore=0, spaceAfter=4))
story.append(Paragraph(
    '<strong><font color="#4a67b5">Soundblend</font></strong> '
    '<font color="#444444"><i>distribui musicas curtidas do Spotify em playlists por genero</i></font>',
    style_body))
story.append(Paragraph(
    '<strong><font color="#4a67b5">Verbo</font></strong> '
    '<font color="#444444"><i>RAG fechado sobre a Biblia Ave Maria, sem inventar com conhecimento geral do LLM</i></font>',
    style_body))

# Footer
story.append(HRFlowable(width="100%", thickness=0.4, color=LIGHT, spaceBefore=18, spaceAfter=4))
story.append(Paragraph(
    "Curriculo gerado em julho de 2026. Versao mais recente em armandonetto.com.",
    style_footer))

doc.build(story)
print(f"PDF gerado: {dst} ({dst.stat().st_size} bytes)")