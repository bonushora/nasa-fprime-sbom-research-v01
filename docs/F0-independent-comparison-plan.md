# F0 — Independent comparison plan

## Status

`PLAN_ONLY — NOT_AUTHORIZED_FOR_EXECUTION`

The future objective is to compare the native mechanism with an independent enumeration without treating agreement as automatic proof of completeness.

## Mandatory preconditions

1. Explicit authorization for a new executable phase.
2. Full F´ commit frozen and files obtained through immutable URLs.
3. Verified hashes for source, submodules, tools, and configurations.
4. Pinned Syft, Python, and CMake; network-disabled environment; disposable workspace.
5. Deployment, platform/toolchain, and build configuration defined before collection.
6. Acceptance criteria approved without modifying upstream.

## Sets to compare

| Set | Future production | Purpose |
|---|---|---|
| NATIVE-SOURCE | native F´ target in the isolated environment | observe the mechanism's effective result |
| DIRECT-SOURCE | same Syft version and equivalent argv, controlled invocation | separate wrapper/CMake effects |
| MANIFEST-LEDGER | read-only parsing of manifests/locks at the commit | independent inventory of declarations |
| BUILD-GRAPH | CMake File API/metadata generated in an authorized build | build targets and dependencies |
| ARTIFACT-SCAN | Syft against install tree/final artifact, if approved | measure source-versus-product difference |
| LINKAGE | link maps and dynamic dependencies of the artifact, if applicable | libraries actually linked |
| OFFICIAL | any authenticated artifact published by NASA | compare only if its existence/provenance is verified |

## Normalization

- Preserve originals and work on normalized copies.
- Record schema/version; do not silently convert between formats.
- Normalize identifiers by PURL/CPE/ecosystem, name, version, and origin while preserving collisions.
- Separate timestamp/random-ID differences from semantic differences.
- Do not equate declared, resolved, built, linked, and distributed dependencies.
- Classify each difference as a confirmed explanation, hypothesis, or unknown.

## Comparisons and metrics

1. Byte-for-byte and semantic reproducibility across two identical runs.
2. Components found only in each set and intersections by class.
3. Missing versions, hashes, licenses, supplier, PURL/CPE, and relationships.
4. Coverage by deployment, platform, build configuration, and artifact.
5. Presence of commit/release identity and cryptographic evidence of the association.
6. Effect of the `.github` exclusion and initialized/uninitialized submodules.
7. Difference between a detected package and a merely present file.

## Stop criteria

Stop and record `BLOCKED` if identity, hashes, network isolation, tool pinning, or result provenance cannot be demonstrated. Failure or divergence does not authorize ad hoc source changes or tool installation outside the approved procedure.

## Expected future outputs

Input manifest, sanitized environment log, commands, hashes of original results, normalization report, classified diff, and separate decisions for generation and qualification. This plan does not establish that any of those outputs exists today.
