# Portfolio — Armando Netto

Publicado em [armandonetto.com](https://armandonetto.com).

## Automacoes

O site e estatico (HTML/CSS/JS puro), mas os dados sao dinamicos via API do GitHub:

| Automacao | Descricao |
|-----------|-----------|
| **Projetos** | Lista repos do GitHub automaticamente com nome, descricao, estrelas, linguagens e ultima atualizacao |
| **Bio** | Puxa do README do perfil do GitHub |
| **README dos projetos** | Ao clicar em um projeto, carrega o README direto do repo |
| **Cache local** | Dados da API ficam em localStorage por 2 horas |
| **Proxy** | Cloudflare Worker como intermediario para nao expor token |
| **Dark mode** | Toggle com persistencia em localStorage |
| **Saudacao** | Dinamica baseada no horario de Brasilia |
| **Deploy** | Push em `main` faz deploy automatico no GitHub Pages via GitHub Actions |
