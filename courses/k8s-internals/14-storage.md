# 14 — Storage: disks that outlive pods

## ELI5 hook

A container’s writable layer is a **whiteboard on the apartment wall** — wiped when you move out. A **volume** is a **filing cabinet** you can roll into the apartment. **PersistentVolumes** are filing cabinets in the building basement that survive lease changes. **CSI** is the moving company that attaches the right cabinet to the right room.

## Mental model

| Object | Meaning |
|--------|---------|
| **Volume** (in a Pod) | Something mounted into a container path |
| **emptyDir** | Temporary cabinet — lives as long as the Pod on that node |
| **PersistentVolume (PV)** | Piece of storage in the cluster inventory |
| **PersistentVolumeClaim (PVC)** | “I need 10Gi ReadWriteOnce” request |
| **StorageClass** | “Provision me a disk of type X dynamically” |
| **CSI driver** | Plugin that creates/attaches/mounts real storage |

```mermaid
flowchart LR
  pod[Pod] --> pvc[PVC]
  pvc --> pv[PV]
  pv --> csi[CSI driver]
  csi --> disk[Cloud disk / NFS / local]
```

## What Linux does

Mounting is still **mount(2)** into the container’s mount namespace:

1. **Attach** (controller) — disk appears on the node (block device / NFS export)
2. **Mount** (node) — filesystem mounted on host, bind-mounted into the pod

kubelet coordinates; CSI **sidecars** (`external-attacher`, `node-driver-registrar`, …) do the vendor work.

### Access modes

| Mode | Meaning |
|------|---------|
| ReadWriteOnce (RWO) | One node read-write |
| ReadOnlyMany (ROX) | Many nodes read-only |
| ReadWriteMany (RWX) | Many nodes read-write (NFS-like) |
| ReadWriteOncePod | Single Pod RWO (newer) |

RWO volumes **pin scheduling** to the node where attached.

## How Kubernetes uses it

Dynamic provisioning flow:

1. Pod references a PVC
2. PVC asks StorageClass
3. CSI provisioner creates PV + backing disk
4. Scheduler places Pod where attach is possible
5. CSI attaches + kubelet mounts → container sees files

```yaml
volumes:
  - name: data
    persistentVolumeClaim:
      claimName: data-pvc
```

Other common volumes: `configMap`, `secret`, `projected`, `hostPath` (sharp), `csi` ephemeral.

## Lab

```bash
# emptyDir — data dies with Pod
kubectl apply -f - <<'EOF'
apiVersion: v1
kind: Pod
metadata:
  name: scratch
spec:
  containers:
    - name: app
      image: busybox:1.36
      command: ["sh", "-c", "echo hello > /data/f; sleep 3600"]
      volumeMounts:
        - name: data
          mountPath: /data
  volumes:
    - name: data
      emptyDir: {}
EOF

kubectl wait --for=condition=Ready pod/scratch --timeout=60s
kubectl exec scratch -- cat /data/f
kubectl delete pod scratch

# PVC — only works if a default StorageClass exists (kind usually has one)
kubectl get storageclass
kubectl apply -f - <<'EOF'
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: demo-pvc
spec:
  accessModes: ["ReadWriteOnce"]
  resources:
    requests:
      storage: 100Mi
EOF
kubectl get pvc demo-pvc
kubectl delete pvc demo-pvc
```

## Gotchas

- **Deleting PVC with retain policy** — PV may keep data; know `reclaimPolicy`.
- **RWO + multi-AZ** — Attach failures if Pod reschedules to another zone without multi-AZ disks.
- **hostPath** — Ties to node filesystem; security + portability hazard.
- **Filesystem vs block** — Some apps need raw block (`volumeMode: Block`).
- **Capacity ≠ inode / performance** — Small PVC can still be slow depending on class.

## Checkpoint

Volumes mount Linux filesystems into mount namespaces. PVCs/PVs/CSI make storage **portable across Pod lifetimes**.

Next: [15 — Cluster security](15-security-k8s.md).

---

**Quiz:** [`/quizzes/k8s-networking-storage/`](/quizzes/k8s-networking-storage/)
