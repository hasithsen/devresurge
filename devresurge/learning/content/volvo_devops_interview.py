ROADMAP = {
    "slug": "devops-interview-30-day",
    "title": "30-day DevOps interview sprint",
    "tagline": "Four weeks to interview-ready: enterprise CI/CD, Azure, Kubernetes, and production craft.",
    "description": (
        "A structured one-month plan for DevOps engineer interviews at large "
        "enterprises — including automotive and industrial teams like Volvo Group. "
        "Each week builds on the last: foundations, delivery pipelines, cloud "
        "infrastructure, then production operations and interview drills."
    ),
    "domain": "devops",
    "level": "intermediate",
    "icon": "🚛",
    "order": 45,
    "audience": (
        "Engineers preparing for enterprise DevOps interviews who want a daily "
        "plan instead of random tutorials."
    ),
    "outcomes": (
        "Follow a week-by-week study and practice schedule",
        "Answer technical and behavioral DevOps interview questions with confidence",
        "Demonstrate Azure, CI/CD, containers, and SRE fundamentals",
    ),
    "related_quiz_slugs": (
        "linux-shell",
        "git-collaboration",
        "containers-docker",
        "cicd-devops",
        "observability-basics",
        "networking-fundamentals",
    ),
    "lessons": [
        {
            "slug": "30-day-battle-plan",
            "title": "Week 0: Your 30-day battle plan",
            "summary": "How to use this sprint, time budget, and what interviewers actually score.",
            "minutes": 12,
            "outcomes": ("Block your calendar for four focused weeks",),
            "body": """
## What this sprint covers

Enterprise DevOps interviews — including roles at Volvo Group and similar
industrial companies — test **breadth and judgment**, not trivia:

- Linux, Git, networking fundamentals
- CI/CD design and pipeline troubleshooting
- Azure cloud, containers, Kubernetes (often AKS)
- Infrastructure as code (Terraform is common)
- Observability, incidents, and blameless culture
- Behavioral stories about collaboration, safety, and delivery

## Time budget (≈1 hour/day)

| Week | Focus | Daily split |
|------|-------|-------------|
| 1 | Foundations | 30 min lesson + 30 min hands-on |
| 2 | Build & ship | 20 min lesson + 40 min pipeline/lab |
| 3 | Cloud & infra | 20 min lesson + 40 min Terraform/Azure |
| 4 | Ops & interview | 20 min lesson + 40 min mocks + review |

## How to use DevResurge

1. Complete lessons in order — each unlocks context for the next.
2. Take linked quizzes after each topic cluster.
3. Write short notes after every boss fight; reuse them in mock interviews.
4. Pair this sprint with the **DevOps & SRE** roadmap for deeper dives.

## Interview scoring rubric (memorize this)

Interviewers grade on:

- **Clarity** — can you explain trade-offs without hand-waving?
- **Safety** — do you protect main, prod, and users?
- **Evidence** — do you cite metrics, logs, and past incidents?
- **Collaboration** — do you mention teams, reviews, and postmortems?

> You don't need to know every Azure service name. You need to show you can
> **design, debug, and deliver** under real constraints.
""",
        },
        {
            "slug": "linux-shell-interview",
            "title": "Week 1, Day 1–2: Linux & shell for interviews",
            "summary": "Processes, permissions, logs, and the commands you'll whiteboard or live-debug.",
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

# Networking
ss -tlnp          # what's listening?
curl -v https://… # full HTTP/TLS trace
dig +short api.example.com
traceroute host

# Logs
journalctl -u myservice -f
tail -F /var/log/app.log | grep ERROR

# Files & permissions
ls -la /path
find /var/log -name "*.log" -mtime -1
chmod / chown (know when UID mapping matters in containers)
```

## Common interview prompts

**"A pod can't reach a database."** Walk through:

1. DNS resolves? (`dig`, `/etc/resolv.conf`)
2. Port open and listening on DB host? (`ss`, `telnet`/`nc`)
3. Firewall / NSG / NetworkPolicy blocking?
4. Credentials / TLS / certificate expiry?
5. Connection pool exhausted on app side?

**"Disk is full on a build agent."** Check `df -h`, find large dirs with
`du -sh /*`, rotate logs, clean Docker images (`docker system prune`).

## Scripting bar

Be comfortable writing a 10-line Bash script: loop over files, grep a pattern,
exit non-zero on failure (`set -euo pipefail`). Python for parsing JSON (`jq`
alternative) is a plus.

## Enterprise context

Industrial teams run long-lived Linux VMs, build agents, and container hosts.
Show you respect **change control**: no `rm -rf` heroics; snapshot, mitigate,
then fix.
""",
        },
        {
            "slug": "git-collaboration-interview",
            "title": "Week 1, Day 3: Git & collaboration at scale",
            "summary": "Trunk-based flow, PR hygiene, and stories that show team maturity.",
            "minutes": 14,
            "quiz_slug": "git-collaboration",
            "outcomes": ("Describe your PR and review process in 60 seconds",),
            "body": """
## Branching strategy interviewers want to hear

- **Trunk-based development** or short-lived feature branches
- Main/master always releasable
- Feature flags > long-lived branches
- Protected branches with required reviews and CI green

## PR quality checklist

Every PR should answer:

1. What problem and for whom?
2. How tested? (unit, integration, manual)
3. Rollback plan?
4. Blast radius if this breaks prod?

## Git commands worth knowing

```bash
git rebase -i HEAD~3      # clean history before merge
git cherry-pick <sha>     # hotfix to release branch
git bisect start          # find the breaking commit
git stash / git reflog    # recovery, not panic
```

## Behavioral angle

Prepare a STAR story:

- **Situation**: messy branch strategy or broken main
- **Task**: improve flow without blocking the team
- **Action**: introduced protected main, CI gates, smaller PRs
- **Result**: fewer rollbacks, faster merges, measurable cycle time

## Red flags to avoid

- Force-pushing shared branches
- "I don't write commit messages"
- Merging without CI because "it's a small change"
""",
        },
        {
            "slug": "networking-http-ops",
            "title": "Week 1, Day 4–5: Networking & HTTP for operators",
            "summary": "DNS, TLS, load balancers, and the path a request takes in Azure.",
            "minutes": 15,
            "quiz_slug": "networking-fundamentals",
            "outcomes": ("Trace a request from client to pod",),
            "body": """
## The request path (draw this in interviews)

```
Client → DNS → CDN/WAF → Load Balancer → Ingress → Service → Pod
```

Know where TLS terminates (edge vs pod) and what breaks when certs expire.

## Core concepts

- **DNS**: A/AAAA, CNAME, TTL, private zones in Azure
- **TCP/TLS**: three-way handshake, SNI, certificate chain validation
- **HTTP**: methods, status codes, headers, keep-alive, HTTP/2
- **Load balancing**: L4 vs L7, health checks, session affinity

## Azure-specific (Volvo Group stack)

Volvo and many enterprises standardize on **Microsoft Azure**:

- Application Gateway / Front Door for L7
- Azure Load Balancer for L4
- Private Link for PaaS without public exposure
- Network Security Groups (NSGs) and Azure Firewall

## Debug script (say this out loud)

1. `curl -v` from inside the cluster (or `kubectl run` debug pod)
2. Compare internal vs external DNS
3. Check NSG rules and route tables
4. Verify backend health probe matches app health endpoint
5. Inspect Ingress/AGW backend pool status

## Interview question

*"Design how a microservice in AKS receives HTTPS traffic from the internet
without exposing pod IPs."*

Hit: Ingress controller, cert-manager, WAF, private cluster option, mTLS
between services if they ask about zero-trust.
""",
        },
        {
            "slug": "week1-checkpoint",
            "title": "Week 1 checkpoint: foundations lab",
            "summary": "Consolidate Linux, Git, and networking with a timed troubleshooting drill.",
            "minutes": 12,
            "outcomes": ("Complete the week-1 troubleshooting scenario",),
            "body": """
## Week 1 recap

You should now comfortably explain:

- How you debug "service A can't reach B"
- Your team's Git/PR workflow
- The path from browser to container

## Timed drill (45 minutes)

**Scenario**: After a deploy, `/health` returns 502 from the load balancer but
works when you `curl localhost` inside the pod.

Work through:

1. Readiness vs liveness probe configuration
2. Port mismatch (containerPort vs app listen port)
3. Backend pool health check path/port
4. Recent Ingress or AGW change in the last deploy

Write your answer as a numbered checklist — this is exactly how senior
interviewers want you to think.

## Self-score

| Topic | Can explain in 2 min? | Did hands-on practice? |
|-------|----------------------|------------------------|
| Linux debug | ☐ | ☐ |
| Git/PR flow | ☐ | ☐ |
| Request path | ☐ | ☐ |

If any box is empty, redo that lesson before Week 2.

## Bridge to Week 2

Next week you build the pipelines that deploy the apps you've been debugging.
Bring your Week 1 notes — CI/CD interviews always loop back to networking
and Git.
""",
        },
        {
            "slug": "cicd-design-interview",
            "title": "Week 2, Day 1: CI/CD design interview answers",
            "summary": "Pipeline stages, quality gates, artifacts, and safe rollouts.",
            "minutes": 16,
            "quiz_slug": "cicd-devops",
            "outcomes": ("Whiteboard an 8-stage pipeline from memory",),
            "body": """
## The pipeline every interviewer expects

```
Commit → Lint/Test → Build artifact → Scan → Deploy staging
       → Integration tests → Deploy prod (progressive) → Smoke + monitor
```

## Non-negotiable principles

1. **Build once, promote everywhere** — same Docker image / binary tag
2. **Fail fast** — unit tests before slow integration suites
3. **Immutable artifacts** — tag with git SHA, not `latest`
4. **Automated rollback** — on SLO burn or failed smoke tests
5. **Audit trail** — who deployed what, when, from which pipeline run

## Quality gates

- Static analysis / lint
- Unit + contract tests
- SAST / dependency scan (SCA)
- Container image scan
- IaC plan review (Terraform)
- Manual approval only for prod — not for every typo fix

## Rollout strategies (know trade-offs)

| Strategy | Pros | Cons |
|----------|------|------|
| Rolling | Simple | Mixed versions during deploy |
| Blue/green | Fast rollback | Double resources |
| Canary | Limits blast radius | Needs metrics + routing |
| Feature flags | Decouple deploy from release | Flag debt |

## Sample interview answer

*"How would you prevent a bad deploy from reaching all users?"*

> Canary 5% traffic, watch error rate and p99 latency for 15 minutes against
> SLO burn alerts. Auto-rollback if thresholds breach. Same artifact promoted
> through staging with integration tests. Feature flags for risky logic.
""",
        },
        {
            "slug": "azure-devops-github-actions",
            "title": "Week 2, Day 2–3: Azure DevOps & GitHub Actions",
            "summary": "YAML pipelines, environments, approvals, and secrets in enterprise setups.",
            "minutes": 16,
            "outcomes": ("Sketch a multi-stage YAML pipeline with environments",),
            "body": """
## Why this matters for Volvo Group roles

Large enterprises often use **Azure DevOps** (Repos, Pipelines, Boards) or
**GitHub Enterprise** with Actions. Expect YAML pipeline questions, not
click-ops.

## Azure DevOps concepts

- **Pipeline**: YAML or classic; triggers on branch/PR
- **Stages / jobs / steps**: parallelize tests, serialize deploys
- **Environments**: dev → staging → prod with approvals
- **Variable groups & Key Vault**: secrets never in YAML
- **Service connections**: scoped credentials to Azure subscriptions
- **Artifacts**: universal packages, container images to ACR

## GitHub Actions parallel

```yaml
# Pattern: build on PR, deploy on main with environment protection
on:
  push:
    branches: [main]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: docker build -t $REGISTRY/app:${{ github.sha }} .
  deploy:
    needs: build
    environment: production  # required reviewers
```

## Interview topics

- **Pipeline triggers**: PR validation vs main deploy
- **Secrets management**: Key Vault references, OIDC federation (no long-lived SP passwords)
- **Self-hosted agents** vs Microsoft-hosted (compliance, network to on-prem)
- **Template reuse**: YAML templates / reusable workflows

## Hands-on goal

Write a pipeline that: runs tests on PR, builds and pushes an image on merge,
deploys to staging automatically, and requires manual approval for production.

## Common pitfall question

*"A pipeline works on your machine but fails in CI."*

Check: env vars, service connections, agent OS differences, cached deps,
Docker daemon availability, and path assumptions.
""",
        },
        {
            "slug": "docker-production-interview",
            "title": "Week 2, Day 4: Docker & container security",
            "summary": "Dockerfiles, image scanning, and runtime hardening interview answers.",
            "minutes": 15,
            "quiz_slug": "containers-docker",
            "outcomes": ("Defend a production Dockerfile line by line",),
            "body": """
## Production Dockerfile checklist

```dockerfile
# Multi-stage: build vs runtime
FROM node:20-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci --omit=dev
COPY . .
RUN npm run build

FROM node:20-alpine
RUN addgroup -S app && adduser -S app -G app
WORKDIR /app
COPY --from=build /app/dist ./dist
USER app
EXPOSE 8080
HEALTHCHECK CMD curl -f http://localhost:8080/health || exit 1
CMD ["node", "dist/server.js"]
```

Explain every line in an interview.

## Security talking points

- Non-root user
- Minimal base image (Alpine/distroless)
- No secrets in layers — use runtime env / mounted secrets
- Pin base image by **digest**, not floating tags
- Scan images in CI (Trivy, Defender for Cloud)
- Read-only root filesystem where possible
- Drop capabilities; no `--privileged`

## Runtime interview questions

- **Liveness vs readiness**: liveness restarts; readiness removes from load balancer
- **Resource limits**: CPU/memory requests and limits prevent noisy neighbors
- **Logs**: stdout/stderr → centralized logging (App Insights, ELK)

## Debug scenario

*"Container exits immediately in AKS."*

Check: `kubectl logs`, `kubectl describe pod`, wrong CMD, missing env var,
crash on startup, OOMKilled, failed probe killing the pod too early.
""",
        },
        {
            "slug": "kubernetes-aks-essentials",
            "title": "Week 2, Day 5: Kubernetes & AKS essentials",
            "summary": "Pods, Deployments, Services, Ingress — what DevOps engineers must explain.",
            "minutes": 16,
            "outcomes": ("Explain a rolling deploy and rollback in Kubernetes",),
            "body": """
## Core objects (interview map)

| Object | Purpose |
|--------|---------|
| Pod | Smallest deploy unit; one or more containers |
| Deployment | Declarative rollouts, replicas, rollback |
| Service | Stable ClusterIP/LoadBalancer for pods |
| Ingress | HTTP routing into the cluster |
| ConfigMap / Secret | Config vs sensitive data |
| HPA | Autoscale on CPU/custom metrics |

## AKS-specific knowledge

- **Node pools**: system vs user, spot vs regular
- **Azure CNI** vs kubenet networking trade-offs
- **ACR integration**: pull images with managed identity
- **Azure Monitor / Container Insights**: metrics and logs
- **Pod Identity / Workload Identity**: access Azure resources without secrets

## kubectl toolkit

```bash
kubectl get pods -n app -w
kubectl describe pod <name>
kubectl logs <pod> --previous      # crashed container
kubectl rollout status deploy/app
kubectl rollout undo deploy/app    # rollback
kubectl exec -it <pod> -- sh       # debug shell
```

## Rolling update interview answer

Deployment updates create a new ReplicaSet. MaxUnavailable and MaxSurge control
speed vs capacity. Failed readiness checks stop the rollout (`kubectl rollout
status`). Rollback = `kubectl rollout undo` or deploy previous manifest from Git.

## Design question

*"How do you run zero-downtime deploys for a stateful API?"*

Readiness gates, preStop hook for draining connections, PDB (Pod Disruption
Budget), database migrations compatible with old and new code (expand/contract).
""",
        },
        {
            "slug": "week2-checkpoint",
            "title": "Week 2 checkpoint: build a mini pipeline",
            "summary": "Tie CI/CD, Docker, and K8s together in one portfolio artifact.",
            "minutes": 12,
            "outcomes": ("Ship a containerized app through a YAML pipeline",),
            "body": """
## Week 2 recap

You should whiteboard without notes:

- 8-stage CI/CD pipeline
- Azure DevOps or GitHub Actions environment promotion
- Production Dockerfile defenses
- Kubernetes rolling deploy + rollback

## Portfolio project (weekend)

Build a **mini delivery pipeline** you can demo in interviews:

1. Small API or static site in Git
2. CI: test + build Docker image → push to registry
3. CD: deploy to AKS or local kind/minikube
4. README with architecture diagram and rollback steps

This beats listing "Docker, K8s, Azure" on a CV without proof.

## Mock question (record yourself)

*"Walk me through what happens from git push to users hitting the new version."*

Target: 3-minute clear narrative touching Git webhook, pipeline stages, image
tag, manifest update, rolling deploy, health checks, monitoring.

## Self-score

| Skill | Demo-ready? |
|-------|-------------|
| YAML pipeline | ☐ |
| Dockerfile review | ☐ |
| kubectl rollback | ☐ |

Proceed to Week 3 only when at least two boxes are checked.
""",
        },
        {
            "slug": "terraform-iac-interview",
            "title": "Week 3, Day 1–2: Terraform & infrastructure as code",
            "summary": "State, modules, plan/apply workflow, and IaC interview scenarios.",
            "minutes": 16,
            "outcomes": ("Explain Terraform state risks and mitigation",),
            "body": """
## Terraform fundamentals interviewers probe

- **Providers**: AzureRM for Volvo-style Azure estates
- **Resources vs data sources**
- **Variables / outputs / locals**
- **Modules**: reuse, versioning, blast-radius boundaries
- **State**: remote backend (Azure Storage + locking), never commit state
- **Plan → review → apply**: same discipline as application code

## Sample structure

```
modules/
  aks-cluster/
  networking/
envs/
  dev/main.tf
  prod/main.tf
```

## Critical interview topics

**State locking**: prevents concurrent applies corrupting infrastructure.

**Drift**: manual portal changes vs code — detect with `terraform plan`.

**Import**: bring existing resources under management without recreate.

**Destroy risk**: use `prevent_destroy` lifecycle on prod databases.

## Azure examples to mention

- Resource groups as blast-radius boundaries
- VNet, subnets, NSGs before AKS
- Key Vault for secrets referenced by Terraform and apps
- RBAC: who can apply to prod subscription

## Scenario question

*"Terraform apply failed halfway — some resources created, some not."*

Answer: state file records what succeeded; re-run plan (Terraform is
declarative); fix dependency errors; never delete state manually; use
`-target` only as last resort with team awareness.
""",
        },
        {
            "slug": "azure-cloud-devops",
            "title": "Week 3, Day 3: Azure cloud for DevOps engineers",
            "summary": "Subscriptions, IAM, ACR, AKS, Key Vault — the services you'll name in interviews.",
            "minutes": 15,
            "outcomes": ("Map an app architecture to Azure services",),
            "body": """
## Azure building blocks for DevOps roles

| Need | Azure service |
|------|---------------|
| Container registry | Azure Container Registry (ACR) |
| Kubernetes | Azure Kubernetes Service (AKS) |
| Secrets | Key Vault |
| CI/CD | Azure DevOps Pipelines / GitHub Actions |
| Monitoring | Azure Monitor, Application Insights, Log Analytics |
| Identity | Entra ID (Azure AD), managed identities |
| Storage / DB | Blob, Azure SQL, Cosmos (know when not to pick each) |
| Networking | VNet, Private Link, Application Gateway, Front Door |

## IAM interview answer

Principle of **least privilege**:

- Pipeline service principal / managed identity scoped to subscription or RG
- Separate dev and prod subscriptions or RGs
- No owner role for apps; use custom roles
- Audit with Activity Log and Defender for Cloud

## Cost and governance (enterprise cares)

- Tags for cost allocation (team, environment, product)
- Policy (Azure Policy) to enforce regions, SKUs, encryption
- Landing zones for large orgs — mention awareness even if you haven't built one

## Architecture whiteboard

*"Host a microservices platform for 20 teams."*

Shared AKS cluster with namespace isolation, ACR per org or repo, central
logging, GitOps (Flux/Argo CD) for manifests, Key Vault per environment,
Hub-Spoke networking for on-prem connectivity (common in automotive/industrial).
""",
        },
        {
            "slug": "config-secrets-twelve-factor",
            "title": "Week 3, Day 4: Config, secrets & twelve-factor apps",
            "summary": "Environment parity, secret rotation, and config management at scale.",
            "minutes": 14,
            "outcomes": ("Separate config from secrets in your pipeline design",),
            "body": """
## Twelve-factor highlights for interviews

3. **Config** — store in environment, not code
4. **Backing services** — treat DB/cache as attached resources
5. **Build, release, run** — strict separation; same artifact across envs
10. **Dev/prod parity** — minimize gaps; containers help
11. **Logs** — event streams to aggregation
12. **Admin processes** — one-off jobs as containers, not SSH hacks

## Secrets management ladder

1. ❌ Secrets in Git or Dockerfile
2. ⚠️ CI variable groups (encrypted at rest)
3. ✅ Key Vault / HashiCorp Vault with rotation
4. ✅ Workload Identity — pods fetch secrets at runtime, no static creds

## Config patterns

- Helm values per environment
- Kustomize overlays (dev/staging/prod)
- Azure App Configuration for feature flags + dynamic config

## Rotation story (behavioral)

Prepare how you handled credential rotation without downtime: dual-key support,
staged rollout, monitor auth errors, revoke old key after burn-in.

## Interview trap

*"Where do connection strings live?"*

Not in repo. Injected at deploy from Key Vault reference or CSI driver mount;
different vault/RG per environment; audit access.
""",
        },
        {
            "slug": "devsecops-supply-chain",
            "title": "Week 3, Day 5: DevSecOps & supply chain",
            "summary": "Shift-left security, compliance, and automotive-grade delivery culture.",
            "minutes": 15,
            "quiz_slug": "security-basics",
            "outcomes": ("List five security gates in a CI/CD pipeline",),
            "body": """
## Shift-left in the pipeline

1. **Secret scanning** (gitleaks) on every commit
2. **SAST** — static code analysis
3. **SCA** — dependency vulnerabilities (Dependabot, Snyk)
4. **Container scan** before push to registry
5. **IaC scan** (Checkov, tfsec) on Terraform PRs
6. **DAST** in staging for critical apps

## Supply chain (hot topic)

- SBOM generation for container images
- Sign images (Cosign, Notation) and verify at deploy (admission controller)
- Pin dependencies; review transitive updates
- Minimal base images reduce CVE surface

## Automotive / industrial angle

Volvo Group and peers operate under **strict quality and safety culture**:

- Traceability: who changed what, when, with approval
- Separation of duties: dev cannot deploy prod alone
- Compliance frameworks (ISO 27001, ASPICE awareness — you don't need to be
  certified, but show respect for process)
- Change windows and rollback readiness for critical systems

## Interview question

*"Security wants to gate every deploy for manual scan review — releases slow to
weekly. What do you do?"*

Automate scans in CI, fail on critical CVEs, cache results, parallelize,
risk-based tiers (internal tool vs customer-facing), measure lead time and
incident rate to justify policy tuning.
""",
        },
        {
            "slug": "week3-checkpoint",
            "title": "Week 3 checkpoint: infrastructure lab",
            "summary": "Terraform + Azure + secrets — consolidate before interview week.",
            "minutes": 12,
            "outcomes": ("Deploy infra with Terraform and document blast radius",),
            "body": """
## Week 3 recap

Can you explain without notes:

- Terraform state, modules, and drift
- Core Azure services for a container platform
- Config vs secrets separation
- Five DevSecOps pipeline gates

## Hands-on lab

Using free tier or existing subscription:

1. `terraform init/plan/apply` a resource group + ACR (or storage account)
2. Store a secret in Key Vault; reference from a sample app config
3. Run `terraform plan` after a manual portal tweak — observe drift
4. Write a 5-line PR description with blast-radius notes

## Mock system design (15 min)

*"Design CI/CD for 50 microservices on AKS with compliance requirements."*

Touch: mono-repo vs multi-repo, shared pipeline templates, GitOps, env promotion,
central logging, policy-as-code, identity federation.

## Gate to Week 4

If Terraform or Azure still feels fuzzy, spend two extra days here. Week 4
assumes you can talk infra confidently while adding ops and interview polish.
""",
        },
        {
            "slug": "observability-slo-interview",
            "title": "Week 4, Day 1: Observability & SLO interview answers",
            "summary": "Metrics, logs, traces, SLIs/SLOs, and alerting that pages humans for real problems.",
            "minutes": 16,
            "quiz_slug": "observability-basics",
            "outcomes": ("Define SLIs and SLOs for a service you know",),
            "body": """
## Three pillars (+ profiling)

- **Metrics**: counters, gauges, histograms — RED/USE methods
- **Logs**: structured JSON, correlation IDs
- **Traces**: distributed tracing across microservices (OpenTelemetry)
- **Profiling**: continuous profiling for CPU/memory hotspots (bonus points)

## SLI → SLO → error budget

- **SLI**: measurable signal (availability, latency p99, error rate)
- **SLO**: target over window (99.9% availability / 30 days)
- **Error budget**: allowed unreliability; drives release risk decisions

## Alerting that doesn't burn out on-call

Alert on **symptoms** (SLO burn rate), not every CPU spike.

Multi-window burn alerts (Google SRE book pattern):

- Fast burn → page immediately
- Slow burn → ticket or next-day review

## Azure tooling

Application Insights: requests, dependencies, exceptions, live metrics.
Log Analytics KQL for cross-service queries. Workbooks for dashboards.

## Interview scenario

*"Error rate doubled after deploy — walk through your first 10 minutes."*

Check deployment timeline, rollback if user-impacting, compare golden signals,
recent config/feature flag changes, dependency health, then deep dive traces
for failing span.
""",
        },
        {
            "slug": "incident-response-interview",
            "title": "Week 4, Day 2: Incident response & postmortems",
            "summary": "Mitigate first, communicate clearly, blameless learning — enterprise expectations.",
            "minutes": 14,
            "outcomes": ("Tell a blameless postmortem story with action items",),
            "body": """
## Incident lifecycle

1. **Detect** — alert or user report
2. **Triage** — severity (SEV1–SEV4), incident commander
3. **Mitigate** — rollback, scale, failover, feature off — **users first**
4. **Communicate** — status updates on cadence (every 15–30 min for SEV1)
5. **Resolve** — fix forward or revert
6. **Learn** — blameless postmortem within 5 business days

## Roles at scale

- **Incident commander**: coordinates, doesn't deep-debug alone
- **Comms lead**: stakeholders and status page
- **Subject matter experts**: per subsystem

## Postmortem template

- Summary (customer impact, duration)
- Timeline (UTC timestamps, facts not opinions)
- Root causes and contributing factors ( plural — avoid single-root theater)
- What went well / what didn't
- Action items: owner, due date, tracked to completion

## Behavioral STAR example

Prepare a real incident: what broke, how you mitigated, what systemic fix
followed (better alert, runbook, automation — not "be more careful").

## Volvo / enterprise culture signal

Emphasize **safety and transparency**: no hiding incidents, no blame, improve
systems so the same failure mode is harder next time.
""",
        },
        {
            "slug": "behavioral-devops-interview",
            "title": "Week 4, Day 3: Behavioral & culture interview prep",
            "summary": "STAR stories, collaboration, conflict, and why DevOps is a team sport.",
            "minutes": 15,
            "outcomes": ("Prepare five STAR stories for common DevOps prompts",),
            "body": """
## Stories to prepare (STAR format)

Write these before interview day:

1. **Automated something painful** — saved time, reduced errors
2. **Disagreement with dev or security** — data-driven resolution
3. **Production incident you helped resolve** — mitigate-first mindset
4. **Mentored someone or improved team docs/runbooks**
5. **Learned a new tool under deadline** — humility + outcome

## Common behavioral questions

- Tell me about a time you improved deployment frequency or reliability.
- Describe a failed deploy and what changed afterward.
- How do you prioritize when everything is on fire?
- How do you work with developers who resist process?
- Why DevOps / why Volvo Group / why this team?

## Volvo Group values angle

Research the company's current priorities (electrification, software-defined
vehicles, sustainability). Connect your stories to:

- **Safety** — in systems and process
- **Quality** — gates, testing, traceability
- **Collaboration** — cross-functional teams, global orgs
- **Continuous improvement** — retros, metrics, automation

## Questions to ask them

- How is on-call structured for the platform team?
- What does success look like in the first 90 days?
- Biggest bottleneck in delivery today?
- Balance between feature work and platform reliability?

Good questions signal seniority.
""",
        },
        {
            "slug": "technical-mock-drills",
            "title": "Week 4, Day 4: Technical mock interview drills",
            "summary": "Timed scenarios: pipeline design, K8s debug, Terraform, and troubleshooting.",
            "minutes": 16,
            "outcomes": ("Complete three timed mock scenarios out loud",),
            "body": """
## Drill 1 — Pipeline design (20 min)

*"Design CI/CD for a Java microservice on AKS with security scans and prod approval."*

Checklist: PR validation, build JAR + Docker image, scan, push to ACR, deploy
to staging with integration tests, manual prod gate, canary or rolling, smoke
tests, rollback via previous manifest tag.

## Drill 2 — Kubernetes debug (15 min)

*"Pods in CrashLoopBackOff after config change."*

`kubectl describe`, events, logs `--previous`, config mount errors, secret
missing key, probe failing too aggressively, resource limits.

## Drill 3 — Terraform troubleshooting (10 min)

*"State lock error during apply."*

Who holds lock, stale lock break procedure, coordination in team chat, never
two applies on same state.

## Drill 4 — Linux/network (10 min)

*"Intermittent 504 from API gateway."*

Upstream timeout vs client timeout, backend saturation, DB connection pool,
recent deploy, trace slow spans.

## How to practice

- Record audio — listen for rambling and filler
- Use a timer — interviewers notice structure under pressure
- End each answer with **trade-offs** or **what you'd monitor**

## Pair with DevResurge quizzes

Re-take **CI/CD**, **Docker**, **Linux**, and **Observability** quizzes until
you pass comfortably — they're aligned with these drills.
""",
        },
        {
            "slug": "final-checklist-interview-day",
            "title": "Week 4, Day 5: Final checklist & interview day",
            "summary": "Last review, cheat sheet, and calm execution on interview day.",
            "minutes": 14,
            "outcomes": ("Walk into the interview with a one-page cheat sheet",),
            "body": """
## One-page cheat sheet (write yours by hand)

**Pipeline**: build once → scan → stage → prod → rollback path

**K8s**: Deployment rollout/undo, probes, Service vs Ingress

**Azure**: AKS, ACR, Key Vault, Monitor, managed identity

**Terraform**: remote state, plan review, modules, drift

**Ops**: SLI/SLO, mitigate first, blameless postmortem

**Git**: trunk-based, small PRs, protected main

## Night before

- Sleep 7+ hours — cognitive performance beats last-minute cramming
- Lay out quiet space, water, charger for video interviews
- Re-read your five STAR stories once, not fifty new topics

## Interview day flow

1. Join 2 minutes early; test camera/mic
2. Clarify ambiguous questions before diving deep
3. Think out loud — silence reads as stuck
4. Use structure: "First I'd check… then… rollback if…"
5. Admit gaps honestly: "I haven't used X in prod, but I'd approach it by…"

## After each round

Journal: questions asked, what felt weak, one improvement for next round.
Update your cheat sheet — interviews are iterative.

## You are ready when

- You can whiteboard a full pipeline in 5 minutes
- You have three incident/collaboration stories polished
- You've containerized and deployed at least one project
- Quiz scores on DevResurge reflect consistent passes

> Enterprise DevOps hiring rewards **reliable humans who automate wisely** —
> not heroes who hide problems. You've spent 30 days building that signal. Go
> show them.
""",
        },
    ],
}
