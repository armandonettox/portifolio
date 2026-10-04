from fastapi.testclient import TestClient

from app import discussions
from app.main import app

client = TestClient(app)


def test_health():
    assert client.get("/api/health").json() == {"status": "ok"}


def test_lista_de_posts_nao_traz_o_corpo(monkeypatch):
    post = {"slug": "1-x", "title": "X", "date": "2026-10-04", "body": "texto"}
    monkeypatch.setattr(discussions, "list_posts", lambda: [post])
    data = client.get("/api/posts").json()
    assert data and "body" not in data[0]


def test_post_inexistente_retorna_404(monkeypatch):
    monkeypatch.setattr(discussions, "list_posts", lambda: [])
    assert client.get("/api/posts/nao-existe").status_code == 404
