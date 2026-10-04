"""Cache da ultima lista boa: nunca devolve vazio por causa de uma falha da API de fora.

- Se ja existe uma lista boa (na memoria ou salva em disco), ela e entregue na hora, mesmo vencida;
  a atualizacao acontece em segundo plano.
- Uma resposta vazia ou com erro nunca substitui uma lista boa.
- A lista boa e salva em disco, para sobreviver ao reinicio do container.
"""

import json
import logging
import os
import threading
import time
from pathlib import Path
from typing import Callable

log = logging.getLogger("portfolio.cache")

# os testes ligam isto para a atualizacao rodar na hora, sem thread
SYNC_REFRESH = False

_lock = threading.Lock()


def cache_dir() -> Path:
    return Path(os.environ.get("CACHE_DIR", Path(__file__).resolve().parent.parent / "cache"))


def _file(name: str) -> Path:
    return cache_dir() / f"{name}.json"


def _load_disk(state: dict, name: str) -> None:
    try:
        saved = json.loads(_file(name).read_text(encoding="utf-8"))
        if saved.get("data"):
            state["data"] = saved["data"]
            state["at"] = float(saved.get("at", 0.0))
    except (OSError, ValueError):
        # sem arquivo ou arquivo quebrado: segue sem a copia em disco
        pass


def _store(state: dict, name: str, data: list) -> None:
    state["at"] = time.time()
    state["data"] = data
    try:
        path = _file(name)
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(".tmp")
        tmp.write_text(json.dumps({"at": state["at"], "data": data}, ensure_ascii=False), encoding="utf-8")
        os.replace(tmp, path)
    except OSError as err:
        # falhar ao gravar em disco nao pode derrubar o site
        log.warning("nao consegui salvar o cache %s em disco: %s", name, err)


def _refresh(state: dict, name: str, fetch: Callable[[], list]) -> None:
    try:
        data = fetch()
        if data:
            _store(state, name, data)
        else:
            log.warning("%s: resposta vazia ignorada, mantendo a ultima lista boa", name)
    except Exception as err:  # qualquer falha da API de fora: mantem o que ja temos
        log.warning("%s: nao consegui atualizar (%s), mantendo a ultima lista boa", name, err)
    finally:
        state["refreshing"] = False


def _refresh_async(state: dict, name: str, fetch: Callable[[], list]) -> None:
    with _lock:
        if state.get("refreshing"):
            return
        state["refreshing"] = True
    if SYNC_REFRESH:
        _refresh(state, name, fetch)
    else:
        threading.Thread(target=_refresh, args=(state, name, fetch), daemon=True).start()


def get(state: dict, name: str, ttl: int, fetch: Callable[[], list]) -> list:
    """Devolve a lista de `name`. `state` guarda {"at", "data"}; `fetch` busca na API de fora."""
    if state.get("data") is None:
        _load_disk(state, name)

    current = state.get("data")
    if current is not None:
        # entrega o que ja temos agora; se venceu, a atualizacao vale para a proxima chamada
        if time.time() - state["at"] >= ttl:
            _refresh_async(state, name, fetch)
        return current

    # nunca houve lista boa (nem em memoria nem em disco): precisa buscar agora, e o erro sobe
    data = fetch()
    if data:
        _store(state, name, data)
    return data
