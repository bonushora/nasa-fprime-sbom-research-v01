# F0 — Upstream identity

## Result

`BASELINE_FREEZE=PASS`

During the initial F0 observation, the complete identity of `devel` could not be verified. Consequently, the upstream identity requirement failed closed at that stage.

In revision F0-R1, an independent reference supplied a candidate commit and three candidate blobs, but the immutable official endpoints remained inaccessible. Those values were not promoted to verified identity.

In revision F0-R1B, the bytes of those three files were received in a local package and their hashes were confirmed. Content identity was confirmed within the package; the upstream commit→tree→path→blob binding still lacked self-contained local proof.

In revision F0-R1D, the physical R1C evidence supplied the required Git objects. The commit, root tree, and bindings for five files were confirmed directly in the object database; the limitations described above remain as history of the earlier revisions.

## Initial F0 observation record

| Field | Value | Classification |
|---|---|---|
| Repository | `https://github.com/nasa/fprime` | observed fact |
| Requested branch | `devel` | observed fact; moving reference |
| Full `devel` commit | `UNKNOWN` | blocker |
| Local observation | `2026-11-03T23:43:03-03:00` | local fact |
| UTC observation | `2026-11-04T02:43:03Z` | local fact |
| Primary URL | `https://github.com/nasa/fprime/blob/devel/cmake/target/sbom.cmake` | observed fact |
| Helper URL | `https://github.com/nasa/fprime/blob/devel/cmake/target/tools/redirector.py` | observed fact |
| Blob SHA supplied in the mandate | `f298b0f19dc2c5febcb9d9f72f474e2b2561b1b3` | previously observed; not revalidated |

## F0-R1 — external candidate reference

| Field | Supplied value | Local status |
|---|---|---|
| Candidate commit | `a4b1b1c043d1f9b51a7faba4a47d5d0f231910c7` | `EXTERNAL_UNVERIFIED` |
| Blob `cmake/target/sbom.cmake` | `f298b0f19dc2c5febcb9d9f72f474e2b2561b1b3` | `EXTERNAL_UNVERIFIED` |
| Blob `cmake/target/tools/redirector.py` | `e92f70416a0ec6fe0da933a1cf698af66a8e3808` | `EXTERNAL_UNVERIFIED` |
| Blob `cmake/target/install.cmake` | `a0e14e139927c0ea125cd67134b79a460959d71b` | `EXTERNAL_UNVERIFIED` |
| Local attempt | `2026-11-03T23:53:10-03:00` | local fact |
| UTC attempt | `2026-11-04T02:53:10Z` | local fact |

Commit→tree→path→blob bindings: `NOT_VERIFIED`. Immutable bytes: `NOT_OBTAINED`. Local upstream SHA-256: `NOT_COMPUTED`. Call sites at the candidate commit: `NOT_ENUMERATED`. Comparison against the F0 characterization: `NOT_PERFORMED`, because the candidate revision content was not retrieved.

## F0-R1B — offline package verification

Package: `.artifacts/f0-r1b-evidence/FPRIME-SBOM-F0-R1B-EVIDENCE-v01/`

| Item | Size | Local SHA-256 | Local Git blob OID | Result |
|---|---:|---|---|---|
| `cmake/target/sbom.cmake` | 2363 | `aa720bb92c6f3a4525770b59a0c35830d35975f49b9cbb38096669c2643b9eae` | `f298b0f19dc2c5febcb9d9f72f474e2b2561b1b3` | `PASS` |
| `cmake/target/tools/redirector.py` | 236 | `a8ae0dd04044739643fd9f5f96e45dfe1f0a23e7a5fc3bf31f33b74bda5353a4` | `e92f70416a0ec6fe0da933a1cf698af66a8e3808` | `PASS` |
| `cmake/target/install.cmake` | 3246 | `279c06cf3682ee0374dc89b496c014a4af816baac8993cec04cce6066c31df43` | `a0e14e139927c0ea125cd67134b79a460959d71b` | `PASS` |

The OIDs were calculated with `git hash-object --no-filters` and, independently, as the SHA-1 of `blob <size>\0<bytes>`. `verify_evidence.py` was not executed. Envelope hashes: manifest `03247b5ee641ad3bd703c0a7de40008b48b6232197d35fd4f9b03a952e3572b7`, README `54cf5e5a7b16b08ffdb19eee9780a6ddd30d344e62e952c02ecbb8542eef9ef5`, and unexecuted verifier `0c31a42bc1ec8901b12119a0c620cbd1d8a48fca5beb7af828a1d5f917813755`.

The manifest declares commit `a4b1b1c043d1f9b51a7faba4a47d5d0f231910c7`, commit tree `af4e2084aa84d51e82949c42f116d91301f65d81`, and descendant trees, but also states that it does not contain complete proof of the tree objects and that those records were checked separately during preparation. Result: `PACKAGE_INTEGRITY=PASS`; `UPSTREAM_TREE_BINDING=BLOCKED`.

## F0-R1D — closure through physical Git objects

Source: `.artifacts/f0-r1c-upstream-closure-v01/`.

| Field | Verified value |
|---|---|
| Recorded remote | `https://github.com/nasa/fprime.git` |
| Commit | `a4b1b1c043d1f9b51a7faba4a47d5d0f231910c7` |
| Object type | `commit` |
| Root tree | `af4e2084aa84d51e82949c42f116d91301f65d81` |
| Tracked inventory | 3,610 entries, identical to `git ls-tree -r --full-tree` |
| Gitlinks | 1: `googletest` (`58d77fa8070e8cec2dc1ed015d66b454c8d78850`) |
| Search scope | tracked superproject tree; submodules not traversed |

`git fsck --full --strict` found no corruption; it reported only that the evidence repository has no default reference, an expected condition for the shallow package centered on the fixed object.

| Path | Git blob OID | SHA-256 | Bytes |
|---|---|---|---:|
| `cmake/target/sbom.cmake` | `f298b0f19dc2c5febcb9d9f72f474e2b2561b1b3` | `aa720bb92c6f3a4525770b59a0c35830d35975f49b9cbb38096669c2643b9eae` | 2363 |
| `cmake/target/tools/redirector.py` | `e92f70416a0ec6fe0da933a1cf698af66a8e3808` | `a8ae0dd04044739643fd9f5f96e45dfe1f0a23e7a5fc3bf31f33b74bda5353a4` | 236 |
| `cmake/target/install.cmake` | `a0e14e139927c0ea125cd67134b79a460959d71b` | `279c06cf3682ee0374dc89b496c014a4af816baac8993cec04cce6066c31df43` | 3246 |
| `cmake/FPrime.cmake` | `762cdbdafd24cbb748c70b8600a1498eb8e0dc56` | `f63058c664e9e1741bfd429185e07e784c5124e9b8d97da7e8a260b3cce0126d` | 12403 |
| `cmake/target/target.cmake` | `006218f8a6a454f96a1a8e50457a60223ebfea22` | `de8e57b54cec8b3d7f34d6754e3d825c8f437c79a1fb75382c78323ba8a9c294` | 8512 |

For each path, the OID from `ls-tree`, the blob in the pack, the transported copy, the size, and the SHA-256 value matched. Result: `UPSTREAM_IDENTITY=PASS` within the recorded scope.

Attempted immutable URLs included:

- `https://github.com/nasa/fprime/commit/a4b1b1c043d1f9b51a7faba4a47d5d0f231910c7`
- `https://api.github.com/repos/nasa/fprime/git/commits/a4b1b1c043d1f9b51a7faba4a47d5d0f231910c7`
- `https://api.github.com/repos/nasa/fprime/git/trees/a4b1b1c043d1f9b51a7faba4a47d5d0f231910c7?recursive=1`
- `https://raw.githubusercontent.com/nasa/fprime/a4b1b1c043d1f9b51a7faba4a47d5d0f231910c7/cmake/target/sbom.cmake`
- `blob/<commit>/<path>` pages for the three files.

## Upstream files inspected in F0-R1B — historical record

| Path | Reference read | Upstream hash verified in this F0 | Status |
|---|---|---|---|
| `cmake/target/sbom.cmake` | package attributed to the candidate commit | local Git blob and SHA-256 confirmed | upstream path/tree not confirmed |
| `cmake/target/tools/redirector.py` | package attributed to the candidate commit | local Git blob and SHA-256 confirmed | upstream path/tree not confirmed |
| `cmake/target/install.cmake` | package attributed to the candidate commit | local Git blob and SHA-256 confirmed | upstream path/tree not confirmed |

The supplied blob hash was not reused as a hash of the then-current content because: (a) it does not identify the repository commit; (b) there was no official Git object response binding that blob to the path at the observed head; and (c) the channel exposed cached snapshots of different ages.

## Attempts and limitations

- The official branch page and file pages were readable.
- `git ls-remote https://github.com/nasa/fprime.git refs/heads/devel` failed with `Could not resolve host: github.com`.
- The official endpoint `https://api.github.com/repos/nasa/fprime/commits/devel` was unavailable through the read channel.
- The available history page was cached and did not demonstrably represent the head at the local observation time.
- In F0-R1, `git ls-remote` repeated the DNS failure; the immutable commit, tree, raw, and blob endpoints returned unavailability or cache misses through the read channel.
- No clone, archive download, or upstream content execution was performed.

## Closure conclusion

The previous unblocking conditions were satisfied by the R1C evidence: content-addressed identity, the tree, five files, and the frozen enumeration are available and verified. This closes only the F0 documentary baseline; it is not release authentication, a published signature, SBOM generation, or security qualification.
