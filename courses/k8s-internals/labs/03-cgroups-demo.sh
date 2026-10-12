#!/usr/bin/env bash
# Chapter 03 — observe cgroup membership and (optionally) a memory limit.
# Requires: Linux. Docker optional for the limit demo.
set -euo pipefail

echo "== /proc/self/cgroup =="
cat /proc/self/cgroup

echo
echo "== cgroupfs mounts =="
mount | grep -E 'cgroup|cgroup2' || true

echo
if [[ -d /sys/fs/cgroup ]]; then
  echo "== /sys/fs/cgroup (top) =="
  ls /sys/fs/cgroup | head
fi

if command -v docker >/dev/null 2>&1; then
  echo
  echo "== Docker memory limit probe (64m) =="
  docker run --rm -m 64m alpine sh -c '
    if [ -f /sys/fs/cgroup/memory.max ]; then
      echo "cgroup v2 memory.max=$(cat /sys/fs/cgroup/memory.max)"
    elif [ -f /sys/fs/cgroup/memory/memory.limit_in_bytes ]; then
      echo "cgroup v1 limit=$(cat /sys/fs/cgroup/memory/memory.limit_in_bytes)"
    else
      echo "Could not find memory controller files in this image layout"
      ls /sys/fs/cgroup || true
    fi
  '
else
  echo
  echo "(docker not found — skipped memory limit container probe)"
fi

echo
echo "Done. Budgets live in cgroup files; namespaces do not set them."
