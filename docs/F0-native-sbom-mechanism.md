# F0 — Native CMake/Syft mechanism

## Summary

The observed mechanism integrates Syft as an optional global CMake custom target. If `find_program` locates `syft`, the target participates in `ALL`, waits for the targets registered in `SBOM_DEPENDENCIES`, scans the `FPRIME_PROJECT_ROOT` directory, emits SPDX JSON to stdout, writes the result into the build tree through `redirector.py`, and triggers component installation. If Syft is not found, the code only records an informational message and does not create the observed target.

Initial primary source: [nasa/fprime `sbom.cmake` on `devel`](https://github.com/nasa/fprime/blob/devel/cmake/target/sbom.cmake). In F0-R1B, the content was confirmed against the blob. In F0-R1D, the commit→tree→path→blob binding was proven in the physical Git pack for commit `a4b1b1c043d1f9b51a7faba4a47d5d0f231910c7`.

## Observed flow

1. `FPRIME__INTERNAL_SBOM_REDIRECTOR` points to `tools/redirector.py` and is placed in the internal CMake cache.
2. `sbom_add_global_target(TARGET)` searches the configuration environment for an executable named `syft`.
3. When found, `add_custom_target("${TARGET}" ALL ...)` makes generation part of the default build.
4. The command invokes `${PYTHON}`, the redirector, and output path `${CMAKE_BINARY_DIR}/${PROJECT_NAME}_sbom.json`.
5. The redirector executes `"${SYFT}" "dir:${FPRIME_PROJECT_ROOT}" -o spdx-json --exclude '*/**/.github'` without a shell and sends stdout to the file.
6. `DEPENDS $<TARGET_PROPERTY:${TARGET},SBOM_DEPENDENCIES>` introduces build dependencies accumulated on the global target.
7. An `install(FILES ...)` rule associates the JSON with component `${TARGET}` and destination `${TOOLCHAIN_NAME}`.
8. A `POST_BUILD` command invokes CMake in script mode to install the component through `fprime_install.cmake`, passing the component, installation destination, and build directory in the most recently visible page content.

## Inputs and outputs

| Type | Element | Observation |
|---|---|---|
| input | `TARGET` | name of the custom target and installation component |
| input | `PATH` | selects the `syft` executable; no version is pinned |
| input | `${PYTHON}` | interpreter used for the redirector |
| input | `FPRIME_PROJECT_ROOT` | entire root passed to Syft's `dir:` source |
| input | Syft configuration/environment | not neutralized by the observed command |
| input | `SBOM_DEPENDENCIES` | orders the target after the registered CMake targets |
| output | `${CMAKE_BINARY_DIR}/${PROJECT_NAME}_sbom.json` | Syft stdout in `spdx-json` format |
| output | `${FPRIME_INSTALL_DEST}` / `${TOOLCHAIN_NAME}` | installed copy; final path depends on wrapper/variables |

## Deployment and module hooks

`sbom_add_deployment_target(MODULE TARGET SOURCES DEPENDENCIES FULL_DEPENDENCIES)` and `sbom_add_module_target(MODULE TARGET SOURCE_FILES DEPENDENCIES)` check whether `TARGET` exists and, if so, append `MODULE` to the specified target's `SBOM_DEPENDENCIES` property through `append_list_property`.

Important facts:

- The `SOURCES`, `SOURCE_FILES`, `DEPENDENCIES`, and `FULL_DEPENDENCIES` parameters are not used in the observed bodies of these hooks.
- The demonstrated effect is CMake target dependency/ordering, not transmission of a component graph to Syft.
- During initial F0, call sites outside the file and the concrete global target name had not been retrieved with frozen evidence and remained `UNKNOWN`; F0-R1D later resolved this within the recorded superproject scope.

## CMake chain — F0-R1B reconciliation

Confirmed directly in the verified bytes of `sbom.cmake`:

- definitions of `sbom_add_global_target`, `sbom_add_deployment_target`, and `sbom_add_module_target`;
- the global `ALL` target, its dependency on `SBOM_DEPENDENCIES`, the Syft argv, and post-build installation;
- module/deployment hooks that append the module to the target property without consuming the supplied dependency arguments.

Declared by the manifest but not confirmed from bytes present in the package:

- `cmake/FPrime.cmake:121` would call `register_fprime_target(target/sbom)`;
- `cmake/target/target.cmake:96-97` would perform global include/dispatch;
- the same dispatcher would call the module hook at line 121 and the deployment hook at line 140.

At F0-R1B, this chain remained `PARTIAL`: `FPrime.cmake` and `target.cmake` were not in the package, there was no complete tree/archive for a frozen search, and the manifest itself classified the enumeration as non-exhaustive. Registration/dispatch points were therefore declarative package evidence at that revision, not local upstream observations.

## CMake chain — F0-R1D closure

The R1C evidence confirms the complete chain in the tracked superproject tree:

1. `cmake/FPrime.cmake:121` registers `target/sbom` through `register_fprime_target`.
2. `cmake/API.cmake:636-638` appends the target to `FPRIME_TARGET_LIST` through `register_fprime_list_helper`.
3. `cmake/target/target.cmake:37-44` iterates over that list and calls `setup_global_target`.
4. `target.cmake:96-97` includes the plugin, derives the name `sbom`, and dynamically calls `sbom_add_global_target`.
5. `target.cmake:154-181` iterates over the same list for each build target; `setup_single_target` dynamically calls `sbom_add_module_target` at line 121 or `sbom_add_deployment_target` at line 140.
6. `sbom.cmake` defines the three functions and uses `SBOM_DEPENDENCIES` to order the global target after registered modules/deployments.

The literal search `target/sbom|sbom_add_|SBOM_DEPENDENCIES` returned exactly nine matches across the tracked tree: 1 registration, 2 documentary comments, 3 definitions, 1 property read, and 2 property writes. The dispatches do not appear among those nine matches because they are dynamic calls; they were confirmed separately at the same commit. The search covers the superproject and does not traverse the `googletest` gitlink. Result: `CMAKE_CHAIN=PASS` within that boundary.

## Scan scope and exclusions

The Syft source is explicitly a directory: `dir:${FPRIME_PROJECT_ROOT}`. This points to the project tree, not the build directory or installation directory. The only observed explicit exclusion is `*/**/.github`. The upstream comment states that the intent is to exclude `.github` outside the root; the exact glob semantics depend on the Syft version and were not executed in this phase.

Inference: build products outside `FPRIME_PROJECT_ROOT`, sysroots, host packages, and dependencies that are only linked externally do not enter this source's file universe. The CMake dependency causes the scan to occur after registered targets, but does not expand the scanned directory.

## Release, platform, and deployment

| Dimension | Observed binding |
|---|---|
| release/tag | no release, tag, or commit argument is passed to Syft |
| commit | no OID is passed to Syft or explicitly recorded by the observed CMake |
| platform/toolchain | `${TOOLCHAIN_NAME}` affects the installation destination; it was not observed as Syft command metadata |
| deployment | deployments may participate in ordering; no separate source or file per deployment appears in the observed excerpt |
| project | `${PROJECT_NAME}` forms part of the file name |

Conclusion: no verifiable binding between the generated JSON and an immutable release was observed. Any metadata Syft might derive on its own does not replace an explicit, attested binding in the CMake mechanism.

## Role of `redirector.py`

Source: [nasa/fprime `redirector.py` on `devel`](https://github.com/nasa/fprime/blob/devel/cmake/target/tools/redirector.py).

The helper only validates that it received at least one argument after the program name, opens the first argument in `w` mode, executes the remainder with `subprocess.run(..., stdout=file_handle)`, and returns the subprocess return code. It does not use a shell, validate the JSON, capture stderr, make the write atomic, or avoid truncating an existing file before Syft is known to have succeeded.

## Limitations of this characterization

- Commit identity, upstream hashes, and complete call-site enumeration were initial limitations that F0-R1D resolved within the tracked superproject tree, excluding submodules.
- The minimum/maximum Syft version and the effective SPDX version are not pinned by the command.
- No execution confirmed the glob semantics, output content, failure behavior, or final installed path.
