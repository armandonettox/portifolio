import httpx
import pytest

from app import github


def repo(name, pushed, fork=False, stars=0):
    return {
        "name": name,
        "html_url": f"https://github.com/u/{name}",
        "description": f"desc {name}",
        "language": "Python",
        "stargazers_count": stars,
        "pushed_at": pushed,
        "topics": [],
        "fork": fork,
    }


@pytest.fixture(autouse=True)
def limpa_cache():
    github._cache["at"] = 0.0
    github._cache["data"] = None


def fora_do_ar(user):
    raise httpx.ConnectError("sem rede")


def test_filtra_forks_e_escondidos_e_ordena_por_push():
    repos = [
        repo("antigo", "2026-01-01T00:00:00Z"),
        repo("portifolio", "2026-10-01T00:00:00Z"),
        repo("copia", "2026-09-01T00:00:00Z", fork=True),
        repo("recente", "2026-08-01T00:00:00Z", stars=3),
    ]
    out = github.build_projects(repos, {"hidden": ["Portifolio"], "pinned": []})
    assert [p["name"] for p in out] == ["recente", "antigo"]
    assert out[0]["stars"] == 3
    assert out[0]["pushed_at"] == "2026-08-01T00:00:00Z"


def test_fixados_vem_primeiro_na_ordem_da_lista():
    repos = [
        repo("a", "2026-03-01T00:00:00Z"),
        repo("b", "2026-02-01T00:00:00Z"),
        repo("c", "2026-01-01T00:00:00Z"),
    ]
    out = github.build_projects(repos, {"hidden": [], "pinned": ["c", "b"]})
    assert [p["name"] for p in out] == ["c", "b", "a"]


def test_usa_cache_na_segunda_chamada(monkeypatch):
    chamadas = []

    def fake_fetch(user):
        chamadas.append(user)
        return [repo("x", "2026-01-01T00:00:00Z")]

    monkeypatch.setattr(github, "_fetch_repos", fake_fetch)
    github.list_projects()
    github.list_projects()
    assert len(chamadas) == 1


def test_sem_cache_e_com_github_fora_levanta_erro(monkeypatch):
    monkeypatch.setattr(github, "_fetch_repos", fora_do_ar)
    with pytest.raises(httpx.HTTPError):
        github.list_projects()


def test_com_github_fora_devolve_a_ultima_resposta(monkeypatch):
    github._cache["data"] = [{"name": "guardado"}]
    monkeypatch.setattr(github, "_fetch_repos", fora_do_ar)
    assert github.list_projects() == [{"name": "guardado"}]
