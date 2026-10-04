#!/usr/bin/env bash
# Atualiza SO o container do portfolio quando sai imagem nova no GHCR.
# Nao toca em nenhum outro container ou servico.
set -u
IMG=ghcr.io/armandonettox/portfolio:latest
SVC=portfolio.service
HEALTH=http://127.0.0.1:8006/api/health

old_id=$(podman image inspect --format "{{.Id}}" "$IMG" 2>/dev/null || true)

if ! podman pull -q "$IMG" >/dev/null 2>&1; then
  echo "nao consegui baixar a imagem agora, mantendo a versao atual"
  exit 0
fi

new_id=$(podman image inspect --format "{{.Id}}" "$IMG")
# sem imagem nova: nao faz nada e nao reinicia
[ "$old_id" = "$new_id" ] && exit 0

echo "imagem nova: ${new_id:0:12} (anterior: ${old_id:0:12})"
systemctl --user restart "$SVC"

for _ in $(seq 1 15); do
  sleep 2
  if curl -fsS -m 3 "$HEALTH" >/dev/null 2>&1; then
    echo "portfolio atualizado e saudavel"
    exit 0
  fi
done

# a versao nova nao ficou saudavel: volta para a anterior
echo "versao nova nao respondeu, voltando para ${old_id:0:12}"
if [ -n "$old_id" ]; then
  podman tag "$old_id" "$IMG"
  systemctl --user restart "$SVC"
fi
exit 1
