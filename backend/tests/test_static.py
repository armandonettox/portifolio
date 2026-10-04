from fastapi.testclient import TestClient

from app import main


def site_falso(tmp_path, monkeypatch):
    (tmp_path / "assets").mkdir()
    (tmp_path / "index.html").write_text("<html>home</html>", encoding="utf-8")
    (tmp_path / "assets" / "app.js").write_text("console.log(1)", encoding="utf-8")
    (tmp_path.parent / "segredo.txt").write_text("nao pode sair", encoding="utf-8")
    monkeypatch.setattr(main, "STATIC_DIR", tmp_path)
    return TestClient(main.app)


def test_serve_arquivo_existente(tmp_path, monkeypatch):
    client = site_falso(tmp_path, monkeypatch)
    assert client.get("/assets/app.js").text == "console.log(1)"


def test_rota_do_react_devolve_o_index(tmp_path, monkeypatch):
    client = site_falso(tmp_path, monkeypatch)
    assert "home" in client.get("/blog/algum-post").text
    assert "home" in client.get("/").text


def test_rota_de_api_inexistente_nao_devolve_o_site(tmp_path, monkeypatch):
    client = site_falso(tmp_path, monkeypatch)
    assert client.get("/api/nao-existe").status_code == 404


def test_nao_sai_da_pasta_do_site(tmp_path, monkeypatch):
    client = site_falso(tmp_path, monkeypatch)
    for caminho in ("/../segredo.txt", "/%2e%2e/segredo.txt", "/assets/../../segredo.txt"):
        assert "nao pode sair" not in client.get(caminho).text


def test_sem_pasta_do_site_retorna_404(tmp_path, monkeypatch):
    monkeypatch.setattr(main, "STATIC_DIR", tmp_path / "nao-existe")
    assert TestClient(main.app).get("/").status_code == 404


def test_head_funciona_no_site_e_na_api(tmp_path, monkeypatch):
    client = site_falso(tmp_path, monkeypatch)
    assert client.head("/").status_code == 200
    assert client.head("/blog/algum-post").status_code == 200
    assert client.head("/api/health").status_code == 200


def test_arquivo_inexistente_da_404_e_nao_a_pagina_inicial(tmp_path, monkeypatch):
    client = site_falso(tmp_path, monkeypatch)
    for caminho in ("/robots.txt", "/favicon.ico", "/assets/nada.js"):
        assert client.get(caminho).status_code == 404


def test_robots_existente_e_servido(tmp_path, monkeypatch):
    client = site_falso(tmp_path, monkeypatch)
    (tmp_path / "robots.txt").write_text("User-agent: *", encoding="utf-8")
    assert client.get("/robots.txt").text == "User-agent: *"
