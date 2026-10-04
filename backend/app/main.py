from fastapi import FastAPI, HTTPException

from app import content

app = FastAPI(title="portfolio-api")


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/api/posts")
def posts() -> list[dict]:
    # na listagem nao precisa mandar o texto inteiro
    return [{k: v for k, v in p.items() if k != "body"} for p in content.list_posts()]


@app.get("/api/posts/{slug}")
def post(slug: str) -> dict:
    found = content.get_post(slug)
    if found is None:
        raise HTTPException(status_code=404, detail="post nao encontrado")
    return found


@app.get("/api/projects")
def projects() -> list[dict]:
    return content.list_projects()
