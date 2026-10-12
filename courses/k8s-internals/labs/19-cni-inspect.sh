#!/usr/bin/env bash
# Chapter 19 — inspect CNI bins/config and a Pod's routes.
set -euo pipefail

if ! command -v docker >/dev/null 2>&1 || ! command -v kubectl >/dev/null 2>&1; then
  echo "docker + kubectl required (kind recommended)"
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

echo "== CNI binaries on $NODE =="
docker exec "$NODE" ls -la /opt/cni/bin 2>/dev/null || echo "no /opt/cni/bin"

echo
echo "== CNI configs =="
docker exec "$NODE" sh -c 'ls -la /etc/cni/net.d 2>/dev/null; echo; for f in /etc/cni/net.d/*; do echo "--- $f"; cat "$f" 2>/dev/null; echo; done' | head -120

echo
echo "== host links (veth/bridge hints) =="
docker exec "$NODE" ip -br link | head -30

echo
echo "== Pod route lab =="
kubectl delete pod cni-lab --ignore-not-found >/dev/null 2>&1 || true
kubectl run cni-lab --image=busybox:1.36 --restart=Never -- sleep 3600
kubectl wait --for=condition=Ready pod/cni-lab --timeout=120s
kubectl exec cni-lab -- ip -br addr
kubectl exec cni-lab -- ip route
kubectl get pod cni-lab -o wide
kubectl delete pod cni-lab

echo "Done."
