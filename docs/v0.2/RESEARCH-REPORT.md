# Experimental source-level SPDX SBOM generation in NASA F Prime: local repeatability and coverage boundaries

**Status:** Local manuscript candidate F6-R6; unpublished.

**Type:** Independent experimental software supply-chain study.

**Upstream:** `a4b1b1c043d1f9b51a7faba4a47d5d0f231910c7`

## Abstract

This study examined the native F Prime CMake/Syft source-SBOM mechanism at a fixed upstream commit. A minimal harness invoked the unmodified native target in an isolated local environment; it did not compile a complete F Prime deployment. Two runs produced SPDX 2.3 JSON documents with 266 package occurrences, 46 file entries, and 581 relationships each. The originals have different SHA-256 values. A complete recursive comparison found exactly two differing values—creation time and document namespace—and equality after normalizing only those values. This is local repeatability evidence, not external reproducibility or dependency completeness.

## Method

The source export contained 3,609 regular files and omitted the contents of the uninitialized `googletest` gitlink. Source was mounted read-only; writable output was separate; external networking and host credential surfaces were denied. Syft 1.56.0 generated each raw SPDX, which was preserved before analysis. The documents were checked against the included SPDX 2.3 JSON schema and for internal relationship references.

Independent scripts performed three limited analyses:

1. filename-based source/declaration enumeration;
2. name/version set comparison for pinned Python requirements, GitHub Action `uses` values, Cargo lock entries, and Syft packages;
3. a package/relationship projection comparison between runs.

These scripts are auditable research code, not authoritative ecosystem resolvers or a complete SPDX semantic model.

## Results

| Measurement | Run 1 | Run 2 |
|---|---:|---:|
| SHA-256 | `0ad4ec43…fc8b` | `6837b5a0…5c38` |
| Package occurrences | 266 | 266 |
| File entries | 46 | 46 |
| Relationships | 581 | 581 |
| SPDX 2.3 schema check | PASS | PASS |
| Relationship-reference check | PASS | PASS |

The full parsed documents differ only at `creationInfo.created` and `documentNamespace`; they are equal after replacing only those two values. This stronger R6 observation was obtained by a direct recursive comparison of every parsed value.

The historical comparator reported projection digest `1661858c7d6fb692b9408caaaf913d9a26c4f6ad947b90a01708f623dfb4bd8b` for both runs. That digest covers its package/relationship projection, not the entire SPDX document. The projection excludes document metadata and `files`. Its name/version/PURL package key has 27 collisions covering 170 of 266 package occurrences, so relationship endpoints can collapse onto the same key.

The independent state matrix reported 80 unique pinned Python name/version pairs, 35 unique non-local GitHub Action name/version pairs, four unique Cargo lock name/version pairs, and 123 unique normalized Syft name/version pairs. These are sets produced by the implemented parsers. Matching is not ecosystem-qualified and therefore does not prove that a declaration and detection refer to the same component. Two GitHub Action commit references were unmatched while tag-like forms for the same action names appeared in the native set.

The 184 module, 46 library, and four deployment values are lexical counts of `register_fprime_*` call patterns in `CMakeLists.txt` files. They are not configured targets, a build graph, or compiled outputs.

## Interpretation

The evidence supports repeatability of the complete parsed source-level SPDX content across the two local runs after normalizing the two observed volatile document fields. It does not support a universal semantic-equivalence claim, cross-environment reproducibility, or completeness.

Detected, declared, resolved, configured, compiled, linked, deployed, and distributed are distinct states. This experiment directly observed declarations and Syft detections, parsed selected lock entries, and invoked the native SBOM target. It did not measure a full configured deployment graph, compilation, linkage, runtime, or distribution.

## Limitations

- only two local runs in one qualified environment;
- no external independent reconstruction;
- minimal harness, not a complete F Prime deployment build;
- absent `googletest` submodule contents;
- filename/regex parsers and cross-ecosystem name normalization;
- no binary, target-filesystem, runtime, vulnerability, or flight qualification;
- schema validity does not establish completeness or correctness of package conclusions;
- no NASA, Caltech, or JPL review or endorsement.

`EXTERNAL_INDEPENDENT_REPRODUCTION=NOT_VERIFIED`

## Provenance

Raw SPDX files, historical comparator outputs, schema validations, the R6 full-document audit, privacy review, rights review, and package manifest are included. Publication remains a human decision; no release, DOI, or deposit has been created.

