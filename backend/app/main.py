import os
import threading
from contextlib import asynccontextmanager
from pathlib import Path

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse, Response

from app import discussions, github, seo

def warm_cache() -> None:
    """Ao iniciar: carrega a ultima lista boa do disco e tenta atualizar, sem travar a subida."""
    for load in (github.list_projects, discussions.list_posts):
        try:
            load()
        except Exception:  # GitHub fora do ar na subida: o site sobe igual, com o que houver em disco
            pass


@asynccontextmanager
async def lifespan(_app: FastAPI):
    threading.Thread(target=warm_cache, daemon=True).start()
    yield


app = FastAPI(title="portfolio-api", lifespan=lifespan)


def all_posts() -> list[dict]:
    """Posts vindos das discussoes do GitHub; sem resposta, a API devolve 503."""
    try:
        return discussions.list_posts()
    except (httpx.HTTPError, discussions.DiscussionsUnavailable):
        raise HTTPException(status_code=503, detail="nao foi possivel carregar os posts agora")


@app.api_route("/api/health", methods=["GET", "HEAD"])
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


def posts_or_empty() -> list[dict]:
    """Para meta tags e sitemap: se o GitHub falhar, a pagina sai sem os dados dos posts."""
    try:
        return discussions.list_posts()
    except (httpx.HTTPError, discussions.DiscussionsUnavailable):
        return []


@app.api_route("/sitemap.xml", methods=["GET", "HEAD"], include_in_schema=False)
def sitemap() -> Response:
    return Response(seo.sitemap(posts_or_empty()), media_type="application/xml")


# Site compilado (React). Em desenvolvimento a pasta nao existe e o Vite serve o frontend.
STATIC_DIR = Path(os.environ.get("STATIC_DIR", Path(__file__).resolve().parent.parent / "static"))


@app.api_route("/{path:path}", methods=["GET", "HEAD"], include_in_schema=False)
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
    # pedido de arquivo que nao existe (robots.txt, sitemap.xml, imagem...) deve dar 404 de verdade,
    # e nao a pagina inicial com status 200, que confunde buscadores e navegadores
    if "." in path.rsplit("/", 1)[-1]:
        raise HTTPException(status_code=404, detail="arquivo nao encontrado")
    # qualquer outra rota e do React Router: entrega o index.html com as meta tags da pagina,
    # porque o LinkedIn e os buscadores montam a previa sem executar JavaScript
    index = (root / "index.html").read_text(encoding="utf-8")
    posts = posts_or_empty() if path.strip("/").startswith("blog/") else []
    return HTMLResponse(seo.render_index(index, path, posts))
