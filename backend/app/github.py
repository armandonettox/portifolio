import json
import os
from pathlib import Path

import httpx

from app import cache

CONFIG_PATH = Path(__file__).resolve().parent.parent / "content" / "github.json"
API_URL = "https://api.github.com/users/{user}/repos"
CACHE_SECONDS = 3600

# guarda a ultima resposta para nao estourar o limite de consultas do GitHub
_cache: dict = {"at": 0.0, "data": None}


def load_config() -> dict:
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def _fetch_repos(user: str) -> list[dict]:
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "portfolio-api"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    repos: list[dict] = []
    page = 1
    while True:
        res = httpx.get(
            API_URL.format(user=user),
            params={"type": "owner", "sort": "pushed", "per_page": 100, "page": page},
            headers=headers,
            timeout=10,
        )
        res.raise_for_status()
        batch = res.json()
        repos.extend(batch)
        if len(batch) < 100:
            return repos
        page += 1


def _shape(repo: dict) -> dict:
    return {
        "name": repo["name"],
        "description": repo.get("description"),
        "url": repo["html_url"],
        "homepage": repo.get("homepage") or None,
        "language": repo.get("language"),
        "stars": repo.get("stargazers_count", 0),
        "pushed_at": repo.get("pushed_at") or repo.get("updated_at"),
        "topics": repo.get("topics", []),
    }


def build_projects(repos: list[dict], config: dict) -> list[dict]:
    hidden = {name.lower() for name in config.get("hidden", [])}
    pinned = [name.lower() for name in config.get("pinned", [])]

    # forks e repositorios escondidos pela configuracao nao entram
    shown = [r for r in repos if not r.get("fork") and r["name"].lower() not in hidden]
    shown.sort(key=lambda r: r.get("pushed_at") or "", reverse=True)

    def pin_rank(repo: dict) -> int:
        name = repo["name"].lower()
        return pinned.index(name) if name in pinned else len(pinned)

    # sort estavel: fixados primeiro, na ordem da lista, e o resto por data
    shown.sort(key=pin_rank)
    return [_shape(r) for r in shown]


def list_projects() -> list[dict]:
    config = load_config()
    # a ultima lista boa fica em memoria e em disco; se o GitHub falhar, ela continua valendo
    return cache.get(
        _cache,
        "projects",
        CACHE_SECONDS,
        lambda: build_projects(_fetch_repos(config["user"]), config),
    )
