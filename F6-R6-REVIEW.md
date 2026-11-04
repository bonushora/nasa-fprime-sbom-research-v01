# F6-R6 scientific and bilingual review

## Scientific corrections from R4

1. **Comparator scope:** `scripts/compare_sbom_runs.py` compares a package/relationship projection. It excludes the `files` collection and document metadata, removes package `SPDXID`, and substitutes relationship package endpoints with name/version/PURL keys.
2. **Key collisions:** 27 projection keys collide, covering 170 package occurrences. The projection can establish equality of its serialized output across runs, but not universal SPDX semantic equivalence.
3. **Full-document evidence:** an R6 recursive comparison of every parsed value found only two differences. Complete equality follows after normalizing just `creationInfo.created` and `documentNamespace`.
4. **Dependency language:** the inventory comparator uses regex/filename parsing and cross-ecosystem normalized name/version pairs. Empty differences are agreement under that implementation, not proof of resolution, compilation, distribution, identity, or completeness.
5. **CMake counts:** the reported values are lexical call-pattern counts, not configured targets or a build graph.
6. **Reproducibility:** two local runs support local repeatability under recorded conditions. External independent reproduction remains `NOT_VERIFIED`.

## Bilingual review

The English and PT-BR reports were reviewed against the same evidence and terminology. Both preserve:

- all fixed hashes, counts, paths, and gate identifiers;
- the distinction between occurrences and unique normalized pairs;
- the distinction between local repeatability and external reproducibility;
- the limits of the historical projection comparator;
- declared/detected/resolved/configured/compiled/linked/runtime/distributed distinctions;
- the independence and non-endorsement statement.

Terminology mapping:

| English | PT-BR |
|---|---|
| local repeatability | repetibilidade local |
| external independent reproduction | reprodução externa independente |
| source-level SBOM | SBOM em nível de fontes |
| package occurrence | ocorrência de pacote |
| relationship | relação |
| build graph | grafo de build |
| coverage boundary | limite de cobertura |

The machine check confirms invariant parity; it does not substitute for the substantive review recorded here.

`SCIENTIFIC_REVIEW_GREEN=PASS`

`BILINGUAL_EQUIVALENCE_GREEN=PASS`

