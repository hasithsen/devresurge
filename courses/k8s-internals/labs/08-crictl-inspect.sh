#!/usr/bin/env bash
# Chapter 06/08 — peek at CRI through crictl inside a kind node.
# Requires: kind cluster, docker, crictl inside the node image (kind ships it).
set -euo pipefail

if ! command -v kind >/dev/null 2>&1; then
  echo "kind not found. Install kind or run crictl manually on a node."
  exit 1
fi

if ! command -v docker >/dev/null 2>&1; then
  echo "docker not found (needed to exec into kind nodes)."
  exit 1
fi

CLUSTER="${KIND_CLUSTER_NAME:-}"
if [[ -z "$CLUSTER" ]]; then
  # Prefer a cluster that already exists
  CLUSTER="$(kind get clusters 2>/dev/null | head -n1 || true)"
fi

if [[ -z "$CLUSTER" ]]; then
  echo "No kind cluster found. Create one: kind create cluster"
  exit 1
fi

NODE="${CLUSTER}-control-plane"
if ! docker inspect "$NODE" >/dev/null 2>&1; then
  echo "Node container $NODE not found. Set KIND_CLUSTER_NAME or create a cluster."
  exit 1
fi

echo "Using kind cluster=$CLUSTER node=$NODE"
echo
echo "== crictl version =="
docker exec "$NODE" crictl version || docker exec "$NODE" crictl --runtime-endpoint unix:///run/containerd/containerd.sock version

echo
echo "== images (head) =="
docker exec "$NODE" crictl images | head

echo
echo "== pods =="
docker exec "$NODE" crictl pods | head

echo
echo "== containers =="
docker exec "$NODE" crictl ps -a | head

echo
echo "Done. This is the same layer kubelet talks to via CRI."
