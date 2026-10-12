#!/usr/bin/env bash
# Chapter 02 — feel Linux namespaces (UTS + net).
# Requires: Linux (or WSL2), sudo.
set -euo pipefail

echo "== Host UTS =="
echo "hostname=$(hostname)"
echo "uts ns=$(readlink /proc/self/ns/uts)"

echo
echo "== unshare --uts: hostname inside isolated UTS =="
sudo unshare --uts bash -c 'hostname course-island; echo "hostname=$(hostname)"; echo "uts ns=$(readlink /proc/self/ns/uts)"'

echo
echo "== Host hostname unchanged =="
echo "hostname=$(hostname)"

echo
echo "== unshare --net: interfaces inside a fresh netns =="
sudo unshare --net bash -c 'ip -br link || ifconfig -a || true'

echo
echo "Done. Different UTS inode + empty-ish netns = walls, not VMs."
