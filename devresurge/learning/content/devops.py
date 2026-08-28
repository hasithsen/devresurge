ROADMAP = {
    "slug": "devops-sre",
    "title": "DevOps & SRE",
    "tagline": "Ship safely: CI/CD, containers, infra, and production hygiene.",
    "description": (
        "The operational craft behind elite engineering: automated delivery, "
        "containers, infrastructure as code, observability, and incident response."
    ),
    "domain": "devops",
    "level": "intermediate",
    "icon": "⚙",
    "order": 50,
    "audience": "Engineers who want production ownership — not just local demos.",
    "outcomes": (
        "Design a sane CI/CD pipeline with quality gates",
        "Containerize and reason about orchestration basics",
        "Respond to incidents with blameless rigor",
    ),
    "related_quiz_slugs": (
        "linux-shell",
        "containers-docker",
        "cicd-devops",
        "observability-basics",
    ),
    "lessons": [
        {
            "slug": "cicd-pipeline",
            "title": "CI/CD that protects main",
            "summary": "Build, test, scan, deploy — with fast feedback and safe rollout.",
            "minutes": 14,
            "quiz_slug": "cicd-devops",
            "outcomes": ("Sketch a pipeline for a real service",),
            "body": """
## Pipeline stages

1. Lint / typecheck / unit tests (fast fail)
2. Build artifact (image / binary) with immutable tag
3. Integration tests
4. Security scans (deps, container)
5. Deploy to staging
6. Smoke tests
7. Progressive prod deploy (rolling / canary)
8. Automatic rollback triggers

## Branch strategy

Keep main releasable. Feature flags > long-lived branches.

## Speed matters

>10 minute feedback kills flow. Parallelize; cache deps; fail early.

## Artifact discipline

Build once; promote the same artifact across environments.

## Interview questions to rehearse

1. Draw your pipeline on a whiteboard — 8 boxes minimum.
2. Where do you fail fastest? Where is prod approval?
3. How do you rollback in under five minutes?
4. What DORA metrics would you track?
""",
        },
        {
            "slug": "containers-runtime",
            "title": "Containers and runtime basics",
            "summary": "Images, layers, processes, healthchecks, resource limits.",
            "minutes": 14,
            "quiz_slug": "containers-docker",
            "outcomes": ("Write production-minded Dockerfiles",),
            "body": """
## Image hygiene

- Minimal base images
- Non-root user
- Multi-stage builds
- Pin digests for supply-chain sanity
- Don't bake secrets into layers

## Runtime

- One primary process per container
- Health/readiness probes mean different things
- CPU/memory limits prevent noisy neighbors
- Logs to stdout/stderr

## Orchestration peek

Kubernetes schedules pods, restarts failures, and rolls deploys — learn concepts before YAML trivia.

## Lab

Multi-stage Dockerfile for a web app; run with memory limit; break healthcheck on purpose.
""",
        },
        {
            "slug": "linux-and-networking-ops",
            "title": "Linux + networking for operators",
            "summary": "Processes, files, permissions, DNS, and debugging connectivity.",
            "minutes": 14,
            "quiz_slug": "linux-shell",
            "outcomes": ("Debug a broken deploy with shell tools",),
            "body": """
## Everyday toolkit

`ps`, `top`/`htop`, `ss`/`lsof`, `curl`, `dig`, `jq`, `tail -F`, `strace` (sparingly).

## Permissions & users

Understand UID mapping in containers; file modes; secrets mounted as files.

## Connectivity debug

- DNS resolution inside the pod/host?
- Port open and listening?
- Security group / NetworkPolicy blocking?
- TLS verify failing?

## Practice

Trace why service A cannot reach service B — write the decision tree.
""",
        },
        {
            "slug": "iac-and-environments",
            "title": "Infrastructure as code & environments",
            "summary": "Reproducible infra; env parity; secrets and config separation.",
            "minutes": 12,
            "outcomes": ("Treat infra changes like code reviews",),
            "body": """
## Why IaC

ClickOps doesn't scale and can't be reviewed. Terraform/CloudFormation/Pulumi make changes auditable.

## Environment parity

Dev/stage/prod differences should be **data/config**, not mystery snowflakes.

## Config vs secret

- Config: non-sensitive, versioned
- Secrets: vault/SM, short-lived where possible
- Twelve-factor: env-based config

## Review bar

Infra PRs need blast-radius notes and plan output review.
""",
        },
        {
            "slug": "observability-sre",
            "title": "Observability and SRE practice",
            "summary": "SLIs/SLOs, alerting that doesn't page noise, and dashboards that answer questions.",
            "minutes": 14,
            "quiz_slug": "observability-basics",
            "outcomes": ("Define SLIs for a service you know",),
            "body": """
## SLI → SLO → alert

- SLI: measurable user happiness proxy (availability, latency)
- SLO: target over a window
- Alert on **burn rate** / symptom, not every CPU blip

## Golden signals

Latency, traffic, errors, saturation — start here.

## Cardinality

High-cardinality labels explode metrics cost and query time. Be intentional.

## On-call hygiene

Pages must be actionable. If not, fix the alert — don't accept pager spam.
""",
        },
        {
            "slug": "incidents",
            "title": "Incident response",
            "summary": "Mitigate first, then diagnose; blameless postmortems that change systems.",
            "minutes": 12,
            "outcomes": ("Run a crisp incident timeline",),
            "body": """
## During the fire

1. Declare incident / severity
2. Mitigate user impact (rollback, failover, feature flag off)
3. Communicate status on a cadence
4. Then deep diagnosis

## Roles

Incident commander, comms, ops — separate when severity warrants.

## Postmortem

- Timeline of facts
- Contributing factors (not root-cause theater)
- Action items with owners/dates
- Blameless culture → more truth → fewer repeats

## Drill

Tabletop: "p99 latency 10× after deploy" — what do you check first?
""",
        },
        {
            "slug": "devops-sre-complete-resources",
            "title": "Complete DevOps/SRE reference guide",
            "summary": "Official docs, quizzes, labs, and pass checklist for production craft.",
            "minutes": 15,
            "outcomes": ("Use as ongoing reference after clearing all quests",),
            "body": """
## Pass criteria — DevOps & SRE questline

- [ ] All 7 lessons cleared (6 core + this guide)
- [ ] Quizzes passed: [CI/CD](/quizzes/cicd-devops/), [Docker](/quizzes/containers-docker/), [Linux](/quizzes/linux-shell/), [Observability](/quizzes/observability-basics/)
- [ ] One service deployed with pipeline, probes, and dashboard
- [ ] One blameless postmortem written (real or tabletop)
- [ ] Runbook for "latency 10× after deploy" documented

## Interview sprint paths (visa sponsors)

Preparing for relocation interviews? Add one [regional elective](/learn/) (visa + culture) alongside this craft path.
""",
        },
    ],
}
