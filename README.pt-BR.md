# NASA F Prime — pesquisa experimental de SBOM SPDX v0.2 (F6-R6)

Pacote de pesquisa independente preparado para decisão humana de publicação. Não é publicação, certificação nem endosso da NASA, Caltech ou JPL.

[English](README.md)

## Resultado observado

Duas execuções locais do mecanismo nativo CMake/Syft de SBOM de fontes do F Prime, invocado por um harness mínimo, produziram documentos SPDX 2.3 JSON com 266 ocorrências de pacotes, 46 entradas de arquivos e 581 relações em cada execução. Ambos passaram nas verificações registradas do schema JSON SPDX 2.3 e das referências de relações.

Os originais não são idênticos em bytes. Uma comparação recursiva completa encontrou exatamente dois valores diferentes: `creationInfo.created` e `documentNamespace`. Após substituir somente esses dois valores, os documentos analisados completos são iguais.

O campo `semantic_identical` do comparador anterior tem sentido mais restrito: igualdade da projeção de pacotes e relações definida pelo estudo. Ele omite metadados do documento e a coleção `files`, e sua chave de pacote não é exclusiva nestes dados (27 chaves com colisão abrangendo 170 das 266 ocorrências de pacotes). Seu hash não é um resumo semântico SPDX universal.

## Limites

O experimento não comprova completude de dependências, correspondência com distinção de ecossistema, cobertura de compilação/vinculação/runtime/distribuição, ausência de vulnerabilidades, prontidão para voo nem reprodutibilidade externa. O harness não compilou um deployment completo do F Prime, e o conteúdo do submódulo `googletest` não inicializado estava ausente.

`EXTERNAL_INDEPENDENT_REPRODUCTION=NOT_VERIFIED`

## Mapa do pacote

- [Relatório em inglês](docs/v0.2/RESEARCH-REPORT.md)
- [Relatório em português](docs/v0.2/RESEARCH-REPORT.pt-BR.md)
- [Procedimento de reconstrução](REPRODUCIBILITY.pt-BR.md)
- [Revisão científica e linguística](F6-R6-REVIEW.pt-BR.md)
- [Revisão de direitos](RIGHTS-REVIEW.pt-BR.md)
- [Inventário de redistribuição](REDISTRIBUTION.md)
- Evidências SPDX originais: `evidence/v0.2/runs/`
- Qualificação R6: `validation/f6-r6/`
- Snapshot BH-SDP: `governance/F6-R6-sdp-snapshot.json`
- Manifesto físico: `SHA256SUMS-PUBLIC`

## Identidades fixadas

- Baseline F0 da pesquisa: `6e00649fc2e2ae65f30086f059160865bdc49442`
- Upstream F Prime: `a4b1b1c043d1f9b51a7faba4a47d5d0f231910c7`
- Manifesto R4 preservado: `5f3a398f5a776b17720d979781b232c95e118cfa876258dd0d2904bc877b7d88`

O pacote é local e não publicado. Não houve push, release, criação de DOI, depósito Zenodo, alteração de ORCID nem contato institucional.

