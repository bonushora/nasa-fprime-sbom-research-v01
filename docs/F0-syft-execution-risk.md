# F0 — Syft execution risk

## Phase classification

`EXECUTION=NOT_AUTHORIZED_AND_NOT_EXECUTED`

This is an analysis of the effect surface, not a finding of vulnerability.

## Observed tools and effects

| Component | Action | Potential effect |
|---|---|---|
| CMake | resolves `syft` through `PATH` | behavior depends on the host and the binary found |
| Python | executes `redirector.py` | opens/truncates the output JSON |
| `redirector.py` | invokes argv with `subprocess.run` | executes Syft without a shell; propagates the return code; stderr remains external |
| Syft | catalogs `dir:${FPRIME_PROJECT_ROOT}` | recursively reads the project and interprets manifests/artifacts |
| CMake install | installs the component after the target | writes/copies to the configured installation destination |

## Host dependencies and variability

- CMake, Python, and Syft executables, all with versions and hashes unpinned in the observed excerpt.
- `PATH`, CMake variables, permissions, locale, timezone, filesystem, and symbolic links.
- Configuration, environment variables, cache, and local directories that Syft may discover.
- The content and initialization state of submodules under the scanned root.
- The cataloger set and format version associated with the Syft version found.

The current official Syft reference documents settings for update checks, optional remote ecosystem queries, and local caching; the observed F´ command does not pin those controls. See the [Syft Configuration Reference](https://oss.anchore.com/docs/reference/syft/configuration/) and [Supported Sources](https://github.com/anchore/syft/wiki/supported-sources).

## Possible side effects

1. Creation or truncation of the JSON in the build tree, including when Syft fails.
2. Writing the installed copy under the destination configured by F´.
3. Broad reading of all reachable paths under the root, subject to effective exclusions.
4. Reading user configuration and caches; possible cache writes, depending on version/configuration.
5. Network traffic for update checks or remote enrichment when enabled by the version/configuration.
6. CPU, memory, and I/O use proportional to the scanned content.
7. Silent behavior changes when `syft` appears in or disappears from `PATH`, because the target is conditional and participates in `ALL`.

Items 4 and 5 are version/configuration-dependent possibilities, not effects observed during execution in this research.

## Coverage and confidence limits

- The source is a directory tree, not the final installation or an executable image.
- Syft identifies packages through catalogers and recognized evidence; this is not equivalent to enumerating every source file or every CMake target.
- The compiler link graph and the `DEPENDENCIES`/`FULL_DEPENDENCIES` parameters are not provided to the observed Syft command.
- Dependencies absent from the tree, code generated outside it, and host/toolchain components may be omitted.
- `spdx-json` without an explicit version may change schema/defaults between Syft versions. The official documentation confirms that standard formats may omit or transform data available in the native format: [Output Formats](https://oss.anchore.com/docs/guides/sbom/formats/).

## Minimum conditions for future isolated execution

Only after new authorization:

- freeze the upstream commit and verify hashes for all inputs;
- pin the versions and SHA-256 values of the Syft, Python, and CMake binaries used;
- use a read-only source and ephemeral build/install/cache locations in a dedicated directory;
- deny network access through an external mechanism and explicitly disable update/remote-enrichment behavior;
- provide controlled HOME/config/cache locations and a minimal environment without credentials;
- use a closed `PATH` and record argv and versions without executing unreviewed wrappers;
- bound CPU, memory, I/O, time, and disk space;
- record the input tree, submodule state, toolchain, platform, and deployment;
- validate the JSON/schema and publish atomically only after a zero return code;
- compare hashes and results from at least two identical runs before claiming reproducibility.

## Build-generated versus officially published

A build-generated SBOM is a local result of the source tree, tools, and configuration on that host. Any officially published SBOM would need to be associated by its publisher with a release and have verifiable provenance, channel, checksums/signatures, and generation policy. This F0 did not establish that NASA publishes such an artifact and does not treat a local result as official.
