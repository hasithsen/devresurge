ROADMAP = {
    "slug": "devops-interview",
    "title": "DevOps interview sprint",
    "tagline": "Four weeks to interview-ready: SRE craft, Kubernetes, CI/CD at scale, and infra system design.",
    "description": (
        "A rigorous 30-day DevOps and SRE interview sprint for **top-tier product companies** — "
        "the bar used at hyperscale teams where reliability, velocity, and judgment matter more "
        "than tool trivia. Covers Linux, networking, release engineering, Kubernetes, IaC, "
        "observability, incidents, infra system design, and behavioral loops. Pair with a "
        "**regional elective** when you need visa sponsorship guidance."
    ),
    "domain": "devops",
    "level": "intermediate",
    "icon": "⚙",
    "order": 45,
    "track": "interview",
    "related_roadmap_slugs": (
        "sponsor-employers-sweden",
        "sponsor-employers-australia",
        "sponsor-employers-usa",
        "devsecops-interview",
        "relocation-sweden",
        "relocation-australia",
        "relocation-new-zealand",
        "relocation-usa",
        "relocation-uk",
    ),
    "audience": (
        "Platform, DevOps, and SRE candidates targeting senior product-company loops who want "
        "a daily plan instead of scattered tutorials."
    ),
    "outcomes": (
        "Execute a four-week schedule aligned to hyperscale interview loops",
        "Whiteboard CI/CD, Kubernetes, and infra system design with trade-offs",
        "Pass behavioral and on-call scenarios with SRE-grade clarity",
    ),
    "related_quiz_slugs": (
        "linux-shell",
        "git-collaboration",
        "containers-docker",
        "cicd-devops",
        "observability-basics",
        "networking-fundamentals",
        "security-basics",
        "system-design-basics",
        "python-fundamentals",
    ),
    "lessons": [
        {
            "slug": "30-day-battle-plan",
            "title": "Week 0: Your 30-day battle plan",
            "summary": "Hyperscale interview loops, daily schedule, and what bar-raisers actually score.",
            "minutes": 14,
            "outcomes": ("Block your calendar for four focused weeks",),
            "body": """
## How this questline works

**This map** — universal DevOps/SRE technical prep at the bar used by top product companies.

**Regional elective (optional)** — visa routes, local employers, relocation admin:

- [🇸🇪 Sweden](/learn/relocation-sweden/) · [🇦🇺 Australia](/learn/relocation-australia/)
- [🇳🇿 New Zealand](/learn/relocation-new-zealand/) · [🇺🇸 USA](/learn/relocation-usa/) · [🇬🇧 UK](/learn/relocation-uk/)

Add one elective in parallel if sponsorship is part of your search.

### Enterprise & migration sponsors (Volvo, IFS, peers)

If you target **visa-sponsored industrial or enterprise SaaS** roles, add the regional migration sponsor path:

- [🇸🇪 Sweden — Volvo, IFS & industrial](/learn/sponsor-employers-sweden/)
- [🇦🇺 Australia — IFS, banks & product](/learn/sponsor-employers-australia/)
- [🇺🇸 USA — IFS, enterprise & Tier-1](/learn/sponsor-employers-usa/)

Pair with the matching [regional relocation elective](/learn/relocation-sweden/) for visa mechanics.

## What hyperscale loops test

Top-tier DevOps/SRE interviews reward **depth + judgment**, not certification trivia:

| Round type | What they probe |
|------------|-----------------|
| Screen | Linux debug, networking, ownership stories |
| Technical deep dive | CI/CD, K8s, IaC — think aloud under pressure |
| Infra system design | Scale, failure modes, cost, operability |
| Coding / scripting | Python or Bash — practical automation, not trick puzzles |
| Behavioral | STAR + leadership signals: ownership, bias for action, customer impact |
| On-call simulation | Mitigate first, communicate, error-budget thinking |

## The bar (memorize)

- **Clarity** — trade-offs named before solutions
- **Safety** — prod, users, and data protected; rollbacks rehearsed
- **Evidence** — metrics, SLOs, postmortems — not heroics
- **Scale** — what breaks at 10× traffic or 500 teams
- **Toil reduction** — automate repeat work; measure lead time

## Time budget (~1 hour/day, 6 days/week)

| Week | Focus | Daily split |
|------|-------|-------------|
| 1 | Foundations + scripting | 25 min lesson + 35 min hands-on |
| 2 | Release engineering + K8s | 20 min lesson + 40 min pipeline/lab |
| 3 | Cloud + IaC + design | 20 min lesson + 40 min Terraform/design |
| 4 | SRE ops + mocks | 20 min lesson + 40 min timed drills |

**Week 4 days 6–7:** full mock loop (2 technical + 1 design + 1 behavioral).

## Pass gates — complete before scheduling loops

| Gate | Requirement |
|------|-------------|
| Quizzes | Pass [Linux](/quizzes/linux-shell/), [Git](/quizzes/git-collaboration/), [Docker](/quizzes/containers-docker/), [CI/CD](/quizzes/cicd-devops/), [Observability](/quizzes/observability-basics/), [Networking](/quizzes/networking-fundamentals/), [Security](/quizzes/security-basics/), [System design](/quizzes/system-design-basics/) |
| Portfolio | Public repo: app + hardened Dockerfile + CI YAML + K8s manifest + rollback README |
| Scripting | One Python tool (100–150 lines): parse logs/metrics or automate a deploy check |
| Mocks | 2 technical + 1 infra design + 1 behavioral — **recorded audio** |
| Stories | 5 STAR stories with **metrics** (latency, MTTR, deploy frequency, cost) |
| Cheat sheet | One handwritten page: pipeline, K8s, SLO, rollback, design spine |

## Hands-on labs (complete all three)

1. [KillerCoda — Kubernetes](https://killercoda.com/kubernetes/)
2. [AWS Skill Builder — EKS path](https://skillbuilder.aws/) or [Google Cloud — GKE](https://cloud.google.com/kubernetes-engine/docs)
3. End-to-end: GitHub Actions → build/test/scan → push image → deploy to kind/minikube/EKS

## Deepen after this sprint

- [DevOps & SRE craft](/learn/devops-sre/) · [System design](/learn/system-design/) · [DevSecOps sprint](/learn/devsecops-interview/)
""",
        },
        {
            "slug": "linux-shell-interview",
            "title": "Week 1, Day 1–2: Linux & shell at production scale",
            "summary": "Debug like on-call: processes, I/O, networking, and the commands you live-debug with.",
            "minutes": 16,
            "quiz_slug": "linux-shell",
            "outcomes": ("Debug a connectivity issue with shell tools",),
            "body": """
## Commands interviewers expect

```bash
# Processes & resources
ps aux | grep app
top / htop
free -h && df -h
vmstat 1 5
iostat -xz 1

# Networking
ss -tlnp
curl -v https://…
dig +short api.example.com
traceroute host
tcpdump -i any port 443 -c 20   # when permitted

# Logs & signals
journalctl -u myservice -f
tail -F /var/log/app.log | grep ERROR
kill -USR1 <pid>                # stack dump / reload patterns

# Files & permissions
find /var/log -name "*.log" -mtime -1
lsof -p <pid>
ulimit -a
```

## Hyperscale debug prompts

**"Latency p99 doubled after deploy."**

1. Confirm scope — one region/AZ or global?
2. Golden signals: traffic, errors, latency, saturation (USE/RED)
3. Correlation with deploy, config flag, or dependency
4. `ss`, connection counts, thread pools, GC pauses
5. Rollback decision vs fix-forward using error budget

**"Pod can't reach database."**

DNS → routing → firewall/NetworkPolicy → credentials/TLS → pool exhaustion.

## Scripting bar (many top-tier loops include this)

Write **Python or Bash** (10–30 lines) without IDE hand-holding:

- Parse JSON logs; aggregate error counts by service
- Health-check script exit non-zero on SLO breach
- `set -euo pipefail` in Bash; type hints welcome in Python

Pass [Python fundamentals](/quizzes/python-fundamentals/) if scripting feels rusty.

## Production mindset

No `rm -rf` heroics. Snapshot, mitigate user impact, then root-cause. Show **change discipline**
that survives audit and on-call handoffs.
""",
        },
        {
            "slug": "git-collaboration-interview",
            "title": "Week 1, Day 3: Git & release discipline at scale",
            "summary": "Trunk-based flow, monorepo awareness, and PR hygiene that hyperscale teams expect.",
            "minutes": 14,
            "quiz_slug": "git-collaboration",
            "outcomes": ("Describe your PR and review process in 60 seconds",),
            "body": """
## Branching strategy interviewers want

- **Trunk-based development** — main always releasable
- Short-lived branches (< 2 days) or direct to main with flags
- Feature flags decouple **deploy** from **release**
- Protected main: required reviews, green CI, no force-push

## At scale (what to mention)

- **Monorepo** trade-offs: atomic changes vs CI fan-out; Bazel/Build systems cache
- **Polyrepo**: independent release cadence; shared pipeline templates
- Code owners and blast-radius review for infra dirs

## PR quality checklist

1. Problem, metric, and rollback plan
2. Test evidence (unit, integration, load if relevant)
3. Observability: new metrics/logs/alerts?
4. Feature flag or progressive rollout path

## Git commands worth knowing

```bash
git bisect start
git cherry-pick <sha>
git rebase -i HEAD~3
git reflog
```

## Behavioral STAR

Messy branches or broken main → introduced protected main, smaller PRs, CI gates →
fewer rollbacks, faster lead time (cite **DORA** metrics if you have them).
""",
        },
        {
            "slug": "networking-http-ops",
            "title": "Week 1, Day 4–5: Networking & HTTP for platform engineers",
            "summary": "DNS, TLS, L4/L7 load balancing, and the path a request takes at scale.",
            "minutes": 15,
            "quiz_slug": "networking-fundamentals",
            "outcomes": ("Trace a request from client to pod",),
            "body": """
## The request path (draw this in every design round)

```
Client → DNS → CDN/edge → WAF → L7 LB → Ingress/service mesh → Pod
```

Know TLS termination (edge vs sidecar), connection pooling, and keep-alive pitfalls.

## Core concepts

- **DNS**: A/AAAA, CNAME, TTL, geo routing, health-checked records
- **TCP/TLS**: handshake cost, SNI, cert rotation, mTLS between services
- **HTTP**: methods, status codes, HTTP/2 multiplexing, timeouts at each hop
- **Load balancing**: L4 vs L7, consistent hashing, health checks vs readiness

## Cloud patterns (pick one stack deeply; compare others)

| Layer | AWS | GCP | Azure |
|-------|-----|-----|-------|
| L7 LB | ALB | Cloud Load Balancing | App Gateway |
| Ingress | ALB + Ingress Controller | GCE Ingress / Gateway | App Gateway |
| Private access | VPC endpoints | Private Service Connect | Private Link |
| Firewall | SG + NACL | VPC firewall | NSG |

## Debug script (say aloud)

1. `curl -v` from client and from in-cluster debug pod
2. Compare internal vs external DNS
3. Verify LB target health matches app `/ready`
4. Check recent deploy, flag, or autoscale event
5. Trace slow span in APM if latency not network-bound

## Design question

*"Serve HTTPS globally with <50ms added latency for static assets and secure origin for API."*

CDN cache, TLS at edge, origin shield, WAF, rate limits, DDoS protection, zero-trust
service-to-service auth if they push further.
""",
        },
        {
            "slug": "week1-checkpoint",
            "title": "Week 1 checkpoint: foundations + scripting drill",
            "summary": "Linux, Git, networking, and a timed scripting exercise.",
            "minutes": 14,
            "outcomes": ("Complete the week-1 troubleshooting and scripting scenarios",),
            "body": """
## Week 1 recap

Explain in 2 minutes each:

- Golden-signal debug path for latency regression
- Trunk-based flow and why flags beat long branches
- Client → pod request path with TLS and probes

## Timed drill A — Troubleshooting (45 min)

**Scenario**: After deploy, `/health` returns 502 from the load balancer but
`curl localhost` inside the pod succeeds.

Work through: readiness vs liveness, port mismatch, target group health check,
Ingress/backend config drift, recent canary weights.

## Timed drill B — Scripting (30 min)

Write Python or Bash: given a log file of HTTP status lines, print error rate
(5xx) per minute and exit 1 if any minute exceeds 5%.

This mirrors lightweight coding rounds — clarity and tests beat cleverness.

## Self-score

| Topic | 2-min explain? | Hands-on? |
|-------|----------------|-----------|
| Linux / on-call debug | ☐ | ☐ |
| Git / release flow | ☐ | ☐ |
| Request path | ☐ | ☐ |
| Scripting drill | ☐ | ☐ |

Redo weak areas before Week 2.
""",
        },
        {
            "slug": "cicd-design-interview",
            "title": "Week 2, Day 1: CI/CD & release engineering at scale",
            "summary": "Pipeline stages, DORA metrics, progressive delivery, and safe rollouts.",
            "minutes": 16,
            "quiz_slug": "cicd-devops",
            "outcomes": ("Whiteboard an 8-stage pipeline from memory",),
            "body": """
## The pipeline bar-raisers expect

```
Commit → Lint/Test → Build artifact → Scan → Deploy staging
       → Integration tests → Deploy prod (progressive) → Smoke + SLO watch
```

## Non-negotiable principles

1. **Build once, promote everywhere** — immutable artifact tagged with git SHA
2. **Fail fast** — unit/contract tests before slow suites; target PR feedback < 10 min
3. **Progressive delivery** — canary, blue/green, or rolling with automated rollback
4. **Audit trail** — who promoted what artifact, when, with which pipeline run ID
5. **Toil metrics** — track deployment frequency, lead time, change fail rate, MTTR

## Quality gates (ordered by cost)

Lint → unit → SAST/SCA → build → container scan → IaC scan → integration → staging soak → prod

Manual approval only where risk warrants — not for every typo.

## Rollout strategies

| Strategy | When | Risk control |
|----------|------|--------------|
| Rolling | Default stateless | maxUnavailable, readiness gates |
| Canary | User-facing APIs | metric comparison + auto rollback |
| Blue/green | Strict rollback SLA | double capacity cost |
| Feature flags | Decouple release | flag hygiene and cleanup |

## Sample answer

*"Bad deploy reached 100% of users — how do you prevent recurrence?"*

Canary on error rate and p99 vs baseline; auto-rollback on SLO burn; same artifact
through staging integration; feature flags for risky logic; postmortem with
automation action item (not "more careful").
""",
        },
        {
            "slug": "cicd-release-engineering",
            "title": "Week 2, Day 2–3: Release engineering — GitHub Actions & GitOps",
            "summary": "YAML pipelines, environments, OIDC, and GitOps patterns used at scale.",
            "minutes": 16,
            "outcomes": ("Sketch a multi-stage YAML pipeline with progressive prod deploy",),
            "body": """
## Why release engineering matters

Hyperscale teams ship **hundreds to thousands of times per day** across many services.
Interviewers want pipeline **design**, not click-ops nostalgia.

## GitHub Actions patterns

```yaml
on:
  pull_request:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: make test

  build-and-push:
    if: github.ref == 'refs/heads/main'
    needs: test
    permissions:
      id-token: write
      contents: read
    steps:
      - uses: aws-actions/configure-aws-credentials@v4  # OIDC, no long-lived keys
      - run: docker build -t $REGISTRY/app:${{ github.sha }} .
      - run: docker push $REGISTRY/app:${{ github.sha }}

  deploy-prod:
    needs: build-and-push
    environment: production
    steps:
      - run: ./deploy-canary.sh ${{ github.sha }}
```

## Topics to master

- **OIDC federation** to cloud — no static cloud keys in CI
- **Reusable workflows / templates** — DRY for 200 microservices
- **GitOps** (Argo CD / Flux): Git as desired state; drift detection; rollback = revert commit
- **Artifact promotion** vs rebuild per environment
- **Hermetic builds** awareness (reproducible, cached)

## Spinnaker / internal systems

You may not have used them — show you understand **orchestrated progressive delivery**
across clusters and regions.

## Hands-on goal

Pipeline: PR tests → main builds immutable image → scans → deploy staging →
manual or automated canary to prod with rollback documented in README.

## Pitfall question

*"Pipeline green locally, red in CI."*

Env vars, architecture mismatch, flaky tests, missing service containers, Docker
layer cache hiding bugs, insufficient permissions on OIDC role.
""",
        },
        {
            "slug": "docker-production-interview",
            "title": "Week 2, Day 4: Docker & container hardening",
            "summary": "Multi-stage builds, least privilege, and runtime security interview answers.",
            "minutes": 15,
            "quiz_slug": "containers-docker",
            "outcomes": ("Defend a production Dockerfile line by line",),
            "body": """
## Production Dockerfile checklist

```dockerfile
FROM python:3.12-slim AS build
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

FROM python:3.12-slim
RUN groupadd -r app && useradd -r -g app app
WORKDIR /app
COPY --from=build /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=build /app /app
USER app
EXPOSE 8080
HEALTHCHECK CMD curl -f http://localhost:8080/health || exit 1
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]
```

Explain: multi-stage, non-root, minimal base, healthcheck, exec form CMD.

## Security talking points

- Pin base image by **digest**
- No secrets in layers; runtime injection only
- Read-only root FS; drop capabilities; seccomp/AppArmor awareness
- Scan in CI (Trivy, Grype); block critical CVEs on prod path
- Distroless or slim bases — justify attack surface vs debuggability

## Runtime interview questions

- **Liveness vs readiness** — restart vs remove from load balancing
- **Requests/limits** — prevent noisy neighbor; OOMKill behavior
- **Graceful shutdown** — `preStop` + `terminationGracePeriodSeconds`

## Debug scenario

*"CrashLoopBackOff after config change."*

`kubectl logs --previous`, events, missing secret key, probe killing during slow start,
wrong entrypoint, OOMKilled.
""",
        },
        {
            "slug": "kubernetes-production-essentials",
            "title": "Week 2, Day 5: Kubernetes production essentials",
            "summary": "Workloads, scheduling, networking, and rollouts at scale.",
            "minutes": 16,
            "outcomes": ("Explain rolling deploy, rollback, and failure containment in Kubernetes",),
            "body": """
## Core objects (whiteboard map)

| Object | Purpose |
|--------|---------|
| Deployment / StatefulSet | Workload lifecycle |
| Service | Stable cluster IP / LB |
| Ingress / Gateway API | HTTP routing |
| ConfigMap / Secret | Config vs sensitive data |
| HPA / VPA | Autoscaling |
| PDB | Availability during disruptions |
| NetworkPolicy | East-west segmentation |

## Production depth (beyond tutorials)

- **Scheduling**: requests/limits, affinity/anti-affinity, taints/tolerations, topology spread
- **Probes**: startup vs readiness; avoid killing during warm-up
- **Rollouts**: maxSurge/maxUnavailable; `kubectl rollout undo`; Helm revision rollback
- **Identity**: IRSA (AWS) / Workload Identity (GCP) — no static cloud creds in pods
- **Service mesh** (awareness): mTLS, retries, circuit breaking — when worth the complexity

## kubectl toolkit

```bash
kubectl get pods -n app -w
kubectl describe pod <name>
kubectl logs <pod> --previous
kubectl rollout status deploy/app
kubectl rollout undo deploy/app
kubectl top pods
kubectl auth can-i create deployment --as=system:serviceaccount:app:deployer
```

## Design question

*"Zero-downtime deploy for stateful API with DB migration."*

Expand/contract migrations, readiness gates, `preStop` draining, PDB, backward-compatible
schema, rollback plan if migration irreversible.
""",
        },
        {
            "slug": "week2-checkpoint",
            "title": "Week 2 checkpoint: ship a portfolio pipeline",
            "summary": "CI/CD, containers, and Kubernetes in one demo-ready artifact.",
            "minutes": 12,
            "outcomes": ("Ship a containerized app through a YAML pipeline to Kubernetes",),
            "body": """
## Week 2 recap — no notes

- 8-stage pipeline with scans and progressive prod
- OIDC or scoped credentials — no long-lived secrets in YAML
- Hardened Dockerfile defended line-by-line
- K8s rollout, rollback, probes, resource limits

## Portfolio project (weekend — non-negotiable)

Public Git repo interviewers can skim in 5 minutes:

1. Small API or worker with tests
2. CI: test → build → scan → push image (SHA tag)
3. CD: deploy to kind/minikube/EKS/GKE
4. README: architecture diagram, SLO sketch, **rollback steps**, link to sample run

This separates "listed Kubernetes" from **proven** release engineering.

## Mock narrative (record 3 min)

*"Walk from git push to users on new version."*

Webhook → CI stages → immutable artifact → manifest update (GitOps or deploy job) →
rolling/canary → health checks → metrics watch → rollback trigger.

## Gate to Week 3

| Skill | Demo-ready? |
|-------|-------------|
| YAML pipeline | ☐ |
| Dockerfile review | ☐ |
| kubectl rollback | ☐ |

Need 3/3 before infra design week.
""",
        },
        {
            "slug": "terraform-iac-interview",
            "title": "Week 3, Day 1–2: Terraform & infrastructure as code",
            "summary": "State, modules, blast radius, and IaC interview scenarios.",
            "minutes": 16,
            "outcomes": ("Explain Terraform state risks and team workflows",),
            "body": """
## Fundamentals interviewers probe

- Providers, resources, data sources, variables/outputs
- **Modules** — versioning, composition, blast-radius boundaries
- **Remote state** + locking (S3+DynamoDB, GCS, Terraform Cloud)
- **Plan → peer review → apply** — same rigor as app code
- **Policy as code** — Sentinel, OPA/Conftest on plans

## Repository layout

```
modules/
  eks-cluster/
  vpc/
envs/
  staging/main.tf
  prod/main.tf
```

## Critical topics

| Topic | Interview angle |
|-------|-----------------|
| State locking | Prevent corrupt concurrent applies |
| Drift | Portal edits vs code; detect in CI |
| Import | Adopt existing resources safely |
| `-target` | Emergency only; document blast radius |
| `prevent_destroy` | Prod data resources |

## Multi-account / multi-project

Landing zone awareness: shared networking, centralized logging, least-privilege roles
for CI apply vs human break-glass.

## Scenario

*"Apply failed halfway."*

State records successes; re-plan declaratively; fix dependency graph; never edit
state by hand without runbook; communicate in shared channel before retry.
""",
        },
        {
            "slug": "cloud-platform-engineering",
            "title": "Week 3, Day 3: Cloud platform engineering at scale",
            "summary": "IAM, compute, networking, and the services you map in design rounds.",
            "minutes": 15,
            "outcomes": ("Map a multi-team platform to cloud services with IAM boundaries",),
            "body": """
## Platform building blocks (AWS example — translate to GCP/Azure)

| Need | Service |
|------|---------|
| Kubernetes | EKS / GKE / AKS |
| Container registry | ECR / Artifact Registry / ACR |
| Secrets | Secrets Manager / Secret Manager / Key Vault |
| Observability | CloudWatch + AMP / Cloud Monitoring / Azure Monitor |
| Identity | IAM roles, IRSA, SCPs / org policies |
| Networking | VPC, subnets, NAT, endpoints, transit hub |
| Object storage | S3 / GCS / Blob |

## IAM interview answer

- Least privilege for humans and **workloads**
- Separate accounts/projects per environment
- CI role scoped to deploy targets only; no admin for apps
- Break-glass audited; prefer short-lived credentials

## Infra system design spine (45 min)

Clarify: teams served, SLO, regions, compliance, scale.

1. Requirements & constraints
2. High-level diagram (edge → compute → data)
3. Deep dive: CI/CD, K8s tenancy, observability, security
4. Failure modes: AZ loss, bad deploy, dependency outage
5. Cost and operability trade-offs
6. Rollout plan for the platform itself

## Whiteboard prompt

*"Shared Kubernetes platform for 50 teams, 200 services, 99.9% control plane SLO."*

Namespace isolation, quotas, admission policies, central logging/metrics, GitOps,
multi-AZ node pools, upgrade strategy, on-call rotation, self-service with guardrails.

Pass [System design basics](/quizzes/system-design-basics/) before mock design rounds.
""",
        },
        {
            "slug": "config-secrets-twelve-factor",
            "title": "Week 3, Day 4: Config, secrets & twelve-factor at scale",
            "summary": "Environment parity, rotation, and dynamic config without secret sprawl.",
            "minutes": 14,
            "outcomes": ("Separate config from secrets in platform design",),
            "body": """
## Twelve-factor highlights

3. **Config** in environment, not repo
5. **Build, release, run** — strict separation
10. **Dev/prod parity** — containers + IaC reduce gap
11. **Logs** as streams to centralized aggregation
12. **Admin tasks** as one-off jobs, not SSH snowflakes

## Secrets ladder

1. ❌ Git, Dockerfile, or plain CI vars for prod
2. ⚠️ Encrypted CI secrets (rotation pain)
3. ✅ Cloud secret manager + workload identity
4. ✅ CSI driver / sidecar injection; automatic rotation; audit access

## Config patterns

- Helm values / Kustomize overlays per env
- Feature flags service (LaunchDarkly, internal) for release decoupling
- Gradual config rollout with observability on error budget

## Rotation STAR story

Dual-key support, staged rollout, monitor auth errors, revoke old credential after
burn-in — zero user-facing downtime.

## Trap question

*"Where do DB connection strings live?"*

Injected at deploy from secret manager; scoped IAM; different secret per env;
never in build artifacts.
""",
        },
        {
            "slug": "devsecops-supply-chain",
            "title": "Week 3, Day 5: Supply chain security & shift-left",
            "summary": "Pipeline security gates, SBOM, signing — expected at top-tier bar.",
            "minutes": 15,
            "quiz_slug": "security-basics",
            "outcomes": ("List proportional security gates for high-velocity teams",),
            "body": """
## Shift-left pipeline (proportional, not theatrical)

1. Secret scanning on every commit
2. SAST on PR
3. SCA / dependency CVE gates with SLA by severity
4. Container image scan before registry push
5. IaC scan on Terraform PRs
6. Admission control verifying signatures at deploy

## Supply chain (table stakes)

- **SBOM** stored with artifacts
- **Sign** images (Cosign/Sigstore); verify in cluster admission
- Pin dependencies; review transitive updates
- Minimal images; rebuild on base CVE patches

## Velocity vs security debate

*"Security wants manual review every deploy."*

Automate in CI, fail on criticals, risk-tier services, measure escape rate and
lead time — tune policy with data. Pair with [DevSecOps sprint](/learn/devsecops-interview/) for depth.

## Compliance awareness (without drowning)

SOC2-style control mapping, change management evidence, segregation of duties —
show you respect audit without blocking every fix.
""",
        },
        {
            "slug": "week3-checkpoint",
            "title": "Week 3 checkpoint: infra design mock",
            "summary": "Terraform, cloud platform, and a timed infra system design.",
            "minutes": 14,
            "outcomes": ("Complete a 35-minute infra system design aloud",),
            "body": """
## Week 3 recap

Without notes:

- Terraform state, modules, drift, team workflow
- Multi-team platform on Kubernetes with IAM boundaries
- Config vs secrets separation
- Supply-chain gates that don't kill velocity

## Hands-on lab

1. `terraform plan/apply` minimal VPC + cluster or registry module
2. Inject secret via cloud manager + workload identity
3. Introduce drift manually → observe in plan
4. PR description with blast radius and rollback

## Infra system design mock (35 min, timer on)

*"Design a global CI/CD platform for 500 engineers building containerized services."*

Cover: monorepo vs polyrepo, shared templates, artifact storage, regional runners,
secrets, audit, rate limits, multi-region failover for **control plane**, SLO for
pipeline availability, cost controls.

Use clarify → estimate → diagram → deep dives → failure modes → trade-offs.

## Gate to Week 4

If design rounds still feel fuzzy, repeat one mock before interview week.
""",
        },
        {
            "slug": "observability-slo-interview",
            "title": "Week 4, Day 1: Observability & SLO interview mastery",
            "summary": "Metrics, logs, traces, SLIs/SLOs, and alerting that respects sleep.",
            "minutes": 16,
            "quiz_slug": "observability-basics",
            "outcomes": ("Define SLIs, SLOs, and error budgets for a service you know",),
            "body": """
## Three pillars (+ profiling)

- **Metrics**: Prometheus/Datadog/CloudWatch — RED for services, USE for resources
- **Logs**: structured JSON, trace/ request IDs
- **Traces**: OpenTelemetry across microservices
- **Profiling**: continuous profiling for tail latency (bonus depth)

## SLI → SLO → error budget

- **SLI**: availability, latency p99, freshness, correctness
- **SLO**: target over window (e.g. 99.95% / 30d)
- **Error budget**: product + engineering negotiate release risk

## Alerting philosophy (Google SRE book)

Alert on **user-visible symptoms** and **multi-window burn rates** — not every CPU blip.

- Fast burn → page
- Slow burn → ticket
- Every page must be actionable

## Post-deploy watch

Compare canary to baseline: error rate, p99, saturation, business KPIs.
Automated rollback tied to SLO burn.

## Scenario

*"Error rate doubled after deploy — first 10 minutes."*

Confirm scope → rollback if user impact → compare golden signals → check flags/deps →
trace failing spans → comms cadence → postmortem if sustained.
""",
        },
        {
            "slug": "incident-response-interview",
            "title": "Week 4, Day 2: Incident command & blameless learning",
            "summary": "Mitigate first, communicate clearly, improve systems — on-call bar.",
            "minutes": 14,
            "outcomes": ("Tell a blameless postmortem story with tracked action items",),
            "body": """
## Incident lifecycle

1. **Detect** — alert or customer signal
2. **Triage** — severity, incident commander
3. **Mitigate** — rollback, scale, disable feature — **users first**
4. **Communicate** — status page cadence; no silent heroes
5. **Resolve** — fix forward or revert
6. **Learn** — blameless postmortem; actions tracked to completion

## Roles at scale

- **Incident commander** coordinates; doesn't solo-debug
- **Communications** — internal + external stakeholders
- **SMEs** per subsystem with clear handoffs

## Postmortem template

- Customer impact (duration, scope)
- Timeline (UTC facts)
- Contributing factors (plural)
- What worked / didn't
- Action items: owner, due date, verified done

## STAR story

Real incident → mitigate with metric impact → systemic fix (automation, alert,
runbook, architecture) — not "we'll try harder."

## Culture signal

Top companies hire engineers who **surface** problems early and improve systems —
not those who hide outages or blame individuals.
""",
        },
        {
            "slug": "behavioral-devops-interview",
            "title": "Week 4, Day 3: Behavioral & leadership principles",
            "summary": "STAR stories mapped to ownership, customer impact, and technical disagreement.",
            "minutes": 15,
            "outcomes": ("Prepare five STAR stories for hyperscale behavioral loops",),
            "body": """
## Five stories to write (STAR, <3 min each)

1. **Automated toil** — metric: hours saved, fewer incidents, faster lead time
2. **Technical disagreement** — data-driven; customer/SLO centered resolution
3. **Production incident** — mitigate-first; postmortem outcome
4. **Mentorship / uplift** — docs, pairing, platform self-service
5. **Ambiguous deadline** — prioritized ruthlessly; communicated trade-offs

## Common prompts

- Tell me about improving reliability or deployment frequency.
- Describe a time you were wrong in production.
- How do you prioritize when multiple SEVs compete?
- How do you partner with dev teams who resist process?
- Why platform / SRE / DevOps — why now?

## Leadership signals (generic bar-raiser language)

- **Ownership** end-to-end, including toil you created
- **Customer / user impact** in every story
- **Dive deep** on technical details when asked
- **Bias for action** with reversible decisions
- **Learn and be curious** — what you changed after failure

## Questions to ask them

- On-call load and rotation fairness?
- Error budget policy in practice?
- Biggest platform bottleneck today?
- Success in first 90 days?

Strong questions signal seniority.
""",
        },
        {
            "slug": "technical-mock-drills",
            "title": "Week 4, Day 4: Full-loop mock drills",
            "summary": "Pipeline design, K8s debug, infra design, scripting — timed.",
            "minutes": 18,
            "outcomes": ("Complete four timed mock scenarios out loud",),
            "body": """
## Drill 1 — Pipeline design (20 min)

*"CI/CD for 20 microservices, 200 commits/day, strict prod SLO."*

Shared templates, caching, fan-in/fan-out, artifact promotion, progressive prod,
automatic rollback, audit trail, DORA metrics dashboard.

## Drill 2 — Kubernetes debug (15 min)

*"Intermittent 503 after HPA scale-out."*

Events, endpoints, readiness during warm-up, CPU throttling, DB pool limits,
connection storms, PDB blocking rollout.

## Drill 3 — Infra system design (35 min)

*"Multi-region active-active API with RPO/RTO targets."*

DNS, data replication lag, conflict handling, observability per region, failover
drills, cost of double write, runbooks.

## Drill 4 — Scripting (15 min)

Parse sample JSON access logs; output top 10 paths by 5xx count; discuss complexity
and how you'd productionize (tests, cron, alert hook).

## Drill 5 — Terraform (10 min)

State lock contention during incident deploy — coordination, lock break procedure,
never parallel applies on shared state.

## Practice rules

- Timer on; record audio
- Structure: clarify → approach → trade-offs → monitoring
- Re-take [CI/CD](/quizzes/cicd-devops/), [Observability](/quizzes/observability-basics/),
  [System design](/quizzes/system-design-basics/) until consistent passes
""",
        },
        {
            "slug": "final-checklist-interview-day",
            "title": "Week 4, Day 5: Final checklist & interview day",
            "summary": "Cheat sheet, calm execution, and loop strategy.",
            "minutes": 14,
            "outcomes": ("Enter the loop with a one-page cheat sheet and five polished stories",),
            "body": """
## One-page cheat sheet (handwrite)

**Pipeline**: build once → scan → stage → progressive prod → rollback

**K8s**: probes, rollout/undo, requests/limits, PDB, identity

**Cloud**: IAM least privilege, multi-AZ, private networking

**Terraform**: remote state, plan review, modules, drift

**SRE**: SLI/SLO, error budget, burn alerts, mitigate first

**Design**: clarify → estimate → diagram → deep dive → failures → trade-offs

## Night before

- Sleep 7+ hours — structured thinking beats cramming
- Re-read five STAR stories once
- Test camera, mic, quiet space, backup network

## During each round

1. Clarify constraints before solving
2. Think aloud — silence reads as stuck
3. Name trade-offs and monitoring
4. Admit gaps honestly with learning path

## After each round

Journal questions, weak spots, one improvement. Update cheat sheet — loops are iterative.

## Ready signal

- Whiteboard full pipeline in 5 minutes
- 35-minute infra design without freezing
- Portfolio repo you'd proudly share in screen share
- Quizzes passed consistently on DevResurge

> Top companies hire **reliable engineers who automate wisely** — not on-call heroes
> who hide problems. Thirty days of reps built that signal. Execute.
""",
        },
        {
            "slug": "sprint-complete-resources",
            "title": "Complete reference guide & pass checklist",
            "summary": "Quizzes, labs, design prompts, and final audit before you schedule loops.",
            "minutes": 18,
            "outcomes": ("Verify every pass gate before booking interviews",),
            "body": """
## Sprint complete when

- [ ] All lessons cleared on DevResurge
- [ ] Eight core quizzes passed (Linux, Git, Docker, CI/CD, Observability, Networking, Security, System design)
- [ ] Portfolio repo public: CI YAML, Dockerfile, K8s manifest, rollback README
- [ ] Python/Bash scripting artifact in portfolio or gist
- [ ] Five STAR stories rehearsed under 3 minutes
- [ ] Four mocks timed (pipeline, K8s, design, behavioral)
- [ ] One-page cheat sheet handwritten

## Technical self-audit (target 4+ on all)

| Topic | Whiteboard? | Hands-on? |
|-------|-------------|-----------|
| Linux on-call debug | | |
| Git / release at scale | | |
| HTTP/DNS/TLS path | | |
| CI/CD + DORA | | |
| Dockerfile hardening | | |
| K8s rollout + rollback | | |
| Terraform workflow | | |
| Infra system design | | |
| SLI/SLO + alerting | | |
| Incident + postmortem | | |
| Supply chain gates | | |

## Optional certifications (signal boost, not required)

- [CKA — Kubernetes Administrator](https://www.cncf.io/certification/cka/)
- [AWS DevOps Engineer Professional](https://aws.amazon.com/certification/certified-devops-engineer-professional/)
- [Google Professional Cloud DevOps Engineer](https://cloud.google.com/certification/cloud-devops-engineer)

## Continue on DevResurge

[DevOps & SRE craft](/learn/devops-sre/) · [System design](/learn/system-design/) ·
[Distributed systems](/learn/distributed-systems/) · [DevSecOps sprint](/learn/devsecops-interview/)
""",
        },
    ],
}
