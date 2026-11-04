# F0 — Scope and boundaries

## Mandate

This phase materializes local documentation and static analysis only. The declared governance is BH-SEP v2.3 / BH-SDP v2.3, with authorization `APPROVED — DOCUMENTATION_AND_READ_ONLY`, risk `LOW`, and initial state `NOT_QUALIFIED`.

Authorized workspace:

`/home/usuario/Desenvolvimento/bonushora/nasa-fprime-sbom-research-v01`

## In scope

- Reading official public sources from the `nasa/fprime` repository.
- Static inspection of `cmake/target/sbom.cmake`, `redirector.py`, and directly relevant CMake context.
- Recording identity, provenance, risks, known coverage, and gaps.
- Creating and syntactically validating the F0 documents in this workspace.
- Local commands limited to read-only inspection, date/time, hashing, and documentary validation.

## Out of scope and not executed

- Build, upstream CMake configuration, SBOM generation, or Syft execution.
- Execution of Python, CMake, tests, or any script obtained from upstream.
- Dependency installation or update.
- Cloning, checking out, or modifying NASA F´.
- Accessing or modifying the NASA cFS research project.
- Push, pull request, discussion, publication, or remote repository creation.
- Vulnerability assessment, exploitation, or security qualification.
- Any assertion that an official F´ release SBOM exists.

## Evidence boundary

The accessible official pages were served through a cached read channel. The `sbom.cmake` page indicated 53 lines and the `redirector.py` page 8 lines. The branch identity could not be resolved to a full commit. Therefore:

1. the content is evidence of a mechanism observed at the moving reference;
2. it is not evidence of an immutable baseline;
3. absent upstream hashes remain `UNKNOWN`;
4. SHA `f298b0f19dc2c5febcb9d9f72f474e2b2561b1b3` is recorded only as a previously observed blob supplied in the mandate, not as a commit or as a value revalidated in that session.

### F0-R1B update

The local evidence bridge made it possible to revalidate the transported bytes against the three declared Git blob OIDs and SHA-256 values. This verification replaces `UNKNOWN` only for the internal integrity of the package files. By itself, it does not demonstrate that the official commit/tree associates those blobs with the declared paths: the tree objects and an authenticated official response are not part of the package. Upstream provenance remained `BLOCKED`, and the CMake registration chain remained `PARTIAL` because two files cited by the manifest were not transported.

### F0-R1D closure

The R1C runner provided a physical shallow Git repository containing the fixed commit and tree. Offline validation traversed all 3,610 tracked entries in the superproject, confirmed five paths with `git ls-tree`, compared bytes from the pack with the transported copies, and reproduced the nine matches. There is one gitlink, `googletest`; its contents were neither traversed nor included in the completeness claim. Identity and the CMake chain are therefore closed within the explicit boundary “tracked superproject tree, excluding submodules.”

## Rules for future phases

Any executable phase requires new, explicit authorization. The future plan does not grant permission to execute the actions it describes.
