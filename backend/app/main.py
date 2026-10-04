import httpx
from fastapi import FastAPI, HTTPException

from app import content, discussions, github

app = FastAPI(title="portfolio-api")


def all_posts() -> list[dict]:
    """Posts das discussoes do GitHub; se nao houver, usa os arquivos markdown do repositorio."""
    try:
        posts = discussions.list_posts()
    except (httpx.HTTPError, discussions.DiscussionsUnavailable):
        posts = []
    return posts or content.list_posts()


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/api/posts")
def posts() -> list[dict]:
    # na listagem nao precisa mandar o texto inteiro
    return [{k: v for k, v in p.items() if k != "body"} for p in all_posts()]


@app.get("/api/posts/{slug}")
def post(slug: str) -> dict:
    found = next((p for p in all_posts() if p["slug"] == slug), None)
    if found is None:
        raise HTTPException(status_code=404, detail="post nao encontrado")
    return found


@app.get("/api/blog-config")
def blog_config() -> dict:
    # identificadores publicos que o widget de comentarios (giscus) precisa
    cfg = discussions.load_config()
    return {
        "repo": f"{cfg['owner']}/{cfg['repo']}",
        "repo_id": cfg["repo_id"],
        "category": cfg["category"],
        "category_id": cfg["category_id"],
    }


@app.get("/api/projects")
def projects() -> list[dict]:
    try:
        return github.list_projects()
    except httpx.HTTPError:
        raise HTTPException(status_code=503, detail="nao foi possivel consultar o github agora")
