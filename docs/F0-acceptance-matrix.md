# F0 — Acceptance matrix

## Decision

`F0_DOCUMENTATION_GREEN=PASS`

The workspace, upstream identity, CMake chain, risk boundaries, coverage matrix, independent plan, and snapshot were verified. The promotion is exclusively documentary and does not change the generation or qualification gates.

| ID | Criterion | Evidence | Result |
|---|---|---|---|
| F0-01 | documentary workspace exists | nine required artifacts in the authorized workspace | `PASS` |
| F0-02 | upstream identity verified and recorded | commit, tree, five paths/blobs, sizes, and SHA-256 values confirmed in the Git pack | `PASS` |
| F0-03 | CMake/Syft integration characterized | registration, dynamic dispatch, three definitions, and nine matches classified at the same commit | `PASS` |
| F0-04 | execution risk bounded | inputs, tools, effects, host, network/cache, and isolation documented | `PASS` |
| F0-05 | matrix identifies knowns/unknowns | class-based matrix with gaps and conditions | `PASS` |
| F0-06 | independent comparison plan | sets, preconditions, metrics, and stop rules | `PASS` |
| F0-07 | documents inspected and validated | local checks of files, JSON, links/fields, and documentary hashes | `PASS` |
| F0-08 | BH-SDP v2.3 snapshot consistent | valid `governance/F0-sdp-snapshot.json` aligned with the gates | `PASS` |

## Operational gates

| Gate | Result | Rationale |
|---|---|---|
| upstream fixed commit | `PASS` | commit object and root tree verified offline |
| evidence package integrity | `PASS` | sizes, SHA-256 values, and Git blob OIDs match |
| immutable source bytes | `PASS` | five blobs and transported copies are identical |
| upstream tree binding | `PASS` | five paths resolved by the commit tree |
| call-site inventory | `PASS` | nine matches reproduced in the tracked superproject tree |
| mechanism characterization | `PASS` | registration chain and dynamic dispatch confirmed |
| risk boundary | `PASS` | no execution required to establish the boundary |
| local artifact set | `PASS` | required set present |
| JSON syntax | `PASS` | local validation planned/executed before delivery |
| forbidden execution | `PASS` | build/Syft/tests/scripts/installation not executed |

## Independent states

- `F0_DOCUMENTATION_GREEN=PASS`
- `SBOM_GENERATION_GREEN=NÃO_EXECUTADO`
- `SECURITY_QUALIFICATION_GREEN=NÃO_EXECUTADO`
- `GLOBAL_GREEN=NOT_DECLARED`

## Limits preserved after PASS

1. Enumeration covers the tracked superproject tree and does not traverse the `googletest` submodule.
2. No SBOM was generated or compared through execution.
3. No official release/signature was qualified by this phase.
4. Coverage fields marked `UNKNOWN` remain unknown until an authorized executable phase.

These limits do not block F0 documentary closure, but prevent any promotion of the generation, security, or global-green gates.
