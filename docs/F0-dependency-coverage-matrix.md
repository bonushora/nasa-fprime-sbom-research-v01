# F0 — Dependency coverage matrix

Legend: `IN-SCOPE` describes files potentially reachable by the directory source; `OUT-OF-SCOPE` describes items outside the root; `CONDITIONAL` depends on tree/cataloger state; `UNKNOWN` lacks evidence. Reachability does not imply correct detection as a package.

| Class | Reach of observed source | Coverage as a dependency | Evidence/limit |
|---|---|---|---|
| manifests within `FPRIME_PROJECT_ROOT` | `IN-SCOPE` | `CONDITIONAL` | Syft receives the root; cataloger and version are not pinned |
| C/C++ sources and headers | `IN-SCOPE` | `UNKNOWN` | being readable does not imply an SPDX package or relationship |
| CMake modules/targets | `IN-SCOPE` as files | `UNKNOWN` | the CMake graph is not passed to Syft |
| dependencies declared in `DEPENDENCIES`/`FULL_DEPENDENCIES` | n/a | `NOT_DIRECTLY_CONVEYED` | observed hooks ignore these parameters |
| built modules/deployments | `CONDITIONAL` | `UNKNOWN` | registered as ordering dependencies, not as packages |
| initialized Git submodules under the root | `IN-SCOPE` | `CONDITIONAL` | only materialized content can be read |
| uninitialized submodules | `OUT-OF-SCOPE` material | `NOT_COVERED` | a Git pointer does not materialize the content |
| vendored dependencies under the root | `IN-SCOPE` | `CONDITIONAL` | depends on evidence recognized by the catalogers |
| Python virtual environment outside the root | `OUT-OF-SCOPE` | `NOT_COVERED` | the source is the project directory |
| Python packages declared in files under the root | `IN-SCOPE` | `CONDITIONAL` | unpinned constraints and transitive resolution may limit accuracy |
| build products outside the root | `OUT-OF-SCOPE` | `NOT_COVERED` | the source is not `CMAKE_BINARY_DIR` |
| code generated in the build tree | `OUT-OF-SCOPE` | `NOT_COVERED` | unless the build tree is exceptionally placed inside the root |
| installation artifacts | `OUT-OF-SCOPE` | `NOT_COVERED` | installation occurs after the observed generation step |
| system/sysroot libraries | `OUT-OF-SCOPE` | `NOT_COVERED` | no sysroot or target filesystem is passed |
| compiler, linker, and host toolchain | `OUT-OF-SCOPE` | `NOT_COVERED` | `${TOOLCHAIN_NAME}` was observed only in the installation destination |
| libraries only linked externally | `OUT-OF-SCOPE` | `UNKNOWN/LIKELY_GAP` | no link map or linker graph is supplied |
| binaries/archives present under the root | `IN-SCOPE` | `CONDITIONAL` | depends on catalogers and archive/binary options |
| nested `.github` directories | `EXCLUDED_INTENT` | `NOT_COVERED` | argument `--exclude '*/**/.github'`; glob not tested |
| root `.github` directory | `UNKNOWN` | `UNKNOWN` | comment suggests preserving the root; no execution |
| release/tag/commit identity | n/a | `NOT_BOUND` | no identifier is passed by the observed command |
| platform identity | n/a | `NOT_BOUND` | installation destination does not prove SBOM metadata |
| deployment identity | n/a | `NOT_BOUND` | no separate file or per-deployment metadata was observed |
| licenses | `CONDITIONAL` | `UNKNOWN` | depends on the package, files, and enrichment/configuration |
| transitive relationships | `CONDITIONAL` | `UNKNOWN` | the observed mechanism provides no general guarantee |

## Conclusion

The mechanism is best described as Syft cataloging of a project tree after certain CMake targets, not as an SBOM of the final artifact, target filesystem, or complete build graph. The reference commit was frozen and verified in F0-R1D; the effective Syft version/configuration and execution behavior remain unknown because generation was not authorized. No `UNKNOWN` field is promoted by assumption.
