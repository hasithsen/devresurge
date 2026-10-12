#!/usr/bin/env bash
# Chapter 17 — inspect etcd health via kind control-plane certs.
set -euo pipefail

if ! command -v docker >/dev/null 2>&1; then
  echo "docker required for kind node exec"
  exit 1
fi

CLUSTER="${KIND_CLUSTER_NAME:-}"
if [[ -z "$CLUSTER" ]]; then
  CLUSTER="$(kind get clusters 2>/dev/null | head -n1 || true)"
fi
if [[ -z "$CLUSTER" ]]; then
  echo "No kind cluster. Create one: kind create cluster"
  exit 1
fi

NODE="${CLUSTER}-control-plane"
if ! docker inspect "$NODE" >/dev/null 2>&1; then
  echo "Node $NODE not found"
  exit 1
fi

echo "cluster=$CLUSTER node=$NODE"
echo
echo "== etcd endpoint status =="
docker exec "$NODE" bash -lc '
  ETCDCTL_API=3 etcdctl \
    --endpoints=https://127.0.0.1:2379 \
    --cacert=/etc/kubernetes/pki/etcd/ca.crt \
    --cert=/etc/kubernetes/pki/etcd/server.crt \
    --key=/etc/kubernetes/pki/etcd/server.key \
    endpoint status -w table
'

echo
echo "== etcd endpoint health =="
docker exec "$NODE" bash -lc '
  ETCDCTL_API=3 etcdctl \
    --endpoints=https://127.0.0.1:2379 \
    --cacert=/etc/kubernetes/pki/etcd/ca.crt \
    --cert=/etc/kubernetes/pki/etcd/server.crt \
    --key=/etc/kubernetes/pki/etcd/server.key \
    endpoint health
'

echo
echo "== bump a revision via ConfigMap =="
if command -v kubectl >/dev/null 2>&1; then
  NAME="etcd-lab-$(date +%s)"
  kubectl create configmap "$NAME" --from-literal=k=v
  kubectl delete configmap "$NAME"
  echo "Created and deleted ConfigMap $NAME (revision moved)."
else
  echo "kubectl not found — skipped object create"
fi

echo "Done."
