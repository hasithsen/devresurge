#!/usr/bin/env bash
# Chapter 20 — observe iptables kube-proxy vs BPF presence on a kind node.
set -euo pipefail

if ! command -v docker >/dev/null 2>&1; then
  echo "docker required"
  exit 1
fi

CLUSTER="${KIND_CLUSTER_NAME:-}"
if [[ -z "$CLUSTER" ]]; then
  CLUSTER="$(kind get clusters 2>/dev/null | head -n1 || true)"
fi
if [[ -z "$CLUSTER" ]]; then
  echo "No kind cluster found"
  exit 1
fi
NODE="${CLUSTER}-control-plane"

echo "== kube-proxy / iptables footprints on $NODE =="
docker exec "$NODE" bash -lc 'iptables-save 2>/dev/null | grep -E "KUBE-|CALI-|CILIUM" | head -50' \
  || echo "(iptables-save unavailable)"

echo
echo "== bpftool (may be absent on kind image) =="
docker exec "$NODE" bash -lc 'command -v bpftool && bpftool prog show | head -20 || echo "bpftool not installed in node"'

echo
echo "== /sys/fs/bpf =="
docker exec "$NODE" bash -lc 'ls /sys/fs/bpf 2>/dev/null | head || echo "no bpffs listings"'

echo
echo "Note: stock kind uses iptables/IPVS-style kube-proxy, not Cilium."
echo "Install Cilium on a disposable cluster to see eBPF Service/policy maps."
echo "Done."
