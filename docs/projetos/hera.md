---
title: Hera
---

# Hera

Assistente pessoal de finanças e agenda no Telegram, com portal web em `hera.armandonetto.com`.

**Status:** Em producao | [hera.armandonetto.com](https://hera.armandonetto.com) | [GitHub](https://github.com/armandonettox/hera)

## O que faz

O Hera conversa em linguagem natural e atua em duas areas:

**Financas** — registro de gastos livres e fixos, resumo por periodo, projecao de saldo, comparativo mensal, metas de economia, controle de cartao de credito e categorias customizadas. Entende foto de nota fiscal e comprovante, e processa mensagens de audio.

**Agenda** — criacao, listagem e conclusao de lembretes por linguagem natural.

Alem das respostas sob demanda, o Hera envia alertas proativos sem ser acionado: vencimentos do dia, relatorio semanal, fechamento mensal, anomalias de gasto e avisos de limite por categoria.

## Portal web

Disponivel em `hera.armandonetto.com`:

- Landing page com planos
- Cadastro com verificacao de email
- Dashboard financeiro: categorias, transacoes, gastos fixos, metas
- Chat com IA direto pelo navegador
- Exportacao CSV e conexao bancaria via Open Finance

## Stack

- Python + python-telegram-bot
- FastAPI + Jinja2 + HTMX (portal web)
- Supabase (PostgreSQL)
- Hermes Agent (Nous Research) — LLM, memoria persistente, session continuity, visao e audio
- NVIDIA NIM (modelo principal + STT + multimodal)
- Podman + podman-compose (Oracle Cloud Ampere A1 ARM64)
- GitHub Actions + self-hosted runner (deploy automatico)

[Ver no GitHub](https://github.com/armandonettox/hera)
