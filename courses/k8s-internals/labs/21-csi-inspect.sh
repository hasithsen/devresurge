#!/usr/bin/env bash
# Chapter 21 — CSIDriver/CSINode/VolumeAttachment + optional PVC lab.
set -euo pipefail

if ! command -v kubectl >/dev/null 2>&1; then
  echo "kubectl required"
  exit 1
fi

echo "== CSI drivers =="
kubectl get csidrivers 2>/dev/null || echo "no CSIDriver resources"

echo
echo "== CSINodes =="
kubectl get csinodes -o wide 2>/dev/null || true

echo
echo "== StorageClasses =="
kubectl get storageclass

echo
echo "== VolumeAttachments =="
kubectl get volumeattachment 2>/dev/null || true

SC="$(kubectl get storageclass -o jsonpath='{.items[?(@.metadata.annotations.storageclass\.kubernetes\.io/is-default-class=="true")].metadata.name}' 2>/dev/null || true)"
if [[ -z "$SC" ]]; then
  SC="$(kubectl get storageclass -o jsonpath='{.items[0].metadata.name}' 2>/dev/null || true)"
fi

if [[ -z "$SC" ]]; then
  echo "No StorageClass — skipping PVC mount lab"
  exit 0
fi

echo
echo "Using StorageClass=$SC for PVC lab"
kubectl delete pod csi-lab-pod --ignore-not-found >/dev/null 2>&1 || true
kubectl delete pvc csi-lab-pvc --ignore-not-found >/dev/null 2>&1 || true

kubectl apply -f - <<EOF
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: csi-lab-pvc
spec:
  accessModes: ["ReadWriteOnce"]
  storageClassName: "$SC"
  resources:
    requests:
      storage: 100Mi
---
apiVersion: v1
kind: Pod
metadata:
  name: csi-lab-pod
spec:
  containers:
    - name: app
      image: busybox:1.36
      command: ["sh", "-c", "echo hi > /data/x; sleep 3600"]
      volumeMounts:
        - name: data
          mountPath: /data
  volumes:
    - name: data
      persistentVolumeClaim:
        claimName: csi-lab-pvc
EOF

if kubectl wait --for=condition=Ready pod/csi-lab-pod --timeout=120s; then
  kubectl exec csi-lab-pod -- cat /data/x
  kubectl get pvc csi-lab-pvc
  kubectl get volumeattachment
else
  echo "Pod not Ready — describe for attach/mount clues:"
  kubectl describe pod csi-lab-pod | tail -50
fi

kubectl delete pod csi-lab-pod --wait=false >/dev/null 2>&1 || true
kubectl delete pvc csi-lab-pvc --wait=false >/dev/null 2>&1 || true
echo "Done (cleanup issued)."
