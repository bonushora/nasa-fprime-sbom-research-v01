# F Prime — Upstream Maintainer Dialogue Evidence v0.1

## Primary source

- Discussion: https://github.com/nasa/fprime/discussions/6311
- Title: Official SBOM availability and release-level dependency traceability for F´
- Opened by: @bonushora
- Created (UTC): 2026-11-03T22:05:15Z
- Maintainer response: https://github.com/nasa/fprime/discussions/6311#discussioncomment-19386109
- Response date (UTC): 2026-11-04T00:01:54Z
- Researcher follow-up: https://github.com/nasa/fprime/discussions/6311#discussioncomment-19388195
- Follow-up date (UTC): 2026-11-04T02:33:58Z

## Verbatim maintainer clarification

> The F Prime build system generates an SBOM using syft if it is installed on the build host https://github.com/nasa/fprime/blob/devel/cmake/target/sbom.cmake

## Researcher follow-up

The researcher thanked the maintainer and stated the intention to
investigate Syft-generated SPDX JSON at a pinned F Prime revision,
distinguishing independent build-generated results from official
release SBOMs.

The complete original text and comment metadata are preserved in
`discussion-6311-source.json`.

## Scientific relevance

The maintainer identified F Prime's native CMake/Syft SBOM
generation mechanism, conditional on Syft being installed.

This provides a primary-source basis for the methodological
choice to investigate that mechanism in the independent
F Prime SBOM v0.2 research.

## Evidence boundaries

- Confirms a public technical clarification by @thomas-bc.
- Does not establish an officially published release SBOM.
- Does not demonstrate maintainer review of the study's results.
- Does not establish external reproduction or SBOM completeness.
- Does not imply NASA, JPL, Caltech, or F Prime endorsement.
- This addendum was prepared after the v0.2 publication;
  it is not represented as part of the original frozen package.

MAINTAINER_TECHNICAL_CLARIFICATION=VERIFIED
MAINTAINER_REVIEW_OF_RESEARCH=NOT_VERIFIED
INSTITUTIONAL_ENDORSEMENT=NOT_CLAIMED
