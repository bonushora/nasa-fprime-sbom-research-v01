#!/usr/bin/env bash
set -euo pipefail

repo_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)
output_root="$repo_root/evidence/v0.2/environment"
mkdir -p "$output_root"

for output in tool-versions.txt tool-binary-sha256.txt os-and-capacity.txt package-versions.txt python-validator-sha256.txt; do
    if [[ -e "$output_root/$output" ]]; then
        echo "refusing to overwrite environment evidence: $output_root/$output" >&2
        exit 73
    fi
done

{
    date -u +recorded_utc=%Y-%m-%dT%H:%M:%SZ
    /usr/bin/bwrap --version
    /usr/bin/cmake --version
    /usr/bin/python3 --version
    /usr/bin/ninja --version
    /usr/bin/git --version
    "$repo_root/.artifacts/v0.2/tools/syft" version
    python3 -c 'import jsonschema; print("python-jsonschema", jsonschema.__version__)'
} >"$output_root/tool-versions.txt" 2>&1

tool_paths=(
    /usr/bin/bwrap
    /usr/bin/cmake
    /usr/bin/python3.10
    /usr/bin/ninja
    /usr/bin/git
    /usr/bin/timeout
    /usr/bin/prlimit
    /usr/bin/dash
    /usr/bin/ip
    /usr/bin/find
    /usr/bin/sort
    "$repo_root/.artifacts/v0.2/tools/syft"
)
sha256sum "${tool_paths[@]}" >"$output_root/tool-binary-sha256.txt"

{
    uname -a
    sed -n '1,20p' /etc/os-release
    nproc
    free -b
    df -B1 "$repo_root"
    ulimit -a
} >"$output_root/os-and-capacity.txt"

dpkg-query -W -f='${Package}\t${Version}\t${Architecture}\n' \
    bubblewrap cmake python3 python3-jsonschema ninja-build git coreutils util-linux iproute2 findutils \
    >"$output_root/package-versions.txt"

python3 - <<'PY' >"$output_root/python-validator-sha256.txt"
import hashlib
from pathlib import Path
import jsonschema

root = Path(jsonschema.__file__).resolve().parent
for path in sorted(root.rglob("*.py")):
    print(hashlib.sha256(path.read_bytes()).hexdigest(), path)
PY

echo "toolchain evidence captured"

