from fastapi.testclient import TestClient

from app import main, seo

INDEX = (
    '<html><head><title>Armando Netto</title>\n'
    '    <meta name="seo-head" content="">\n'
    "</head><body></body></html>"
)

POST = {
    "slug": "1-por-que-criei-meu-proprio-site",
    "title": "Por que criei meu próprio site",
    "date": "2026-07-20",
    "edited": "2026-10-04",
    "summary": "Meu conhecimento sempre esteve espalhado.",
}


def test_home_recebe_titulo_descricao_og_e_dados_da_pessoa():
    out = seo.render_index(INDEX, "", [])
    assert "<title>Armando Netto</title>" in out
    assert 'property="og:image" content="https://armandonetto.com/og-image.png"' in out
    assert 'name="twitter:card" content="summary_large_image"' in out
    assert '"@type": "Person"' in out
    assert "seo-head" not in out
    # o empregador nao entra nos dados publicos
    assert "worksFor" not in out and "Best" not in out


def test_post_usa_titulo_resumo_url_e_tipo_artigo():
    out = seo.render_index(INDEX, f"blog/{POST['slug']}", [POST])
    assert f"<title>{POST['title']} | Armando Netto</title>" in out
    assert 'property="og:type" content="article"' in out
    assert f'content="https://armandonetto.com/blog/{POST["slug"]}"' in out
    assert "Meu conhecimento sempre esteve espalhado." in out
    assert '"@type": "BlogPosting"' in out and '"datePublished": "2026-07-20"' in out


def test_texto_do_post_nao_quebra_o_html():
    ruim = dict(POST, title='Aspas " e <script>alert(1)</script>', summary='Fim </script><b>x</b> "a"')
    out = seo.render_index(INDEX, f"blog/{ruim['slug']}", [ruim])
    assert "<script>alert(1)</script>" not in out
    assert '</script><b>' not in out.split('type="application/ld+json"')[0]
    assert "&lt;script&gt;" in out and "&quot;" in out


def test_pagina_desconhecida_e_post_inexistente_caem_no_padrao():
    assert "<title>Armando Netto</title>" in seo.render_index(INDEX, "blog/nao-existe", [POST])
    assert "<title>Blog | Armando Netto</title>" in seo.render_index(INDEX, "blog", [])
    assert "<title>Projetos | Armando Netto</title>" in seo.render_index(INDEX, "projetos", [])


def test_index_sem_placeholder_sai_igual():
    assert seo.render_index("<html></html>", "", []) == "<html></html>"


def test_sitemap_lista_paginas_e_posts():
    xml = seo.sitemap([POST])
    assert xml.startswith('<?xml version="1.0" encoding="UTF-8"?>')
    for loc in ("/</loc>", "/projetos</loc>", "/blog</loc>", f"/blog/{POST['slug']}</loc>"):
        assert loc in xml
    assert "<lastmod>2026-10-04</lastmod>" in xml


def test_rota_do_site_entrega_o_index_com_meta_tags(tmp_path, monkeypatch):
    (tmp_path / "index.html").write_text(INDEX, encoding="utf-8")
    monkeypatch.setattr(main, "STATIC_DIR", tmp_path)
    monkeypatch.setattr(main, "posts_or_empty", lambda: [POST])
    client = TestClient(main.app)
    page = client.get(f"/blog/{POST['slug']}")
    assert page.status_code == 200 and POST["title"] in page.text
    assert "og:title" in client.get("/projetos").text
    assert client.head("/projetos").status_code == 200


def test_sitemap_xml_e_servido_como_xml(monkeypatch):
    monkeypatch.setattr(main, "posts_or_empty", lambda: [POST])
    res = TestClient(main.app).get("/sitemap.xml")
    assert res.status_code == 200 and "xml" in res.headers["content-type"]
    assert POST["slug"] in res.text
