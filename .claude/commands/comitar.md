# /comitar

Cria um commit com todas as alteracoes pendentes.

## Comportamento

1. Rodar `git status`
2. Rodar `git diff` para entender mudancas
3. Sugerir mensagem no formato `tipo(escopo): descricao`
4. Aguardar confirmacao
5. Executar commit

## Regras

- Commits em portugues
- Nunca fazer push automatico
- Verificar arquivos sensiveis (.env, .secrets/) antes de commitar
