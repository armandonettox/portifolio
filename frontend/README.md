# Frontend do portfólio

Site pessoal de Armando Netto, em React com TypeScript (Vite). Consome a API do `backend/` (FastAPI).

## Páginas

- **Início:** apresentação, foto e links de contato.
- **Projetos:** repositórios públicos do GitHub, com busca e filtros por linguagem, data e ordem.
- **Blog:** posts escritos como discussões no GitHub, com comentários pelo giscus.

## Como rodar

Precisa de Node 22 ou mais novo e do backend rodando na porta 8000.

```
npm install
npm run dev
```

O Vite encaminha as chamadas de `/api` para `http://localhost:8000` (veja `vite.config.ts`).

## Comandos

| Comando | O que faz |
|---------|-----------|
| `npm run dev` | servidor de desenvolvimento |
| `npm run build` | confere os tipos e gera a versão de produção em `dist/` |
| `npm run lint` | roda o oxlint |

## Estrutura

- `src/pages/`: uma pasta de página por rota (Home, Projects, Posts, PostPage).
- `src/components/`: nome animado, logos flutuantes, menu, botão de tema, comentários.
- `src/api.ts`: tipos e chamadas à API.
- `src/index.css`: paleta (tema claro e escuro por `data-theme`) e estilos globais.
