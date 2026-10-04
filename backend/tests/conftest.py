import pytest

from app import cache


@pytest.fixture(autouse=True)
def cache_isolado(tmp_path, monkeypatch):
    """Cada teste usa uma pasta de cache propria e atualiza na hora, sem thread."""
    monkeypatch.setenv("CACHE_DIR", str(tmp_path / "cache"))
    monkeypatch.setattr(cache, "SYNC_REFRESH", True)
