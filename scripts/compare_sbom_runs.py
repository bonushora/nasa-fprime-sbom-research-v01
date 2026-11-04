#!/usr/bin/env python3
"""Separate volatile SPDX fields from semantic package/relationship content."""

from __future__ import annotations

import argparse
import hashlib
import json
from copy import deepcopy
from pathlib import Path
from typing import Any


def canonical_package(package: dict[str, Any]) -> dict[str, Any]:
    value = deepcopy(package)
    value.pop("SPDXID", None)
    return value


def package_key(package: dict[str, Any]) -> str:
    refs = package.get("externalRefs", [])
    purls = sorted(ref.get("referenceLocator", "") for ref in refs if ref.get("referenceType") == "purl")
    return "|".join([str(package.get("name", "")), str(package.get("versionInfo", "")), ",".join(purls)])


def semantic_model(doc: dict[str, Any]) -> dict[str, Any]:
    packages_by_id = {package["SPDXID"]: package_key(package) for package in doc.get("packages", [])}
    relationships = []
    for relationship in doc.get("relationships", []):
        source = packages_by_id.get(relationship.get("spdxElementId"), relationship.get("spdxElementId"))
        target = packages_by_id.get(relationship.get("relatedSpdxElement"), relationship.get("relatedSpdxElement"))
        relationships.append([source, relationship.get("relationshipType"), target])
    packages = [(package_key(package), canonical_package(package)) for package in doc.get("packages", [])]
    packages.sort(key=lambda item: (item[0], json.dumps(item[1], sort_keys=True, separators=(",", ":"))))
    return {
        "packages": packages,
        "relationships": sorted(relationships),
    }


def digest(value: Any) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("run1", type=Path)
    parser.add_argument("run2", type=Path)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    raw1, raw2 = args.run1.read_bytes(), args.run2.read_bytes()
    doc1, doc2 = json.loads(raw1), json.loads(raw2)
    model1, model2 = semantic_model(doc1), semantic_model(doc2)
    keys1 = {key for key, _ in model1["packages"]}
    keys2 = {key for key, _ in model2["packages"]}
    report = {
        "byte_identical": raw1 == raw2,
        "run_1_sha256": hashlib.sha256(raw1).hexdigest(),
        "run_2_sha256": hashlib.sha256(raw2).hexdigest(),
        "run_1_created": doc1.get("creationInfo", {}).get("created"),
        "run_2_created": doc2.get("creationInfo", {}).get("created"),
        "run_1_namespace": doc1.get("documentNamespace"),
        "run_2_namespace": doc2.get("documentNamespace"),
        "semantic_sha256_run_1": digest(model1),
        "semantic_sha256_run_2": digest(model2),
        "semantic_identical": model1 == model2,
        "packages_only_run_1": sorted(keys1 - keys2),
        "packages_only_run_2": sorted(keys2 - keys1),
        "classification": "VOLATILE_ONLY" if raw1 != raw2 and model1 == model2 else ("IDENTICAL" if raw1 == raw2 else "SEMANTIC_DIVERGENCE"),
        "normalization_scope": [
            "document creation timestamp",
            "document namespace",
            "SPDX element IDs mapped to stable package name/version/PURL keys for relationships",
        ],
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0 if model1 == model2 else 1


if __name__ == "__main__":
    raise SystemExit(main())

