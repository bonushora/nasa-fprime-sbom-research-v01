# F Prime — Evidência de Diálogo com Mantenedor v0.1

## Fonte primária

- Discussão: https://github.com/nasa/fprime/discussions/6311
- Título: Official SBOM availability and release-level dependency traceability for F´
- Autor da discussão: @bonushora
- Abertura (UTC): 2026-11-03T22:05:15Z
- Resposta do mantenedor: https://github.com/nasa/fprime/discussions/6311#discussioncomment-19386109
- Data da resposta (UTC): 2026-11-04T00:01:54Z
- Resposta do pesquisador: https://github.com/nasa/fprime/discussions/6311#discussioncomment-19388195
- Data da resposta (UTC): 2026-11-04T02:33:58Z

## Declaração original do mantenedor

> The F Prime build system generates an SBOM using syft if it is installed on the build host https://github.com/nasa/fprime/blob/devel/cmake/target/sbom.cmake

## Tradução explicativa

O sistema de build do F Prime gera uma SBOM utilizando Syft
quando essa ferramenta está instalada no computador de build.

A tradução acima é explicativa; o texto original em inglês
permanece preservado como evidência primária.

## Resposta do pesquisador

O pesquisador agradeceu o esclarecimento e declarou a intenção
de analisar a saída SPDX JSON gerada pelo Syft em uma revisão
fixa do F Prime, distinguindo resultados independentes de
artefatos oficiais de releases.

O conteúdo integral e os metadados dos comentários estão no
arquivo `discussion-6311-source.json`.

## Relevância científica

A resposta identificou o mecanismo nativo de geração
de SBOM por CMake/Syft do F Prime, condicionado à
disponibilidade do Syft no ambiente de build.

Essa informação sustenta a escolha metodológica
investigada na pesquisa independente F Prime SBOM v0.2.

## Limites da evidência

- Confirma esclarecimento técnico público de @thomas-bc.
- Não comprova SBOM oficial publicada por release.
- Não comprova revisão dos resultados pelo mantenedor.
- Não comprova reprodução externa nem cobertura completa.
- Não constitui endosso da NASA, JPL, Caltech ou do F Prime.
- Este adendo é posterior à publicação v0.2 e não é
  apresentado como integrante do pacote original congelado.

MAINTAINER_TECHNICAL_CLARIFICATION=VERIFIED
MAINTAINER_REVIEW_OF_RESEARCH=NOT_VERIFIED
INSTITUTIONAL_ENDORSEMENT=NOT_CLAIMED
