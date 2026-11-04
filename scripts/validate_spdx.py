#!/usr/bin/env python3
"""Validate the structural and referential invariants used by this study."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import jsonschema


def fail(message: str) -> None:
    raise ValueError(message)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("spdx", type=Path)
    parser.add_argument("--schema", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()

    raw = args.spdx.read_bytes()
    doc: dict[str, Any] = json.loads(raw)
    schema_raw = args.schema.read_bytes()
    schema = json.loads(schema_raw)
    validator_class = jsonschema.validators.validator_for(schema)
    validator_class.check_schema(schema)
    schema_errors = sorted(validator_class(schema).iter_errors(doc), key=lambda error: list(error.absolute_path))
    if schema_errors:
        rendered = [f"/{'/'.join(map(str, error.absolute_path))}: {error.message}" for error in schema_errors]
        fail(f"official schema validation failed: {rendered}")
    required = ["spdxVersion", "SPDXID", "name", "documentNamespace", "creationInfo", "packages", "relationships"]
    missing = [field for field in required if field not in doc]
    if missing:
        fail(f"missing document fields: {missing}")
    if not str(doc["spdxVersion"]).startswith("SPDX-2."):
        fail(f"unexpected SPDX version: {doc['spdxVersion']}")
    if doc["SPDXID"] != "SPDXRef-DOCUMENT":
        fail(f"unexpected document SPDXID: {doc['SPDXID']}")

    ids = {doc["SPDXID"]}
    duplicate_ids: list[str] = []
    for collection in ("packages", "files", "snippets"):
        for item in doc.get(collection, []):
            spdx_id = item.get("SPDXID")
            if not spdx_id:
                fail(f"item without SPDXID in {collection}")
            if spdx_id in ids:
                duplicate_ids.append(spdx_id)
            ids.add(spdx_id)
    if duplicate_ids:
        fail(f"duplicate SPDXIDs: {sorted(set(duplicate_ids))}")

    external = {"NONE", "NOASSERTION"}
    dangling: list[dict[str, str]] = []
    for relationship in doc["relationships"]:
        source = relationship.get("spdxElementId", "")
        target = relationship.get("relatedSpdxElement", "")
        if source not in ids and source not in external:
            dangling.append({"side": "source", "id": source})
        if target not in ids and target not in external:
            dangling.append({"side": "target", "id": target})
    if dangling:
        fail(f"dangling relationship references: {dangling}")

    package_names = sorted(str(item.get("name", "")) for item in doc["packages"])
    report = {
        "validator": "scripts/validate_spdx.py",
        "sha256": hashlib.sha256(raw).hexdigest(),
        "json_syntax": "PASS",
        "official_spdx_2_3_json_schema": "PASS",
        "schema_sha256": hashlib.sha256(schema_raw).hexdigest(),
        "jsonschema_python_version": getattr(jsonschema, "__version__", "unknown"),
        "spdx_structural_profile": "PASS",
        "relationship_references": "PASS",
        "spdx_version": doc["spdxVersion"],
        "data_license": doc.get("dataLicense"),
        "packages": len(doc["packages"]),
        "files": len(doc.get("files", [])),
        "relationships": len(doc["relationships"]),
        "package_names": package_names,
        "limitations": [
            "This is a local structural and referential validator, not official SPDX certification.",
            "A valid document does not establish dependency completeness, vulnerability absence, or binary coverage.",
        ],
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

