# Arquivos do servidor

Copia dos arquivos que rodam na VM, para ela poder ser recriada. O deploy so reage a `backend/`,
`frontend/` e `Dockerfile`; mexer nesta pasta nao gera imagem nova.

| Arquivo | Onde fica na VM |
|---------|-----------------|
| `portfolio.container` | `~/.config/containers/systemd/` (quadlet do container) |
| `portfolio-refresh.sh` | `~/.local/bin/` (modo 700) |
| `portfolio-refresh.service` e `.timer` | `~/.config/systemd/user/` |

O timer roda a cada 5 minutos e o script baixa `ghcr.io/armandonettox/portfolio:latest`. Se a imagem
for diferente da atual, reinicia so o `portfolio.service`, espera `/api/health` responder e, se a
versao nova nao ficar saudavel, volta para a anterior. Ele nao toca em nenhum outro container.

Instalar: copiar os arquivos, criar `~/portfolio.env` (modo 600, com `GITHUB_TOKEN`), depois
`systemctl --user daemon-reload` e `systemctl --user enable --now portfolio-refresh.timer`.
O usuario precisa de linger ligado (`loginctl enable-linger`).

O nginx do servidor (`novo`/dominio principal) e o certificado do Cloudflare ficam fora desta pasta
porque o mesmo nginx serve outros projetos.
