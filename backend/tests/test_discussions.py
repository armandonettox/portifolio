import httpx
import pytest
from fastapi.testclient import TestClient

from app import discussions
from app.main import app


def node(number, title, body, author="armandonettox", labels=(), comments=0):
    return {
        "number": number,
        "title": title,
        "body": body,
        "url": f"https://github.com/armandonettox/blog/discussions/{number}",
        "createdAt": "2026-10-04T10:00:00Z",
        "updatedAt": "2026-10-05T10:00:00Z",
        "author": {"login": author},
        "labels": {"nodes": [{"name": name} for name in labels]},
        "comments": {"totalCount": comments},
    }


@pytest.fixture(autouse=True)
def limpa_cache():
    discussions._cache["at"] = 0.0
    discussions._cache["data"] = None


def test_slug_sem_acento_e_com_numero():
    assert discussions.slugify("Obsidian como segundo cérebro!") == "obsidian-como-segundo-cerebro"
    post = discussions.shape(node(7, "Meu primeiro post", "Texto."))
    assert post["slug"] == "7-meu-primeiro-post"
    assert post["date"] == "2026-10-04"
    assert post["edited"] == "2026-10-05"


def test_so_discussoes_do_dono_viram_post():
    nodes = [node(1, "Meu", "a"), node(2, "De outra pessoa", "b", author="alguem")]
    out = discussions.build_posts(nodes, "ArmandoNettox")
    assert [p["number"] for p in out] == [1]


def test_marca_de_data_vira_a_data_mostrada_e_sai_do_texto():
    body = "<!-- data: 2026-07-20 -->\n*Aviso em italico.*\n\nPrimeiro paragrafo do post."
    post = discussions.shape(node(4, "Antigo", body))
    assert post["date"] == "2026-07-20"
    assert "data:" not in post["body"]
    assert post["body"].startswith("*Aviso")
    # o aviso em italico nao vira resumo
    assert post["summary"] == "Primeiro paragrafo do post."


def test_marca_com_data_invalida_e_ignorada():
    post = discussions.shape(node(5, "Erro", "<!-- data: 2026-13-45 -->\nTexto."))
    assert post["date"] == "2026-10-04"
    assert post["body"] == "Texto."


def test_sem_marca_usa_a_data_de_criacao():
    assert discussions.shape(node(6, "Normal", "Texto."))["date"] == "2026-10-04"


def test_lista_ordenada_pela_data_mostrada():
    antigo = node(1, "Publicado agora, escrito antes", "<!-- data: 2026-07-20 -->\nTexto antigo.")
    novo = node(2, "Escrito e publicado agora", "Texto novo.")
    out = discussions.build_posts([antigo, novo], "armandonettox")
    assert [p["number"] for p in out] == [2, 1]


def test_resumo_pula_titulo_e_corta_texto_longo():
    body = "# Titulo\n\n![img](x.png)\n\n" + "palavra " * 80
    resumo = discussions.make_summary(body)
    assert resumo.startswith("palavra") and resumo.endswith("…") and len(resumo) <= 220


def test_resumo_tira_marcacao_de_links_e_negrito():
    assert discussions.make_summary("Veja o **site** e o [repo](http://x).") == "Veja o site e o repo."


def test_sem_token_levanta_indisponivel(monkeypatch):
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)
    with pytest.raises(discussions.DiscussionsUnavailable):
        discussions.list_posts()


def test_api_responde_503_quando_discussoes_indisponiveis(monkeypatch):
    def fora():
        raise discussions.DiscussionsUnavailable("sem token")

    monkeypatch.setattr(discussions, "list_posts", fora)
    client = TestClient(app)
    assert client.get("/api/posts").status_code == 503
    assert client.get("/api/posts/qualquer").status_code == 503


def test_api_usa_discussoes_quando_disponiveis(monkeypatch):
    post = discussions.shape(node(3, "Do GitHub", "Texto do post.", labels=("workflow",), comments=2))
    monkeypatch.setattr(discussions, "list_posts", lambda: [post])
    client = TestClient(app)
    lista = client.get("/api/posts").json()
    assert [p["slug"] for p in lista] == ["3-do-github"]
    assert lista[0]["comments"] == 2
    assert client.get("/api/posts/3-do-github").json()["body"] == "Texto do post."
    assert client.get("/api/posts/nao-existe").status_code == 404


def test_config_do_blog_traz_so_ids_publicos():
    cfg = TestClient(app).get("/api/blog-config").json()
    assert set(cfg) == {"repo", "repo_id", "category", "category_id"}
    assert cfg["repo"] == "armandonettox/blog"


def test_resultado_vazio_nao_fica_em_cache(monkeypatch):
    respostas = [[], [node(1, "Primeiro post", "Texto.")]]
    monkeypatch.setattr(discussions, "_fetch_nodes", lambda config: respostas.pop(0))
    assert discussions.list_posts() == []
    # o post publicado logo depois aparece na proxima consulta, sem esperar o cache vencer
    assert [p["number"] for p in discussions.list_posts()] == [1]


def test_erro_de_rede_sem_cache_levanta(monkeypatch):
    def rede(config):
        raise httpx.ConnectError("sem rede")

    monkeypatch.setattr(discussions, "_fetch_nodes", rede)
    with pytest.raises(httpx.HTTPError):
        discussions.list_posts()


def test_resposta_vazia_nao_apaga_os_posts_ja_conhecidos(monkeypatch):
    discussions._cache["at"] = 0.0
    discussions._cache["data"] = [{"number": 1, "slug": "1-x"}]
    monkeypatch.setattr(discussions, "_fetch_nodes", lambda config: [])
    assert discussions.list_posts() == [{"number": 1, "slug": "1-x"}]
