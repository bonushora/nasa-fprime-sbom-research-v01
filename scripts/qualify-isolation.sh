#!/usr/bin/env bash
set -euo pipefail

repo_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)
source_root="$repo_root/.artifacts/v0.2/source"
result_root="$repo_root/evidence/v0.2/environment/isolation"

if [[ -e "$result_root" ]]; then
    echo "refusing to overwrite isolation evidence: $result_root" >&2
    exit 73
fi
mkdir -p "$result_root/work"

set +e
timeout --signal=TERM --kill-after=5s 60s \
prlimit --as=536870912 --cpu=30 --nproc=4096 --nofile=256 --fsize=1048576 -- \
bwrap \
    --unshare-user --unshare-pid --unshare-ipc --unshare-uts --unshare-cgroup-try --unshare-net \
    --die-with-parent --new-session --clearenv \
    --ro-bind /usr /usr --ro-bind /lib /lib --ro-bind /lib64 /lib64 \
    --symlink usr/bin /bin --symlink usr/sbin /sbin \
    --ro-bind "$source_root" /input \
    --bind "$result_root/work" /work \
    --proc /proc --dev /dev --tmpfs /tmp \
    --setenv HOME /tmp/home --setenv PATH /usr/bin --setenv LANG C.UTF-8 --setenv LC_ALL C.UTF-8 --setenv TZ UTC \
    --chdir /work \
    /usr/bin/sh -eu -c '
        mkdir -p /tmp/home
        echo "== mount =="
        grep " /input " /proc/self/mountinfo
        echo "== source write denial =="
        if touch /input/.bh-write-probe 2>/tmp/write-error; then
            echo "FAIL: source write unexpectedly succeeded"
            exit 1
        fi
        cat /tmp/write-error
        test ! -e /input/.bh-write-probe
        echo "PASS: source is effectively read-only"
        echo "== output write =="
        printf qualified > /work/write-probe.txt
        test "$(cat /work/write-probe.txt)" = qualified
        echo "PASS: dedicated output is writable"
        echo "== network namespace =="
        ip link
        python3 - <<"PY"
import socket
s = socket.socket()
s.settimeout(1)
try:
    s.connect(("1.1.1.1", 443))
except OSError as error:
    print(f"PASS: external network denied: {type(error).__name__}: {error}")
else:
    raise SystemExit("FAIL: external network connection succeeded")
finally:
    s.close()
PY
        echo "== credential surfaces =="
        test ! -e /home && echo "PASS: /home absent"
        test ! -e /root && echo "PASS: /root absent"
        test ! -e /etc/passwd && echo "PASS: /etc not mounted"
        env | sort
        echo "== visible root =="
        find / -mindepth 1 -maxdepth 1 -printf "%f\n" | sort
    ' >"$result_root/qualification.log" 2>&1
status=$?
set -e
printf '%s\n' "$status" >"$result_root/exit-code.txt"
if [[ $status -ne 0 ]]; then
    echo "isolation qualification failed: $status" >&2
    exit "$status"
fi
sha256sum "$result_root/qualification.log" "$result_root/work/write-probe.txt" >"$result_root/sha256.txt"
echo "isolation qualified"

