import os
from pathlib import Path

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

from app import discussions, github

app = FastAPI(title="portfolio-api")


def all_posts() -> list[dict]:
    """Posts vindos das discussoes do GitHub; sem resposta, a API devolve 503."""
    try:
        return discussions.list_posts()
    except (httpx.HTTPError, discussions.DiscussionsUnavailable):
        raise HTTPException(status_code=503, detail="nao foi possivel carregar os posts agora")


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


# Site compilado (React). Em desenvolvimento a pasta nao existe e o Vite serve o frontend.
STATIC_DIR = Path(os.environ.get("STATIC_DIR", Path(__file__).resolve().parent.parent / "static"))


@app.get("/{path:path}", include_in_schema=False)
def site(path: str):
    if not STATIC_DIR.is_dir():
        raise HTTPException(status_code=404, detail="frontend nao encontrado")
    if path.startswith("api/"):
        raise HTTPException(status_code=404, detail="rota da api nao encontrada")

    root = STATIC_DIR.resolve()
    target = (root / path).resolve()
    # so serve arquivo que esteja de fato dentro da pasta do site (evita ../ no endereco)
    if path and target.is_file() and target.is_relative_to(root):
        return FileResponse(target)
    # qualquer outra rota e do React Router: entrega o index.html
    return FileResponse(root / "index.html")
