import html
import json
import os
import re

SITE_URL = os.environ.get("SITE_URL", "https://armandonetto.com").rstrip("/")
SITE_NAME = "Armando Netto"
IMAGE_URL = f"{SITE_URL}/og-image.png"

HOME_DESCRIPTION = (
    "Programador que mistura técnica, criatividade e análise de dados "
    "para resolver problemas reais."
)

PAGES = {
    "": (SITE_NAME, HOME_DESCRIPTION),
    "projetos": (
        f"Projetos | {SITE_NAME}",
        "Projetos públicos de Armando Netto no GitHub, com busca por linguagem, data e estrelas.",
    ),
    "blog": (
        f"Blog | {SITE_NAME}",
        "Posts sobre as decisões técnicas por trás do que eu construo, e não só o resultado.",
    ),
}

# tag deixada no index.html; o backend a troca pelas meta tags da pagina pedida
PLACEHOLDER = re.compile(r'<meta name="seo-head"[^>]*>')
TITLE = re.compile(r"<title>.*?</title>", re.S)

PERSON = {
    "@context": "https://schema.org",
    "@type": "Person",
    "name": SITE_NAME,
    "url": SITE_URL,
    "jobTitle": "Profissional de Dados",
    "sameAs": [
        "https://www.linkedin.com/in/armandonettox/",
        "https://github.com/armandonettox",
    ],
    "knowsAbout": [
        "Python", "SQL", "R", "Power BI", "AWS Athena", "PostgreSQL",
        "RAG", "LLM", "ChromaDB", "Streamlit", "Docker", "FastAPI",
    ],
}


def esc(text: str) -> str:
    return html.escape(text, quote=True)


def page_info(path: str, posts: list[dict]) -> dict:
    """Titulo, descricao, tipo e dados estruturados da pagina pedida."""
    clean = path.strip("/")

    if clean.startswith("blog/"):
        slug = clean[len("blog/") :]
        post = next((p for p in posts if p["slug"] == slug), None)
        if post:
            url = f"{SITE_URL}/blog/{slug}"
            return {
                "title": f"{post['title']} | {SITE_NAME}",
                "description": post["summary"] or HOME_DESCRIPTION,
                "type": "article",
                "url": url,
                "jsonld": {
                    "@context": "https://schema.org",
                    "@type": "BlogPosting",
                    "headline": post["title"],
                    "datePublished": post["date"],
                    "dateModified": post.get("edited") or post["date"],
                    "author": {"@type": "Person", "name": SITE_NAME, "url": SITE_URL},
                    "mainEntityOfPage": url,
                    "image": IMAGE_URL,
                },
            }

    title, description = PAGES.get(clean, PAGES[""])
    return {
        "title": title,
        "description": description,
        "type": "website",
        "url": f"{SITE_URL}/{clean}" if clean else SITE_URL + "/",
        "jsonld": PERSON if not clean else None,
    }


def head_tags(info: dict) -> str:
    title, desc, url = esc(info["title"]), esc(info["description"]), esc(info["url"])
    tags = [
        f'<meta name="description" content="{desc}">',
        f'<meta name="author" content="{SITE_NAME}">',
        '<meta name="robots" content="index, follow">',
        f'<link rel="canonical" href="{url}">',
        f'<meta property="og:type" content="{info["type"]}">',
        '<meta property="og:locale" content="pt_BR">',
        f'<meta property="og:site_name" content="{SITE_NAME}">',
        f'<meta property="og:title" content="{title}">',
        f'<meta property="og:description" content="{desc}">',
        f'<meta property="og:url" content="{url}">',
        f'<meta property="og:image" content="{esc(IMAGE_URL)}">',
        '<meta name="twitter:card" content="summary_large_image">',
        f'<meta name="twitter:title" content="{title}">',
        f'<meta name="twitter:description" content="{desc}">',
        f'<meta name="twitter:image" content="{esc(IMAGE_URL)}">',
    ]
    if info.get("jsonld"):
        # "</" dentro do JSON poderia fechar a tag script antes da hora
        data = json.dumps(info["jsonld"], ensure_ascii=False).replace("</", "<\\/")
        tags.append(f'<script type="application/ld+json">{data}</script>')
    return "\n    ".join(tags)


def render_index(index_html: str, path: str, posts: list[dict]) -> str:
    """Devolve o index.html com titulo e meta tags da pagina pedida."""
    if not PLACEHOLDER.search(index_html):
        return index_html
    info = page_info(path, posts)
    # a funcao evita que \1 ou \g no texto do post sejam lidos como grupo da regex
    out = TITLE.sub(lambda _: f"<title>{esc(info['title'])}</title>", index_html, count=1)
    return PLACEHOLDER.sub(lambda _: head_tags(info), out, count=1)


def sitemap(posts: list[dict]) -> str:
    urls = [(f"{SITE_URL}/", None), (f"{SITE_URL}/projetos", None), (f"{SITE_URL}/blog", None)]
    urls += [(f"{SITE_URL}/blog/{p['slug']}", p.get("edited") or p["date"]) for p in posts]
    items = []
    for loc, last in urls:
        lastmod = f"<lastmod>{esc(last)}</lastmod>" if last else ""
        items.append(f"  <url><loc>{esc(loc)}</loc>{lastmod}</url>")
    body = "\n".join(items)
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{body}\n</urlset>\n"
    )
