# Portfólio, Armando Netto

Código do site [armandonetto.com](https://armandonetto.com). Backend em Python (FastAPI) e frontend em React com TypeScript.

## O que o site mostra

- **Início:** apresentação, foto e links de contato.
- **Projetos:** repositórios públicos do GitHub, buscados automaticamente (estrelas, linguagem e data do último push), com busca e filtros.
- **Blog:** posts escritos como discussões no GitHub, com comentários pelo [giscus](https://giscus.app). Quem comenta no site aparece no GitHub e o contrário também.

A documentação técnica de cada projeto fica no repositório do próprio projeto. O site só apresenta.

## Como funciona

```
backend/    FastAPI: API, leitura do GitHub, meta tags por página e sitemap
frontend/   React + TypeScript (Vite)
Dockerfile  compila o frontend e o backend serve tudo em um container só
```

- **Projetos:** `backend/app/github.py` consulta a API pública do GitHub e guarda a resposta por 1 hora. Os repositórios escondidos ficam em `backend/content/github.json`.
- **Posts:** `backend/app/discussions.py` lê as discussões da categoria **Posts** do repositório `armandonettox/blog`. Só discussões escritas pelo dono viram post. A configuração está em `backend/content/blog.json`.
- **Prévia de links e buscadores:** `backend/app/seo.py` escreve título, descrição e meta tags de cada página direto no HTML, porque o LinkedIn e o Google não executam JavaScript.

## Publicar um post

Abra uma discussão na categoria **Posts** de `armandonettox/blog`. O primeiro parágrafo vira o resumo, e os labels viram tags.

Para um texto escrito antes de ser publicado, a primeira linha pode trazer a data original (o GitHub não mostra comentários HTML, então só o site a usa):

```
<!-- data: 2026-07-20 -->
```

O site demora até 10 minutos para mostrar um post novo, por causa do cache.

## Rodando localmente

Precisa de Python 3.13 ou mais novo e Node 22 ou mais novo.

```bash
# backend (porta 8000)
cd backend
python -m venv .venv
.venv/Scripts/pip install -r requirements-dev.txt
.venv/Scripts/python -m uvicorn app.main:app --port 8000

# frontend (porta 5173), em outro terminal
cd frontend
npm install
npm run dev
```

Os posts precisam de um token do GitHub de leitura pública na variável `GITHUB_TOKEN`. Sem ele, os projetos funcionam e o blog responde 503.

Testes do backend: `cd backend && .venv/Scripts/python -m pytest`. Frontend: `npm run build` e `npm run lint`.

## Publicação

A cada push em `main` que mexe em `backend/`, `frontend/` ou no `Dockerfile`, o GitHub Actions compila a imagem para ARM64 e a publica em `ghcr.io/armandonettox/portfolio`. O servidor percebe a imagem nova sozinho: um timer roda a cada 5 minutos, baixa a imagem e, se ela mudou, reinicia só o container do portfólio. Se a versão nova não ficar saudável, ele volta para a anterior. Ou seja, depois de um push o site atualiza em até uns 7 minutos, sem ninguém fazer nada.

Os arquivos que rodam no servidor (quadlet, script e timer) estão em `deploy/`.

O container roda atrás do nginx e do Cloudflare. O `GITHUB_TOKEN` fica em um arquivo de variáveis no servidor, fora da imagem e do git.

## Histórico

A primeira versão do site era feita em MkDocs (Material). Ela continua no histórico do git, no commit `00ae06a` e nos anteriores.
