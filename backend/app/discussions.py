import json
import os
import re
import unicodedata
from datetime import date
from pathlib import Path

import httpx

from app import cache

CONFIG_PATH = Path(__file__).resolve().parent.parent / "content" / "blog.json"
GRAPHQL_URL = "https://api.github.com/graphql"
CACHE_SECONDS = 600

QUERY = """
query($owner: String!, $name: String!, $category: ID!, $after: String) {
  repository(owner: $owner, name: $name) {
    discussions(first: 50, categoryId: $category, after: $after,
                orderBy: {field: CREATED_AT, direction: DESC}) {
      nodes {
        number
        title
        body
        url
        createdAt
        updatedAt
        author { login }
        labels(first: 10) { nodes { name } }
        comments { totalCount }
      }
      pageInfo { hasNextPage endCursor }
    }
  }
}
"""

# guarda a ultima resposta para nao consultar o GitHub a cada visita
_cache: dict = {"at": 0.0, "data": None}


class DiscussionsUnavailable(Exception):
    """Sem token ou sem resposta do GitHub: quem chama decide o que mostrar no lugar."""


def load_config() -> dict:
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def slugify(text: str) -> str:
    plain = unicodedata.normalize("NFD", text).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", plain.lower()).strip("-")


def make_summary(body: str, limit: int = 220) -> str:
    # primeiro paragrafo de texto, sem titulos, imagens ou blocos de codigo
    for block in re.split(r"\n\s*\n", body.strip()):
        block = block.strip()
        if not block or block.startswith(("#", "```", "![", ">", "<", "---")):
            continue
        # aviso em italico no comeco do post (ex: "texto da primeira versao") nao serve de resumo
        if re.fullmatch(r"\*[^*\n]+\*|_[^_\n]+_", block):
            continue
        text = re.sub(r"[*_`]|\[([^\]]*)\]\([^)]*\)", r"\1", block).replace("\n", " ")
        return text if len(text) <= limit else text[: limit - 1].rstrip() + "…"
    return ""


# o GitHub nao deixa mudar a data de criacao de uma discussao. Para um texto escrito antes de
# ser publicado, a primeira linha do post pode trazer a data original: <!-- data: 2026-07-20 -->
# O GitHub nao mostra comentarios HTML, entao so o site usa essa data.
DATE_MARK = re.compile(r"^\s*<!--\s*data:\s*(\d{4}-\d{2}-\d{2})\s*-->\s*")


def split_date_mark(body: str, created_at: str) -> tuple[str, str]:
    """Devolve (data a mostrar, texto sem a marca). Data invalida na marca e ignorada."""
    found = DATE_MARK.match(body)
    if not found:
        return created_at[:10], body
    try:
        date.fromisoformat(found.group(1))
    except ValueError:
        return created_at[:10], body[found.end() :]
    return found.group(1), body[found.end() :]


def shape(node: dict) -> dict:
    shown_date, body = split_date_mark(node["body"], node["createdAt"])
    return {
        "slug": f"{node['number']}-{slugify(node['title'])}",
        "number": node["number"],
        "title": node["title"],
        "date": shown_date,
        "edited": node["updatedAt"][:10],
        "summary": make_summary(body),
        "tags": [label["name"] for label in node["labels"]["nodes"]],
        "body": body,
        "url": node["url"],
        "comments": node["comments"]["totalCount"],
    }


def build_posts(nodes: list[dict], owner: str) -> list[dict]:
    # a categoria pode aceitar discussoes de outras pessoas; so as suas viram post
    mine = [n for n in nodes if (n.get("author") or {}).get("login", "").lower() == owner.lower()]
    posts = [shape(n) for n in mine]
    # mais recente primeiro, pela data mostrada (que pode ser a original, nao a da publicacao)
    return sorted(posts, key=lambda p: (p["date"], p["number"]), reverse=True)


def _fetch_nodes(config: dict) -> list[dict]:
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        raise DiscussionsUnavailable("GITHUB_TOKEN nao configurado")

    headers = {"Authorization": f"Bearer {token}", "User-Agent": "portfolio-api"}
    nodes: list[dict] = []
    after = None
    while True:
        res = httpx.post(
            GRAPHQL_URL,
            json={
                "query": QUERY,
                "variables": {
                    "owner": config["owner"],
                    "name": config["repo"],
                    "category": config["category_id"],
                    "after": after,
                },
            },
            headers=headers,
            timeout=10,
        )
        res.raise_for_status()
        payload = res.json()
        if payload.get("errors"):
            raise DiscussionsUnavailable(payload["errors"][0].get("message", "erro do GitHub"))
        page = payload["data"]["repository"]["discussions"]
        nodes.extend(page["nodes"])
        if not page["pageInfo"]["hasNextPage"]:
            return nodes
        after = page["pageInfo"]["endCursor"]


def list_posts() -> list[dict]:
    config = load_config()
    # a ultima lista boa fica em memoria e em disco; se o GitHub falhar, ela continua valendo
    return cache.get(
        _cache,
        "posts",
        CACHE_SECONDS,
        lambda: build_posts(_fetch_nodes(config), config["owner"]),
    )
