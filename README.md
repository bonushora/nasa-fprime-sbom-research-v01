# NASA F Prime — experimental SPDX SBOM research v0.2 (F6-R6)

Independent research package prepared for a human publication decision. It is not a NASA, Caltech, or JPL publication, certification, or endorsement.

[Português brasileiro](README.pt-BR.md)

## Observed result

Two local runs of the unmodified F Prime CMake/Syft source-SBOM mechanism, invoked through a minimal harness, produced SPDX 2.3 JSON documents with 266 package occurrences, 46 file entries, and 581 relationships each. Both passed the recorded SPDX 2.3 JSON-schema and relationship-reference checks.

The originals are not byte-identical. A full recursive comparison found exactly two differing values: `creationInfo.created` and `documentNamespace`. After replacing only those two values, the complete parsed documents compare equal.

The older comparator's `semantic_identical` field has a narrower meaning: equality of its study-defined package/relationship projection. It omits document metadata and the `files` collection, and its package key is non-unique for this data (27 colliding keys covering 170 of 266 package occurrences). Its hash is not a universal SPDX semantic digest.

## Boundaries

This experiment does not establish dependency completeness, ecosystem-disambiguated matching, build/link/runtime/distribution coverage, vulnerability absence, flight readiness, or external reproducibility. The harness did not compile a full F Prime deployment, and the uninitialized `googletest` submodule contents were absent.

`EXTERNAL_INDEPENDENT_REPRODUCTION=NOT_VERIFIED`

## Package map

- [English report](docs/v0.2/RESEARCH-REPORT.md)
- [Relatório em português](docs/v0.2/RESEARCH-REPORT.pt-BR.md)
- [Reconstruction procedure](REPRODUCIBILITY.md)
- [Scientific and linguistic review](F6-R6-REVIEW.md)
- [Rights review](RIGHTS-REVIEW.md)
- [Redistribution inventory](REDISTRIBUTION.md)
- Original SPDX evidence: `evidence/v0.2/runs/`
- R6 qualification: `validation/f6-r6/`
- BH-SDP snapshot: `governance/F6-R6-sdp-snapshot.json`
- Physical manifest: `SHA256SUMS-PUBLIC`

## Fixed identities

- F0 research baseline: `6e00649fc2e2ae65f30086f059160865bdc49442`
- F Prime upstream: `a4b1b1c043d1f9b51a7faba4a47d5d0f231910c7`
- Preserved R4 manifest: `5f3a398f5a776b17720d979781b232c95e118cfa876258dd0d2904bc877b7d88`

The package is local and unpublished. No push, release, DOI, Zenodo deposit, ORCID mutation, or institutional contact was performed.


## Post-publication provenance addendum

The following supplementary evidence was added after the frozen v0.2 publication:

- [F Prime Discussion #6311 — bilingual provenance](docs/provenance/fprime-maintainer-dialogue-v01/README.md)

This records a maintainer's technical clarification, not a review or endorsement of the research.
