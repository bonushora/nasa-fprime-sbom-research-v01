# NASA F´ SBOM Research v0.1 — F0

Independent, unqualified documentary baseline for the native SBOM generation mechanism in NASA F´ (F Prime).

> **R6 archival note:** this historical narrative is retained from F0. Its linked
> supporting files resolve to the immutable research baseline commit
> `6e00649fc2e2ae65f30086f059160865bdc49442`; they are not duplicated in this
> public candidate because the historical governance snapshot records a local
> workspace path. The complete, byte-preserved R4 input remains outside this
> derived R6 directory.

## Phase outcome

| Gate | Status |
|---|---|
| `F0_DOCUMENTATION_GREEN` | `PASS` |
| `SBOM_GENERATION_GREEN` | `NÃO_EXECUTADO` |
| `SECURITY_QUALIFICATION_GREEN` | `NÃO_EXECUTADO` |

The initial F0 block was strict: on 2026-11-03, remote read access made it possible to observe official files on the moving `devel` branch, but not to resolve and verify the full commit to which it pointed. Local Git access failed because of DNS resolution, and the official API was unavailable through the read channel. Therefore, no upstream baseline had been frozen at that point, and no value was assumed.

### F0-R1 revision — identity recovery

An independent external query provided candidate commit `a4b1b1c043d1f9b51a7faba4a47d5d0f231910c7` and three Git blob OIDs. A local revalidation attempt at `2026-11-03T23:53:10-03:00` again failed because of DNS in the shell; the commit, API, tree, raw content, and immutable pages were also unavailable through the read channel. The identifiers were preserved as externally supplied, locally unverified evidence without changing the `BLOCKED` gate. The previous documentary SHA-256 values were preserved in the BH-SDP snapshot.

### F0-R1B revision — evidence bridge

The local package `.artifacts/f0-r1b-evidence/FPRIME-SBOM-F0-R1B-EVIDENCE-v01/` was inspected without running its verifier or any upstream file. The three transported files passed size, SHA-256, and Git blob OID checks, including an independent calculation using the Git blob formula. This established the internal integrity of the package bytes, but did not establish upstream identity: the package states that it does not contain self-contained tree proof, and it omits `cmake/FPrime.cmake` and `cmake/target/target.cmake`, which were needed to confirm the registration and dispatch points locally. The gate remained `BLOCKED`.

### F0-R1D revision — documentary closure

The physical R1C evidence closed the previous gaps: commit object `a4b1b1c043d1f9b51a7faba4a47d5d0f231910c7`, its root tree `af4e2084aa84d51e82949c42f116d91301f65d81`, five path-to-blob bindings, and their SHA-256 values were revalidated directly from an offline Git pack. Enumeration reproduced exactly nine literal matches in the tracked superproject tree, and the dynamic registration/dispatch chain was confirmed in the Git objects. The search did not traverse the sole gitlink, `googletest`. With F0-01 through F0-08 satisfied, `F0_DOCUMENTATION_GREEN=PASS`; this does not promote SBOM generation, security qualification, or `GLOBAL_GREEN`.

Even before closure, the phase produced a useful and traceable static characterization. The observed code conditionally creates a CMake `ALL` target, invokes Syft on `FPRIME_PROJECT_ROOT`, requests `spdx-json`, excludes nested `.github` paths according to the observed argument, redirects stdout to a file in the build tree, and installs that file under the toolchain directory. This does not demonstrate completeness, release authenticity, or security qualification.

## Artifacts

- [Scope and boundaries](https://github.com/bonushora/nasa-fprime-sbom-research-v01/blob/6e00649fc2e2ae65f30086f059160865bdc49442/docs/F0-scope-and-boundaries.md)
- [Upstream identity](https://github.com/bonushora/nasa-fprime-sbom-research-v01/blob/6e00649fc2e2ae65f30086f059160865bdc49442/docs/F0-upstream-identity.md)
- [Native mechanism](https://github.com/bonushora/nasa-fprime-sbom-research-v01/blob/6e00649fc2e2ae65f30086f059160865bdc49442/docs/F0-native-sbom-mechanism.md)
- [Syft execution risk](https://github.com/bonushora/nasa-fprime-sbom-research-v01/blob/6e00649fc2e2ae65f30086f059160865bdc49442/docs/F0-syft-execution-risk.md)
- [Coverage matrix](https://github.com/bonushora/nasa-fprime-sbom-research-v01/blob/6e00649fc2e2ae65f30086f059160865bdc49442/docs/F0-dependency-coverage-matrix.md)
- [Independent comparison plan](https://github.com/bonushora/nasa-fprime-sbom-research-v01/blob/6e00649fc2e2ae65f30086f059160865bdc49442/docs/F0-independent-comparison-plan.md)
- [Acceptance matrix](https://github.com/bonushora/nasa-fprime-sbom-research-v01/blob/6e00649fc2e2ae65f30086f059160865bdc49442/docs/F0-acceptance-matrix.md)
- [BH-SDP v2.3 snapshot](https://github.com/bonushora/nasa-fprime-sbom-research-v01/blob/6e00649fc2e2ae65f30086f059160865bdc49442/governance/F0-sdp-snapshot.json)

## Evidence conventions

- **Observed fact:** directly supported by read content or a recorded local result.
- **Inference:** a technical consequence of the observed code, explicitly marked as such.
- **Hypothesis:** a proposition to be tested in a future phase.
- **Unknown/limitation:** information not demonstrated in this phase.

No build, upstream script, test, Syft invocation, or installer was executed. No upstream repository or cFS research project was modified.
