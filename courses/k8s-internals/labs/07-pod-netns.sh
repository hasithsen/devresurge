#!/usr/bin/env bash
# Chapter 07 — two containers in one Pod share localhost (netns).
# Requires: kubectl context pointed at a cluster (kind recommended).
set -euo pipefail

if ! command -v kubectl >/dev/null 2>&1; then
  echo "kubectl not found; install kubectl + kind to run this lab."
  exit 1
fi

kubectl delete pod roommates --ignore-not-found >/dev/null 2>&1 || true

kubectl apply -f - <<'EOF'
apiVersion: v1
kind: Pod
metadata:
  name: roommates
spec:
  containers:
    - name: server
      image: nginx:1.25-alpine
      ports:
        - containerPort: 80
    - name: client
      image: busybox:1.36
      command: ["sh", "-c", "sleep 3600"]
EOF

echo "Waiting for Ready..."
kubectl wait --for=condition=Ready pod/roommates --timeout=120s

echo
echo "== Client hits server via 127.0.0.1 (shared netns) =="
kubectl exec roommates -c client -- wget -qO- http://127.0.0.1/ | head -c 200
echo

echo
echo "== Pod IP (one IP for the apartment) =="
kubectl get pod roommates -o wide

kubectl delete pod roommates
echo "Done."
