from pathlib import Path

import frontmatter

CONTENT_DIR = Path(__file__).resolve().parent.parent / "content"


def _load(folder: str) -> list[dict]:
    items = []
    for path in sorted((CONTENT_DIR / folder).glob("*.md")):
        post = frontmatter.load(path)
        items.append({"slug": path.stem, **post.metadata, "body": post.content})
    return items


def list_posts() -> list[dict]:
    posts = _load("posts")
    # posts mais recentes primeiro
    return sorted(posts, key=lambda p: str(p.get("date", "")), reverse=True)


def get_post(slug: str) -> dict | None:
    return next((p for p in list_posts() if p["slug"] == slug), None)
