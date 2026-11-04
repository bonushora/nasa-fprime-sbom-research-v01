#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
    echo "usage: $0 RUN_ID" >&2
    exit 64
fi

run_id=$1
case "$run_id" in
    run-1|run-2) ;;
    *) echo "RUN_ID must be run-1 or run-2" >&2; exit 64 ;;
esac

repo_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)
source_root="$repo_root/.artifacts/v0.2/source"
tool_root="$repo_root/.artifacts/v0.2/tools"
harness_root="$repo_root/experiment/native-harness"
run_root="$repo_root/evidence/v0.2/runs/$run_id"

for required in \
    "$source_root/cmake/target/sbom.cmake" \
    "$source_root/cmake/target/tools/redirector.py" \
    "$source_root/cmake/target/fprime_install.cmake" \
    "$tool_root/syft" \
    "$harness_root/CMakeLists.txt"; do
    if [[ ! -f "$required" ]]; then
        echo "missing required input: $required" >&2
        exit 66
    fi
done

if [[ -e "$run_root" ]]; then
    echo "refusing to overwrite existing run: $run_root" >&2
    exit 73
fi

mkdir -p "$run_root/work/home" "$run_root/work/cache" "$run_root/logs"

start_utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)
printf '%s\n' "$start_utc" >"$run_root/start-utc.txt"

set +e
timeout --signal=TERM --kill-after=15s 10m \
prlimit --as=2147483648 --cpu=600 --nproc=4096 --nofile=1024 --fsize=104857600 -- \
bwrap \
    --unshare-user --unshare-pid --unshare-ipc --unshare-uts --unshare-cgroup-try --unshare-net \
    --die-with-parent --new-session --clearenv \
    --ro-bind /usr /usr \
    --ro-bind /lib /lib \
    --ro-bind /lib64 /lib64 \
    --symlink usr/bin /bin \
    --symlink usr/sbin /sbin \
    --ro-bind "$source_root" /input \
    --ro-bind "$tool_root" /tool \
    --ro-bind "$harness_root" /harness \
    --bind "$run_root/work" /work \
    --proc /proc --dev /dev --tmpfs /tmp \
    --setenv HOME /work/home \
    --setenv XDG_CACHE_HOME /work/cache \
    --setenv PATH /tool:/usr/bin \
    --setenv LANG C.UTF-8 \
    --setenv LC_ALL C.UTF-8 \
    --setenv TZ UTC \
    --setenv SYFT_CHECK_FOR_APP_UPDATE false \
    --chdir /work \
    /usr/bin/sh -eu -c '
        mkdir -p /work/build /work/install
        printf "network-namespace:\n"
        ip link
        printf "visible-root:\n"
        find / -mindepth 1 -maxdepth 1 -printf "%f\n" | sort
        printf "identities:\n"
        id
        /tool/syft version
        /usr/bin/cmake --version
        /usr/bin/python3 --version
        /usr/bin/cmake -S /harness -B /work/build -G Ninja \
            -DFPRIME_FRAMEWORK_PATH=/input \
            -DFPRIME_PROJECT_ROOT=/input \
            -DFPRIME_INSTALL_DEST=/work/install \
            -DPYTHON=/usr/bin/python3 \
            -DTOOLCHAIN_NAME=Linux
        /usr/bin/cmake --build /work/build --target sbom --verbose
    ' >"$run_root/logs/execution.log" 2>&1
status=$?
set -e

end_utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)
printf '%s\n' "$end_utc" >"$run_root/end-utc.txt"
printf '%s\n' "$status" >"$run_root/exit-code.txt"

sbom="$run_root/work/build/FPrimeNativeSbomExperiment_sbom.json"
installed="$run_root/work/install/Linux/FPrimeNativeSbomExperiment_sbom.json"
if [[ $status -ne 0 ]]; then
    echo "native experiment failed with status $status; see $run_root/logs/execution.log" >&2
    exit "$status"
fi
if [[ ! -s "$sbom" || ! -s "$installed" ]]; then
    echo "native experiment returned zero without both expected SBOM files" >&2
    exit 74
fi

cp --preserve=timestamps "$sbom" "$run_root/native-original.spdx.json"
(
    cd "$run_root"
    sha256sum native-original.spdx.json work/install/Linux/FPrimeNativeSbomExperiment_sbom.json >output-sha256.txt
    du -ab . | sort -n >disk-usage-bytes.txt
)
echo "completed $run_id"

