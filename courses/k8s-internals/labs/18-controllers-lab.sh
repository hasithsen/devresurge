#!/usr/bin/env bash
# Chapter 18 — ownerReferences + finalizer sticky delete.
set -euo pipefail

if ! command -v kubectl >/dev/null 2>&1; then
  echo "kubectl required"
  exit 1
fi

echo "== Deployment ownership chain =="
kubectl delete deploy ctrl-lab --ignore-not-found >/dev/null 2>&1 || true
kubectl create deploy ctrl-lab --image=nginx:1.25-alpine --replicas=2
kubectl rollout status deploy/ctrl-lab --timeout=120s

echo
echo "-- ReplicaSet ownerReferences --"
kubectl get rs -l app=ctrl-lab -o jsonpath='{range .items[*]}{.metadata.name}{" -> "}{.metadata.ownerReferences[0].kind}/{.metadata.ownerReferences[0].name}{"\n"}{end}'

echo
echo "-- Pod ownerReferences --"
kubectl get pods -l app=ctrl-lab -o jsonpath='{range .items[*]}{.metadata.name}{" -> "}{.metadata.ownerReferences[0].kind}/{.metadata.ownerReferences[0].name}{"\n"}{end}'

echo
echo "== Finalizer sticky ConfigMap =="
kubectl delete cm sticky --ignore-not-found >/dev/null 2>&1 || true
kubectl apply -f - <<'EOF'
apiVersion: v1
kind: ConfigMap
metadata:
  name: sticky
  finalizers:
    - course.k8s.internals/wait
data:
  x: "1"
EOF

kubectl delete cm sticky --wait=false
echo "After delete --wait=false (should still exist with deletionTimestamp):"
kubectl get cm sticky -o custom-columns=NAME:.metadata.name,DELETING:.metadata.deletionTimestamp,FINALIZERS:.metadata.finalizers

kubectl patch cm sticky --type=json -p='[{"op":"remove","path":"/metadata/finalizers"}]'
sleep 1
kubectl get cm sticky 2>&1 || echo "sticky gone (expected)"

kubectl delete deploy ctrl-lab
echo "Done."
