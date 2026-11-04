# Geração experimental de SBOM SPDX em nível de fontes no NASA F Prime: repetibilidade local e limites de cobertura

**Estado:** Candidato local a manuscrito F6-R6; não publicado.

**Tipo:** Pesquisa experimental independente sobre cadeia de suprimentos de software.

**Upstream:** `a4b1b1c043d1f9b51a7faba4a47d5d0f231910c7`

## Resumo

Este estudo examinou o mecanismo nativo CMake/Syft de SBOM de fontes do F Prime em commit upstream fixo. Um harness mínimo invocou o alvo nativo sem modificações em ambiente local isolado; ele não compilou um deployment completo do F Prime. Duas execuções produziram documentos SPDX 2.3 JSON com 266 ocorrências de pacotes, 46 entradas de arquivos e 581 relações em cada uma. Os originais têm SHA-256 diferentes. Uma comparação recursiva completa encontrou exatamente dois valores diferentes — horário de criação e namespace do documento — e igualdade após normalizar somente esses valores. Isso evidencia repetibilidade local, não reprodutibilidade externa nem completude de dependências.

## Método

A exportação das fontes continha 3.609 arquivos regulares e omitia o conteúdo do gitlink `googletest` não inicializado. As fontes foram montadas somente para leitura; a saída gravável era separada; rede externa e superfícies de credenciais do host foram negadas. O Syft 1.56.0 gerou cada SPDX original, preservado antes da análise. Os documentos foram verificados com o schema JSON SPDX 2.3 incluído e quanto às referências internas das relações.

Scripts independentes realizaram três análises limitadas:

1. enumeração de fontes e declarações por nomes de arquivos;
2. comparação de conjuntos nome/versão para requisitos Python fixados, valores `uses` de GitHub Actions, entradas Cargo lock e pacotes Syft;
3. comparação de uma projeção de pacotes e relações entre execuções.

Esses scripts são código de pesquisa auditável, não resolvedores autoritativos de ecossistemas nem modelo semântico SPDX completo.

## Resultados

| Medição | Execução 1 | Execução 2 |
|---|---:|---:|
| SHA-256 | `0ad4ec43…fc8b` | `6837b5a0…5c38` |
| Ocorrências de pacotes | 266 | 266 |
| Entradas de arquivos | 46 | 46 |
| Relações | 581 | 581 |
| Verificação do schema SPDX 2.3 | PASS | PASS |
| Verificação de referências | PASS | PASS |

Os documentos analisados completos diferem somente em `creationInfo.created` e `documentNamespace`; eles são iguais após substituir apenas esses dois valores. Essa observação R6 mais forte veio da comparação recursiva direta de todos os valores analisados.

O comparador histórico registrou o digest da projeção `1661858c7d6fb692b9408caaaf913d9a26c4f6ad947b90a01708f623dfb4bd8b` nas duas execuções. Esse digest cobre sua projeção de pacotes/relações, não o documento SPDX inteiro. A projeção exclui metadados do documento e `files`. Sua chave nome/versão/PURL apresenta 27 colisões abrangendo 170 das 266 ocorrências de pacotes; assim, endpoints de relações podem ser colapsados na mesma chave.

A matriz de estados independente registrou 80 pares nome/versão Python fixados, 35 pares de GitHub Actions não locais, quatro pares Cargo lock e 123 pares Syft normalizados. Esses conjuntos resultam dos parsers implementados. A correspondência não distingue ecossistemas e, portanto, não prova que declaração e detecção sejam o mesmo componente. Duas referências de GitHub Actions por commit não corresponderam, enquanto formas semelhantes a tags dos mesmos nomes apareceram no conjunto nativo.

Os valores 184 módulos, 46 bibliotecas e quatro deployments são contagens lexicais de padrões de chamadas `register_fprime_*` em `CMakeLists.txt`. Não são alvos configurados, grafo de build nem resultados compilados.

## Interpretação

As evidências sustentam repetibilidade do conteúdo SPDX completo analisado entre as duas execuções locais após normalização dos dois campos voláteis observados. Não sustentam equivalência semântica universal, reprodução entre ambientes ou completude.

Detectado, declarado, resolvido, configurado, compilado, vinculado, implantado e distribuído são estados distintos. O experimento observou diretamente declarações e detecções do Syft, analisou entradas selecionadas de locks e invocou o alvo nativo de SBOM. Não mediu um grafo completo de deployment configurado, compilação, vinculação, runtime ou distribuição.

## Limitações

- somente duas execuções locais em um ambiente qualificado;
- nenhuma reconstrução externa independente;
- harness mínimo, não build de deployment completo;
- conteúdo ausente do submódulo `googletest`;
- parsers por nomes/regex e normalização entre ecossistemas;
- nenhuma qualificação binária, de sistema-alvo, runtime, vulnerabilidades ou voo;
- validade de schema não comprova completude nem correção das conclusões de pacotes;
- nenhuma revisão ou aprovação da NASA, Caltech ou JPL.

`EXTERNAL_INDEPENDENT_REPRODUCTION=NOT_VERIFIED`

## Proveniência

O pacote inclui SPDXs originais, saídas do comparador histórico, validações de schema, auditoria R6 do documento completo, revisão de privacidade, revisão de direitos e manifesto. Publicar continua sendo decisão humana; nenhum release, DOI ou depósito foi criado.

