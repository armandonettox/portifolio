import json
import time

import pytest

from app import cache


def novo_estado():
    return {"at": 0.0, "data": None}


def falha():
    raise RuntimeError("api fora do ar")


def test_primeira_busca_boa_e_guardada_em_disco(tmp_path):
    estado = novo_estado()
    assert cache.get(estado, "lista", 60, lambda: [{"a": 1}]) == [{"a": 1}]
    salvo = json.loads((tmp_path / "cache" / "lista.json").read_text(encoding="utf-8"))
    assert salvo["data"] == [{"a": 1}]


def test_apos_reiniciar_usa_a_copia_do_disco_mesmo_com_a_api_fora():
    cache.get(novo_estado(), "lista", 60, lambda: [{"a": 1}])
    # container novo: memoria vazia, API fora do ar
    reiniciado = novo_estado()
    assert cache.get(reiniciado, "lista", 60, falha) == [{"a": 1}]


def test_copia_do_disco_vencida_e_entregue_e_atualizada_depois():
    antigo = novo_estado()
    cache.get(antigo, "lista", 60, lambda: [{"v": "velha"}])
    reiniciado = novo_estado()
    # a copia do disco esta vencida (ttl 0): entrega a velha e busca a nova em seguida
    resposta = cache.get(reiniciado, "lista", 0, lambda: [{"v": "nova"}])
    assert resposta == [{"v": "velha"}]
    assert cache.get(reiniciado, "lista", 60, falha) == [{"v": "nova"}]


def test_erro_da_api_nunca_apaga_a_lista_boa():
    estado = novo_estado()
    cache.get(estado, "lista", 0, lambda: [{"a": 1}])
    for _ in range(3):
        assert cache.get(estado, "lista", 0, falha) == [{"a": 1}]


def test_resposta_vazia_nunca_apaga_a_lista_boa():
    estado = novo_estado()
    cache.get(estado, "lista", 0, lambda: [{"a": 1}])
    assert cache.get(estado, "lista", 0, lambda: []) == [{"a": 1}]
    # e o disco continua com a lista boa
    assert cache.get(novo_estado(), "lista", 60, falha) == [{"a": 1}]


def test_sem_nenhuma_copia_o_erro_sobe_e_o_vazio_nao_e_guardado(tmp_path):
    with pytest.raises(RuntimeError):
        cache.get(novo_estado(), "lista", 60, falha)
    assert cache.get(novo_estado(), "lista", 60, lambda: []) == []
    assert not (tmp_path / "cache" / "lista.json").exists()


def test_arquivo_de_cache_quebrado_e_ignorado(tmp_path):
    pasta = tmp_path / "cache"
    pasta.mkdir()
    (pasta / "lista.json").write_text("{isto nao e json", encoding="utf-8")
    assert cache.get(novo_estado(), "lista", 60, lambda: [{"a": 1}]) == [{"a": 1}]


def test_falha_ao_gravar_em_disco_nao_derruba(monkeypatch, tmp_path):
    # o "diretorio" de cache e um arquivo comum: criar a pasta falha
    arquivo = tmp_path / "nao-e-pasta"
    arquivo.write_text("x", encoding="utf-8")
    monkeypatch.setenv("CACHE_DIR", str(arquivo / "cache"))
    estado = novo_estado()
    assert cache.get(estado, "lista", 60, lambda: [{"a": 1}]) == [{"a": 1}]
    assert cache.get(estado, "lista", 60, falha) == [{"a": 1}]


def test_lista_valida_dentro_do_prazo_nao_busca_de_novo():
    chamadas = []

    def busca():
        chamadas.append(1)
        return [{"a": 1}]

    estado = novo_estado()
    cache.get(estado, "lista", 60, busca)
    cache.get(estado, "lista", 60, busca)
    assert len(chamadas) == 1


def test_atualizacao_em_segundo_plano_nao_bloqueia_a_resposta(monkeypatch):
    monkeypatch.setattr(cache, "SYNC_REFRESH", False)
    estado = novo_estado()
    cache.get(estado, "lista", 0, lambda: [{"v": "velha"}])

    def lenta():
        time.sleep(0.4)
        return [{"v": "nova"}]

    inicio = time.time()
    resposta = cache.get(estado, "lista", 0, lenta)
    assert resposta == [{"v": "velha"}]
    assert time.time() - inicio < 0.2  # respondeu na hora, sem esperar a API lenta
    time.sleep(0.8)
    assert estado["data"] == [{"v": "nova"}]
    assert estado["refreshing"] is False
