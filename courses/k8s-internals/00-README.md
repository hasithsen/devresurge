# Kubernetes Internals — From Linux Up

A full-arc course that treats Kubernetes as **orchestration of Linux constructs**, not magic YAML.

You will build a mental model from processes → namespaces → cgroups → containers → pods → kubelet → control plane → networking → storage → security → debugging. Every chapter starts ELI5, then gets precise.

## Who this is for

- Engineers who use `kubectl` and want to know *why* things break
- Platform / SRE folks who debug nodes, not just manifests
- Anyone tired of “containers are lightweight VMs”

## Prerequisites

- Comfortable in a Linux shell (`ps`, `ls`, pipes)
- A Linux VM, WSL2, or cloud VM with root (or passwordless sudo)
- Optional but strongly recommended: [kind](https://kind.sigs.k8s.io/) + `kubectl` + `crictl`

You do **not** need prior Kubernetes experience. You *do* need curiosity about what the kernel is doing.

## How to take the course

1. Read chapters **in order** — later chapters assume earlier mental models
2. Run the **Lab** in each chapter (or the matching script under [`labs/`](labs/))
3. After each arc, take the DevResurge quiz and earn the badge

```mermaid
flowchart LR
  foundation[Ch 01-04 Linux] --> runtime[Ch 05-07 Containers]
  runtime --> node[Ch 08-11 Node and control plane]
  node --> dataplane[Ch 12-14 Net and storage]
  dataplane --> ops[Ch 15-16 Security and debug]
```

## Syllabus

| # | Chapter | Core idea |
|---|---------|-----------|
| [01](01-linux-processes.md) | Linux processes | Processes are the real unit of work |
| [02](02-namespaces.md) | Namespaces | Walls for what you can *see* |
| [03](03-cgroups.md) | cgroups | Budgets for what you can *use* |
| [04](04-security-primitives.md) | Security primitives | Capabilities, seccomp, LSM |
| [05](05-images-oci.md) | OCI images | Suitcases of files + config |
| [06](06-containerd-cri.md) | containerd & CRI | Who actually starts containers |
| [07](07-pods.md) | Pods | Shared fate, shared network namespace |
| [08](08-kubelet.md) | kubelet | The node babysitter |
| [09](09-api-etcd.md) | API server & etcd | Desired state store |
| [10](10-controllers.md) | Controllers | Reconcile forever |
| [11](11-scheduler.md) | Scheduler | Who goes where |
| [12](12-networking.md) | Networking | Pod IP → Service → world |
| [13](13-ingress-gateway.md) | Ingress & Gateway | L7 front door |
| [14](14-storage.md) | Storage | Disks that outlive pods |
| [15](15-security-k8s.md) | Cluster security | SA, RBAC, admission, NetworkPolicy |
| [16](16-troubleshoot.md) | Troubleshoot | Debug like an owner |

## Quiz track (DevResurge)

Pass at 80% to earn badges. Complete all five for the **Cluster Internals** milestone.

| Arc | Chapters | Quiz | Badge |
|-----|----------|------|-------|
| Linux foundations | 01–04 | [`/quizzes/k8s-linux-foundations/`](/quizzes/k8s-linux-foundations/) | K8s Linux Roots |
| Containers & runtime | 05–07 | [`/quizzes/k8s-containers-runtime/`](/quizzes/k8s-containers-runtime/) | K8s Runtime |
| Node & control plane | 08–11 | [`/quizzes/k8s-node-control-plane/`](/quizzes/k8s-node-control-plane/) | K8s Control Plane |
| Networking & storage | 12–14 | [`/quizzes/k8s-networking-storage/`](/quizzes/k8s-networking-storage/) | K8s Data Plane |
| Security & ops | 15–16 | [`/quizzes/k8s-security-ops/`](/quizzes/k8s-security-ops/) | K8s Secure Ops |

Seed quizzes locally with:

```bash
uv run python manage.py seed_quizzes
```

## Labs

Scripts live in [`labs/`](labs/). They are written for Linux (or WSL2). Run with:

```bash
chmod +x courses/k8s-internals/labs/*.sh
sudo ./courses/k8s-internals/labs/02-namespaces-demo.sh
```

| Script | Chapter |
|--------|---------|
| [`02-namespaces-demo.sh`](labs/02-namespaces-demo.sh) | 02 |
| [`03-cgroups-demo.sh`](labs/03-cgroups-demo.sh) | 03 |
| [`07-pod-netns.sh`](labs/07-pod-netns.sh) | 07 |
| [`08-crictl-inspect.sh`](labs/08-crictl-inspect.sh) | 08 |

## Pedagogy contract

Every chapter follows the same shape:

1. **ELI5 hook** — one analogy
2. **Mental model** — the precise idea in plain words
3. **What Linux does** — kernel / userspace reality
4. **How Kubernetes uses it** — the bridge
5. **Lab** — feel it with your hands
6. **Gotchas** — the lies that bite in production

## What this course is not

- Not a YAML cookbook or CKAD dump
- Not vendor-specific (EKS/GKE/AKS appear only as callouts)
- Not a monograph on etcd or eBPF — those get chapter depth, not book depth

Ready? Start with [01 — Linux processes](01-linux-processes.md).
