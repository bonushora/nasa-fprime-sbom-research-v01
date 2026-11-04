#!/usr/bin/env python3
"""Compare independent declarations/resolutions with the native Syft result."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


REQ_RE = re.compile(r"^([A-Za-z0-9_.-]+)==([^;\s]+)")
USES_RE = re.compile(r"\buses:\s*['\"]?([^@\s'\"]+)@([^\s#'\"]+)")
REGISTER_RE = re.compile(r"\bregister_fprime_(module|deployment|library)\s*\(", re.IGNORECASE)


def pep_name(value: str) -> str:
    return re.sub(r"[-_.]+", "-", value).lower()


def package_pairs(doc: dict[str, Any]) -> set[tuple[str, str]]:
    return {(pep_name(str(item.get("name", ""))), str(item.get("versionInfo", ""))) for item in doc.get("packages", [])}


def parse_requirements(source: Path) -> set[tuple[str, str]]:
    values: set[tuple[str, str]] = set()
    for path in source.rglob("requirements*.txt"):
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            match = REQ_RE.match(line.strip())
            if match:
                values.add((pep_name(match.group(1)), match.group(2)))
    return values


def parse_cargo_locks(source: Path) -> set[tuple[str, str]]:
    values: set[tuple[str, str]] = set()
    for path in source.rglob("Cargo.lock"):
        name = None
        version = None
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines() + ["[[package]]"]:
            if line.strip() == "[[package]]":
                if name is not None and version is not None:
                    values.add((pep_name(name), version))
                name = version = None
            elif line.startswith("name = "):
                name = line.split("=", 1)[1].strip().strip('"')
            elif line.startswith("version = "):
                version = line.split("=", 1)[1].strip().strip('"')
    return values


def parse_actions(source: Path) -> set[tuple[str, str]]:
    values: set[tuple[str, str]] = set()
    github = source / ".github"
    if not github.exists():
        return values
    for path in github.rglob("*.y*ml"):
        for match in USES_RE.finditer(path.read_text(encoding="utf-8", errors="replace")):
            name, version = match.groups()
            if not name.startswith(("./", "docker://")):
                values.add((pep_name(name), version))
    return values


def count_cmake_registrations(source: Path) -> dict[str, int]:
    counts = {"module": 0, "deployment": 0, "library": 0}
    for path in source.rglob("CMakeLists.txt"):
        for kind in REGISTER_RE.findall(path.read_text(encoding="utf-8", errors="replace")):
            counts[kind.lower()] += 1
    return counts


def serialize(values: set[tuple[str, str]]) -> list[dict[str, str]]:
    return [{"name": name, "version": version} for name, version in sorted(values)]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("spdx", type=Path)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    source = args.source.resolve()
    native = package_pairs(json.loads(args.spdx.read_text(encoding="utf-8")))
    requirements = parse_requirements(source)
    cargo = parse_cargo_locks(source)
    actions = parse_actions(source)
    declared = requirements | actions
    resolved = cargo
    report = {
        "classification_model": {
            "declared": "Pinned Python requirements and GitHub Action uses parsed independently from source declarations.",
            "resolved": "Cargo.lock package name/version entries parsed independently.",
            "detected": "Unique name/version pairs emitted as packages by the native Syft SPDX.",
            "compiled": "NOT_MEASURED: the research harness invokes the native source SBOM target without compiling F Prime.",
            "distributed": "NOT_MEASURED: no flight binary, release bundle, or production installation was built.",
        },
        "counts": {
            "declared_unique": len(declared),
            "python_requirements_unique": len(requirements),
            "github_actions_unique": len(actions),
            "resolved_cargo_lock_unique": len(resolved),
            "native_detected_unique_name_version": len(native),
        },
        "cmake_registration_calls": count_cmake_registrations(source),
        "python_requirements_not_detected": serialize(requirements - native),
        "cargo_lock_not_detected": serialize(resolved - native),
        "github_actions_not_detected": serialize(actions - native),
        "native_detected_not_in_selected_declaration_sets": serialize(native - declared - resolved),
        "interpretation_limits": [
            "Set differences may reflect ecosystem normalization, conditional markers, local/root packages, or cataloger scope.",
            "Agreement establishes only agreement for the selected declaration classes; it is not proof of completeness.",
            "CMake registration calls are source declarations, not a configured, compiled, linked, or distributed graph.",
        ],
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

