#!/usr/bin/env python3
"""Independent, non-Syft enumeration of tracked source declarations and files."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path


DECLARATION_NAMES = {
    "requirements.txt",
    "pyproject.toml",
    "setup.py",
    "setup.cfg",
    "package.json",
    "package-lock.json",
    "go.mod",
    "go.sum",
    "Cargo.toml",
    "Cargo.lock",
    "CMakeLists.txt",
}
LICENSE_RE = re.compile(r"^(licen[cs]e|copying|notice|copyright|attribution)(\..*)?$", re.IGNORECASE)


def sha256(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    source = args.source.resolve()
    files = sorted(path for path in source.rglob("*") if path.is_file() and not path.is_symlink())
    declarations = []
    licenses = []
    extensions: dict[str, int] = {}
    for path in files:
        relative = path.relative_to(source).as_posix()
        extensions[path.suffix.lower() or "<none>"] = extensions.get(path.suffix.lower() or "<none>", 0) + 1
        entry = {"path": relative, "sha256": sha256(path), "size": path.stat().st_size}
        if path.name in DECLARATION_NAMES:
            declarations.append(entry)
        if LICENSE_RE.match(path.name):
            licenses.append(entry)
    report = {
        "method": "independent filename classification and SHA-256 enumeration; no Syft code or output consumed",
        "source_root": "/input",
        "regular_files": len(files),
        "total_bytes": sum(path.stat().st_size for path in files),
        "extension_counts": dict(sorted(extensions.items())),
        "declaration_files": declarations,
        "license_notice_files": licenses,
        "limitations": [
            "Filename classification enumerates declarations; it does not resolve or compile dependencies.",
            "The uninitialized googletest gitlink has no files in the exported tree and is recorded separately.",
        ],
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

