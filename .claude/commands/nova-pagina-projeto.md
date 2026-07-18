# /nova-pagina-projeto

Cria a documentacao de um projeto dentro do portfolio (`docs/projetos/<slug>/`). O portfolio e a unica fonte de documentacao dos projetos — o README de cada projeto deve so descrever objetivamente o que ele faz e linkar pra ca.

## Comportamento

1. Se o nome do projeto for informado (ex: `/nova-pagina-projeto hera`), localizar o repositorio em `~/armandonettox/projects/<nome>`. Caso contrario, perguntar qual projeto.
2. Ler o `README.md` e o `CLAUDE.md` do projeto (se existirem) para entender objetivo, stack e funcionamento.
3. Verificar se o projeto ja tem uma pasta `docs/` com MkDocs proprio:
   - Se tiver: essa e a fonte principal a portar (copiar conteudo, adaptando so o que for preciso).
   - Se nao tiver: escrever a documentacao do zero com base no README/CLAUDE.md e no codigo-fonte (ler os modulos principais antes de descrever "como funciona" — nao inventar detalhes de arquitetura).
4. Perguntar (uma pergunta, com sugestao) se a documentacao deve ser **pagina unica** (projetos pequenos) ou **multi-pagina** no estilo `Visao geral / Primeiros passos / Referencia` (projetos maiores, como soundblend).
5. Escrever os arquivos em `docs/projetos/<slug>/` (ou `docs/projetos/<slug>.md` se for pagina unica).
6. Atualizar o `nav:` do `mkdocs.yml`, aninhando as paginas novas dentro de `Projetos`. Dar um label explicito tipo "Visao geral" pra pagina de indice de cada projeto (nunca deixar o label repetir o nome da secao — ja aconteceu duplicacao por causa disso).
7. Adicionar uma entrada na lista de `docs/projetos/index.md` linkando pro novo projeto.
8. Rodar `mkdocs build --strict` pra confirmar que nao ha link quebrado ou aviso.
9. Perguntar se deve simplificar o README do projeto original (objetivo + stack + link `https://armandonetto.com/projetos/<slug>/`), seguindo o que ja foi feito em soundblend e verbo. So editar apos confirmacao — e outro repositorio.

## O que evitar

- Nao inventar link de repositorio GitHub sem confirmar que o remote existe (`git remote -v` no projeto).
- Nao remover `requirements.txt` ou qualquer arquivo do projeto original sem checar antes se ele serve so pro MkDocs local ou se e usado pelo app em producao (ja aconteceu de um `requirements.txt` ser as dependencias reais do app, nao so da doc).
- Nao commitar nada nos repositorios (portfolio ou do projeto) sem pedido explicito.
