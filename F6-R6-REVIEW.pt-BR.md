# Revisão científica e bilíngue F6-R6

## Correções científicas em relação à R4

1. **Escopo do comparador:** `scripts/compare_sbom_runs.py` compara uma projeção de pacotes/relações. Exclui a coleção `files` e metadados do documento, remove `SPDXID` dos pacotes e substitui endpoints de pacotes por chaves nome/versão/PURL.
2. **Colisões de chave:** 27 chaves da projeção colidem, abrangendo 170 ocorrências de pacotes. A projeção estabelece igualdade de sua saída serializada entre execuções, não equivalência semântica SPDX universal.
3. **Evidência do documento completo:** uma comparação recursiva R6 de todos os valores analisados encontrou apenas duas diferenças. A igualdade completa ocorre após normalizar somente `creationInfo.created` e `documentNamespace`.
4. **Linguagem de dependências:** o comparador de inventário usa regex/nomes de arquivos e pares nome/versão normalizados entre ecossistemas. Diferenças vazias são concordância sob essa implementação, não prova de resolução, compilação, distribuição, identidade ou completude.
5. **Contagens CMake:** os valores são contagens lexicais de padrões de chamadas, não alvos configurados nem grafo de build.
6. **Reprodutibilidade:** duas execuções locais sustentam repetibilidade local nas condições registradas. A reprodução externa independente permanece `NOT_VERIFIED`.

## Revisão bilíngue

Os relatórios EN e PT-BR foram revisados contra as mesmas evidências e terminologia. Ambos preservam:

- todos os hashes, contagens, caminhos e identificadores de gates;
- a distinção entre ocorrências e pares normalizados únicos;
- a distinção entre repetibilidade local e reprodução externa;
- os limites do comparador projetivo histórico;
- as distinções declarado/detectado/resolvido/configurado/compilado/vinculado/runtime/distribuído;
- a declaração de independência e ausência de endosso.

O mapeamento terminológico correspondente está no documento inglês. A verificação automática confirma paridade de invariantes, mas não substitui a revisão substantiva aqui registrada.

`SCIENTIFIC_REVIEW_GREEN=PASS`

`BILINGUAL_EQUIVALENCE_GREEN=PASS`

