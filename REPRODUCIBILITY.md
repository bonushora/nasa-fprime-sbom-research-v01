# Reconstruction and reproducibility boundary

## Status

Two local executions were observed in the original qualified environment. No independent party has reconstructed the experiment in a separate environment.

`EXTERNAL_INDEPENDENT_REPRODUCTION=NOT_VERIFIED`

This status is a limitation, not a failed local run and not a PASS.

## Reconstruction procedure

1. Obtain F Prime from its official repository and resolve commit `a4b1b1c043d1f9b51a7faba4a47d5d0f231910c7`. Verify the Git object/tree evidence and the 3,609-entry SHA-256 source manifest.
2. Leave the recorded `googletest` gitlink unmaterialized if reproducing the observed input. Initializing it changes the source population and is a different experiment.
3. Obtain Syft 1.56.0 from the official Anchore release. Verify `syft_1.56.0_checksums.txt` and the Linux AMD64 archive hash recorded by the package inputs.
4. Reconstruct `.artifacts/v0.2/source` and `.artifacts/v0.2/tools/syft`. Inspect every script before execution.
5. Recreate effective isolation: source read-only; separate ephemeral home, cache, build, and install paths; denied external network; no host home, credentials, or `/etc`; closed `PATH`; UTC/C locale; and the documented resource/time limits.
6. Run `scripts/run-native-sbom.sh` only in a newly authorized executable phase. Candidate F6-R6 itself did not rerun Syft or CMake.
7. Preserve each raw SPDX before analysis. Validate against the included SPDX 2.3 schema and check relationship references.
8. Compare the complete parsed documents recursively. Report all paths that differ. Separately run the historical projection comparator only as a secondary, explicitly limited analysis.
9. Compare declarations and detected packages with ecosystem-qualified identifiers where available. Do not interpret name/version agreement as resolution, compilation, linkage, or distribution.
10. Verify the new package manifest and record the environment, operator, commands, timestamps, exit codes, and deviations.

## What was locally observed

The two provided SPDX files differ at exactly two paths: `creationInfo.created` and `documentNamespace`. Normalizing only those two values makes the complete parsed documents equal. This is evidence for repeatability in the recorded local conditions, not a general claim across hosts, tool versions, source states, or time.

## What remains unverified

- external reconstruction by an independent operator;
- full F Prime deployment build and test reproduction;
- initialized-submodule behavior;
- binary, linkage, runtime, target-filesystem, and distribution coverage;
- vulnerability status and dependency completeness.

The SPDX originals are immutable evidence and must not be edited to remove paths, timestamps, UUIDs, or metadata.

