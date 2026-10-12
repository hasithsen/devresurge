# Kubernetes Internals — From Linux Up (Book Length)

A book-length course that treats Kubernetes as **orchestration of Linux constructs**, not magic YAML.

You will build a mental model from processes → namespaces → cgroups → containers → pods → kubelet → control plane → networking → storage → security → debugging, then go **monograph-deep** on etcd, controllers/informers, CNI, eBPF dataplanes, and CSI. Every chapter starts ELI5, then gets precise.

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

1. Read the **core arc** (01–16) in order
2. Then the **deep dives** (17–21) — each assumes its parent chapter
3. Run the **Lab** in each chapter (or the matching script under [`labs/`](labs/))
4. After each arc, take the DevResurge quiz and earn the badge

```mermaid
flowchart LR
  foundation[Ch 01-04 Linux] --> runtime[Ch 05-07 Containers]
  runtime --> node[Ch 08-11 Node and control plane]
  node --> dataplane[Ch 12-14 Net and storage]
  dataplane --> ops[Ch 15-16 Security and debug]
  ops --> deep[Ch 17-21 Deep dives]
```

## Syllabus — core arc

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

## Syllabus — deep dives (book depth)

| # | Chapter | Parent | Core idea |
|---|---------|--------|-----------|
| [17](17-etcd-deep.md) | etcd deep dive | 09 | Raft, WAL, compaction, backups |
| [18](18-controllers-deep.md) | Controllers deep dive | 10 | Informers, workqueues, finalizers |
| [19](19-cni-deep.md) | CNI deep dive | 12 | Plugin contract, veth, IPAM |
| [20](20-ebpf-dataplane.md) | eBPF dataplane | 12/19 | Maps, hooks, kube-proxy replacement |
| [21](21-csi-deep.md) | CSI deep dive | 14 | Provision → attach → stage → publish |

## Quiz track (DevResurge)

Pass at 80% to earn badges.

| Arc | Chapters | Quiz | Badge |
|-----|----------|------|-------|
| Linux foundations | 01–04 | [`/quizzes/k8s-linux-foundations/`](/quizzes/k8s-linux-foundations/) | K8s Linux Roots |
| Containers & runtime | 05–07 | [`/quizzes/k8s-containers-runtime/`](/quizzes/k8s-containers-runtime/) | K8s Runtime |
| Node & control plane | 08–11 | [`/quizzes/k8s-node-control-plane/`](/quizzes/k8s-node-control-plane/) | K8s Control Plane |
| Networking & storage | 12–14 | [`/quizzes/k8s-networking-storage/`](/quizzes/k8s-networking-storage/) | K8s Data Plane |
| Security & ops | 15–16 | [`/quizzes/k8s-security-ops/`](/quizzes/k8s-security-ops/) | K8s Secure Ops |
| Deep dives | 17–21 | [`/quizzes/k8s-deep-dives/`](/quizzes/k8s-deep-dives/) | K8s Deep Dive |

**Milestones**

- Pass the five core K8s quizzes → **Cluster Internals**
- Pass those five **plus** deep dives → **Cluster Scholar**

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
| [`17-etcd-raft-lab.sh`](labs/17-etcd-raft-lab.sh) | 17 |
| [`18-controllers-lab.sh`](labs/18-controllers-lab.sh) | 18 |
| [`19-cni-inspect.sh`](labs/19-cni-inspect.sh) | 19 |
| [`20-ebpf-observe.sh`](labs/20-ebpf-observe.sh) | 20 |
| [`21-csi-inspect.sh`](labs/21-csi-inspect.sh) | 21 |

## Pedagogy contract

Every chapter follows the same shape:

1. **ELI5 hook** — one analogy
2. **Mental model** — the precise idea in plain words
3. **What Linux / the component does** — kernel / userspace reality
4. **How Kubernetes uses it** — the bridge
5. **Lab** — feel it with your hands
6. **Gotchas** — the lies that bite in production

## What this course is not

- Not a YAML cookbook or CKAD dump
- Not vendor-specific (EKS/GKE/AKS appear only as callouts)
- Not a substitute for reading upstream design proposals — it *is* book-depth on the five deep-dive topics above

Ready? Start with [01 — Linux processes](01-linux-processes.md).
