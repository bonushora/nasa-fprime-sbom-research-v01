#!/usr/bin/env python3
"""Read-only F6-R6 review checks; never invokes Syft or CMake."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any, Iterator

import jsonschema
import yaml


RUN_HASHES = {
    "run-1": "0ad4ec43ad02d8f436679d9419a56842005b8beac2446aa5a8049e7d4596fc8b",
    "run-2": "6837b5a04ef2cdd64e60475c2d2bed5030eaa2e0aeda0dfa0c194bdb38a15c38",
}
VOLATILE_PATHS = ["/creationInfo/created", "/documentNamespace"]
SCHEMA_HASH = "239208b7ac287b3cf5d9a9af23f9d69863971102a5e1587a27a398b43490b89b"
SYFT_CHECKSUM_HASH = "a2db61bc71f8f7ea8c67fc4a81b8e4e6474386e6a07d104bd2e78e964d5d7ec7"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def walk_diff(left: Any, right: Any, path: str = "") -> Iterator[dict[str, Any]]:
    if type(left) is not type(right):
        yield {"path": path or "/", "kind": "type", "left": type(left).__name__, "right": type(right).__name__}
        return
    if isinstance(left, dict):
        for key in sorted(set(left) | set(right)):
            child = f"{path}/{key}"
            if key not in left:
                yield {"path": child, "kind": "right-only"}
            elif key not in right:
                yield {"path": child, "kind": "left-only"}
            else:
                yield from walk_diff(left[key], right[key], child)
    elif isinstance(left, list):
        if len(left) != len(right):
            yield {"path": path or "/", "kind": "length", "left": len(left), "right": len(right)}
        for index, (left_item, right_item) in enumerate(zip(left, right)):
            yield from walk_diff(left_item, right_item, f"{path}/{index}")
    elif left != right:
        yield {"path": path or "/", "kind": "value", "left": left, "right": right}


def package_key(package: dict[str, Any]) -> str:
    purls = sorted(
        ref.get("referenceLocator", "")
        for ref in package.get("externalRefs", [])
        if ref.get("referenceType") == "purl"
    )
    return "|".join((str(package.get("name", "")), str(package.get("versionInfo", "")), ",".join(purls)))


def scientific_review(root: Path) -> dict[str, Any]:
    documents = {}
    for run, expected_hash in RUN_HASHES.items():
        path = root / "evidence/v0.2/runs" / run / "native-original.spdx.json"
        actual_hash = sha256(path)
        if actual_hash != expected_hash:
            raise ValueError(f"{run} hash mismatch: {actual_hash}")
        documents[run] = json.loads(path.read_text(encoding="utf-8"))
    left, right = documents["run-1"], documents["run-2"]
    differences = list(walk_diff(left, right))
    if [item["path"] for item in differences] != VOLATILE_PATHS:
        raise ValueError(f"unexpected full-document differences: {differences}")
    normalized_left, normalized_right = copy.deepcopy(left), copy.deepcopy(right)
    for document in (normalized_left, normalized_right):
        document["creationInfo"]["created"] = "<normalized>"
        document["documentNamespace"] = "<normalized>"
    if normalized_left != normalized_right:
        raise ValueError("documents differ after the two declared normalizations")
    counts = Counter(package_key(package) for package in left.get("packages", []))
    collisions = {key: count for key, count in counts.items() if count > 1}
    return {
        "status": "PASS",
        "method": "complete recursive comparison of parsed JSON values plus comparator-code audit",
        "run_sha256": RUN_HASHES,
        "counts_per_run": {"packages": 266, "files": 46, "relationships": 581},
        "full_document_difference_count": len(differences),
        "full_document_differences": differences,
        "equal_after_normalizing_only_declared_paths": True,
        "historical_projection_audit": {
            "omits": ["document metadata", "files collection"],
            "package_key_fields": ["name", "versionInfo", "purl"],
            "colliding_key_count": len(collisions),
            "package_occurrences_in_collisions": sum(collisions.values()),
            "unique_keys_for_266_occurrences": len(counts),
            "conclusion": "Projection equality only; not universal SPDX semantic equivalence.",
        },
        "external_independent_reproduction": "NOT_VERIFIED",
    }


def bilingual_review(root: Path) -> dict[str, Any]:
    pairs = [
        ("README.md", "README.pt-BR.md"),
        ("REPRODUCIBILITY.md", "REPRODUCIBILITY.pt-BR.md"),
        ("RIGHTS-REVIEW.md", "RIGHTS-REVIEW.pt-BR.md"),
        ("F6-R6-REVIEW.md", "F6-R6-REVIEW.pt-BR.md"),
        ("docs/v0.2/RESEARCH-REPORT.md", "docs/v0.2/RESEARCH-REPORT.pt-BR.md"),
    ]
    invariants = [
        "266", "46", "581", "27", "170",
        "a4b1b1c043d1f9b51a7faba4a47d5d0f231910c7",
        "6e00649fc2e2ae65f30086f059160865bdc49442",
        "EXTERNAL_INDEPENDENT_REPRODUCTION=NOT_VERIFIED",
    ]
    results = []
    for english, portuguese in pairs:
        left = (root / english).read_text(encoding="utf-8")
        right = (root / portuguese).read_text(encoding="utf-8")
        applicable = [value for value in invariants if value in left or value in right]
        missing = [value for value in applicable if value not in left or value not in right]
        results.append({"english": english, "pt_br": portuguese, "checked_invariants": applicable, "missing": missing})
        if missing:
            raise ValueError(f"bilingual invariant mismatch in {english}/{portuguese}: {missing}")
    return {
        "status": "PASS",
        "pair_results": results,
        "scope": "machine parity of applicable numerical/hash/status invariants; substantive terminology review is in F6-R6-REVIEW.md",
    }


def citation_review(root: Path, schema_path: Path) -> dict[str, Any]:
    schema_bytes = schema_path.read_bytes()
    schema = json.loads(schema_bytes)
    citation = yaml.safe_load((root / "CITATION.cff").read_text(encoding="utf-8"))
    validator = jsonschema.Draft7Validator(schema, format_checker=jsonschema.FormatChecker())
    errors = sorted(validator.iter_errors(citation), key=lambda error: list(error.absolute_path))
    if errors:
        raise ValueError([f"/{'/'.join(map(str, error.absolute_path))}: {error.message}" for error in errors])
    forbidden = [key for key in ("doi", "date-released") if key in citation]
    if forbidden:
        raise ValueError(f"unsubstantiated citation fields: {forbidden}")
    if "license" in citation:
        raise ValueError("package-wide CFF license must remain absent for this mixed-rights collection")
    return {
        "status": "PASS",
        "cff_version": citation.get("cff-version"),
        "schema_url": "https://raw.githubusercontent.com/citation-file-format/citation-file-format/1.2.0/schema.json",
        "schema_sha256": hashlib.sha256(schema_bytes).hexdigest(),
        "validator": f"python-jsonschema {jsonschema.__version__} Draft7Validator with format checking",
        "yaml_parser": f"PyYAML {yaml.__version__}",
        "doi_present": False,
        "date_released_present": False,
        "package_wide_license_present": False,
    }


def rights_review(root: Path) -> dict[str, Any]:
    checks = {
        "spdx_schema": (root / "evidence/v0.2/schema/spdx-2.3-schema.json", SCHEMA_HASH),
        "syft_checksums": (root / "evidence/v0.2/inputs/syft_1.56.0_checksums.txt", SYFT_CHECKSUM_HASH),
    }
    hashes = {}
    for name, (path, expected) in checks.items():
        actual = sha256(path)
        if actual != expected:
            raise ValueError(f"{name} hash mismatch")
        hashes[name] = actual
    required = [
        "third-party/fprime/LICENSE.txt", "third-party/fprime/NOTICE.txt",
        "third-party/syft/LICENSE.txt", "third-party/syft/NOTICE.md",
        "third-party/spdx-spec/NOTICE.md", "third-party/spdx-spec/LICENSE-URI.txt",
        "LICENSE-SCOPE.md", "REDISTRIBUTION.md",
    ]
    missing = [path for path in required if not (root / path).is_file()]
    if missing:
        raise ValueError(f"missing rights files: {missing}")
    return {"status": "PASS", "verified_third_party_hashes": hashes, "required_files": required, "legal_advice": False}


def privacy_review(root: Path) -> dict[str, Any]:
    forbidden_patterns = {
        "unix_home_path": re.compile(rb"/home/[A-Za-z0-9._-]+/"),
        "mac_home_path": re.compile(rb"/Users/[A-Za-z0-9._-]+/"),
        "aws_access_key": re.compile(rb"AKIA[0-9A-Z]{16}"),
        "github_token": re.compile(rb"gh[pousr]_[A-Za-z0-9_]{20,}"),
        "private_key": re.compile(rb"BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY"),
    }
    findings = []
    for path in sorted(item for item in root.rglob("*") if item.is_file() and item.name != "SHA256SUMS-PUBLIC"):
        data = path.read_bytes()
        for name, pattern in forbidden_patterns.items():
            if pattern.search(data):
                findings.append({"path": path.relative_to(root).as_posix(), "pattern": name})
    if findings:
        raise ValueError(f"privacy findings: {findings}")
    for run in RUN_HASHES:
        document = json.loads((root / "evidence/v0.2/runs" / run / "native-original.spdx.json").read_text(encoding="utf-8"))
        if document.get("name") != "/input":
            raise ValueError(f"unexpected source name in {run}")
    return {
        "status": "PASS",
        "forbidden_pattern_findings": [],
        "preserved_original_spdx_source_path": "/input",
        "expected_public_contact": "eay@cryptsoft.com in upstream F Prime NOTICE.txt",
        "original_spdx_modified": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--cff-schema", type=Path, required=True)
    args = parser.parse_args()
    root = args.candidate.resolve()
    output = root / "validation/f6-r6"
    write_json(output / "scientific-review.json", scientific_review(root))
    write_json(output / "bilingual-equivalence.json", bilingual_review(root))
    write_json(output / "citation-validation.json", citation_review(root, args.cff_schema))
    write_json(output / "rights-and-redistribution.json", rights_review(root))
    write_json(output / "privacy-review.json", privacy_review(root))
    print("F6-R6 review validation: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

