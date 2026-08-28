ROADMAP = {
    "slug": "devops-interview-usa",
    "title": "30-day DevOps sprint: USA & visa sponsors",
    "tagline": "H-1B, O-1, and big-tech enterprise loops — AWS, EKS, system design, and STAR stories.",
    "description": (
        "A one-month DevOps interview plan for the United States job market at "
        "employers who sponsor work visas (H-1B, O-1, L-1, TN where eligible). "
        "Covers FAANG-adjacent bar, financial services and scale-up patterns, "
        "AWS-heavy infrastructure, and the high-intensity US interview loop."
    ),
    "domain": "devops",
    "level": "advanced",
    "icon": "🇺🇸",
    "order": 49,
    "audience": (
        "International engineers targeting US DevOps, SRE, or platform roles with "
        "employer visa sponsorship."
    ),
    "outcomes": (
        "Navigate H-1B timing and sponsor employer strategies",
        "Perform in multi-round US technical and behavioral loops",
        "Demonstrate AWS, Kubernetes, IaC, and SRE system design depth",
    ),
    "related_quiz_slugs": (
        "linux-shell",
        "git-collaboration",
        "containers-docker",
        "cicd-devops",
        "observability-basics",
        "system-design-basics",
        "distributed-systems-basics",
    ),
    "lessons": [
        {
            "slug": "us-devops-battle-plan",
            "title": "Week 0: USA sprint battle plan",
            "summary": "Aggressive timeline, lottery reality, and how US loops differ from EU/APAC.",
            "minutes": 12,
            "outcomes": ("Plan applications around H-1B cap calendar if applicable",),
            "body": """
## US DevOps market

Highest salaries globally; **most competitive** interviews. Sponsorship is common at
large tech, finance, and healthcare — rare at tiny startups unless well-funded.

## Visa overview (not legal advice)

**H-1B** — specialty occupation; annual cap + lottery for many employers; cap-exempt
(universities, some research orgs) skip lottery.

**O-1** — extraordinary ability; evidence-heavy; no lottery; common for senior/staff.

**L-1** — intracompany transfer after working abroad for same employer 1+ year.

**TN** — USMCA citizens (Canada/Mexico) for specific professions.

## US loop shape

Recruiter → phone screen → 1–3 technical (coding light for DevOps but scripting
common) → system design / infrastructure design → behavioral → hiring committee.

## Four weeks

| Week | Focus |
|------|-------|
| 1 | Visa strategy + foundations + resume |
| 2 | AWS/EKS + CI/CD depth |
| 3 | SRE design + IaC + security |
| 4 | Behavioral + mocks + negotiation |

Start applications **months** before desired start — H-1B filing is March/April for October start historically.
""",
        },
        {
            "slug": "us-visa-sponsor-landscape",
            "title": "Week 1: Sponsorship & employer strategy",
            "summary": "H-1B lottery, cap-exempt, O-1, and reading sponsor history.",
            "minutes": 15,
            "outcomes": ("Build a sponsor-tier list of US employers",),
            "body": """
## Sponsor tiers

**Tier 1 — Frequent sponsors**
Amazon, Google, Microsoft, Meta, Apple, Netflix, Salesforce, Uber, major banks
(JPM, Goldman), healthcare systems, consulting (Deloitte, Accenture — verify project).

**Tier 2 — Selective sponsors**
Well-funded unicorns, mid-size SaaS with mobility team — ask explicitly.

**Tier 3 — Rare sponsors**
Early startups unless CEO commits in writing + lawyer draft.

## Research tactics

- USCIS H-1B employer data (historical filings — not guarantee)
- LinkedIn "H1B" + company filter
- Glassdoor interview + sponsorship reviews
- Ask recruiter: *"Will you file cap-subject H-1B? Premium processing? O-1 if not selected?"*

## H-1B timeline awareness

Job offer → LCA → registration (cap) → petition if selected → approval → start date.
Miss lottery? Plan O-1 evidence building or cap-exempt roles or study/OPT bridge if eligible.

## Red flags

- "We sponsor after probation" with no written policy
- Contractor 1099 only
- Salary below prevailing wage for LCA
""",
        },
        {
            "slug": "us-employers-and-stacks",
            "title": "Week 1: US employers & infrastructure stacks",
            "summary": "Where DevOps/SRE roles cluster and what each layer expects.",
            "minutes": 15,
            "outcomes": ("Tailor resume keywords to target employer tier",),
            "body": """
## Role title map

Same work, different titles: **DevOps Engineer**, **SRE**, **Platform Engineer**,
**Infrastructure Engineer**, **Production Engineer** (Meta), **SDE Infra** (Amazon).

## Stack by employer type

| Type | Stack hints |
|------|-------------|
| Hyperscaler | Internal + AWS/GCP; massive scale, strict design rounds |
| Enterprise SaaS | AWS EKS, Terraform, Datadog, GitHub Actions |
| Finance | AWS/Azure, change mgmt, SOC2, low tolerance for downtime |
| Startups | Heroku→K8s migration stories; cost + speed |

## Resume for US

One page (two max senior), **metrics everywhere**: availability %, cost $M saved,
deploy frequency, MTTR, incidents prevented. No photo. ATS keywords from job post.

## Levels matter

L4/L5 (Google), E4/E5 (Meta), SDE II/III (Amazon) — research leveling before comp talk.
""",
        },
        {
            "slug": "us-foundations-interview",
            "title": "Week 1: Foundations + scripting round",
            "summary": "Linux, Git, Python/Bash — US loops often include light live coding.",
            "minutes": 15,
            "quiz_slug": "linux-shell",
            "outcomes": ("Solve a 20-minute scripting problem cleanly",),
            "body": """
## Scripting interview examples

- Parse log file for top 10 error codes
- Write Bash/Python to health-check URL list
- Automate rolling restart with health wait

Practice on LeetCode Easy string/hash problems + real ops scripts.

## Systems fundamentals

Processes, threads, file descriptors, TCP vs UDP, DNS, HTTP/2, TLS handshake — SRE
loops at Google/Amazon depth.

## Quizzes

Pass **linux-shell**, **git-collaboration**, **networking-fundamentals** on DevResurge.

## Amazon LP preview

Behavioral at Amazon uses **Leadership Principles** — prepare 2 stories per LP you
claim (Customer Obsession, Ownership, Dive Deep, Bias for Action, etc.).
""",
        },
        {
            "slug": "us-aws-eks-deep",
            "title": "Week 2: AWS & EKS — US default stack",
            "summary": "Deep EKS, IAM, networking — infrastructure design round prep.",
            "minutes": 16,
            "quiz_slug": "containers-docker",
            "outcomes": ("Design multi-AZ EKS platform on whiteboard",),
            "body": """
## Design round topics

- VPC layout (public/private subnets, NAT cost vs VPC endpoints)
- EKS control plane vs data plane responsibility
- IRSA for pod AWS access
- Cluster autoscaler + HPA + Karpenter
- GitOps (Flux/Argo CD) vs push deploy
- Disaster recovery: RTO/RPO, backup Velero, multi-region strategy

## Common follow-ups

- How would you migrate monolith to EKS without downtime?
- Secrets rotation with External Secrets Operator
- NetworkPolicy default deny + explicit allow
- Cost optimization at 500-node scale

## Study pairing

DevResurge **system-design-basics** and **distributed-systems-basics** quizzes +
lessons from **distributed systems** roadmap.
""",
        },
        {
            "slug": "us-cicd-at-scale",
            "title": "Week 2: CI/CD at US scale",
            "summary": "Monorepo, thousands of deploys/day, safe progressive delivery.",
            "minutes": 15,
            "quiz_slug": "cicd-devops",
            "outcomes": ("Explain canary analysis and automated rollback",),
            "body": """
## Scale patterns

- Trunk-based dev, feature flags (LaunchDarkly, internal)
- Build graph caching (Bazel, Gradle remote cache)
- Deployment pipelines as product — developer self-service
- Automated canary analysis (Kayenta-style) on metrics
- Rollback in <5 minutes is table stakes at top cos

## Interview question

*"1000 microservices — how prevent one bad deploy from taking down checkout?"*

Blast radius limits, circuit breakers, progressive delivery, dependency graphs,
critical path isolation, error budgets per service tier.
""",
        },
        {
            "slug": "us-terraform-iac",
            "title": "Week 3: Terraform & platform engineering",
            "summary": "IaC at org scale — modules, policy, and self-service platforms.",
            "minutes": 14,
            "outcomes": ("Describe platform team product thinking",),
            "body": """
## Platform interview angle

US senior roles expect **internal developer platform** thinking:

- Golden paths, paved roads, escape hatches documented
- Terraform modules + Backstage/service catalog
- Policy as code (OPA, Sentinel, Cloud Custodian)
- Cost attribution per team

## Terraform deep cuts

State sharding, `-target` abuse prevention, import at scale, drift detection,
testing with terratest, module versioning semver.
""",
        },
        {
            "slug": "us-sre-observability",
            "title": "Week 3: SRE, SLIs, and observability depth",
            "summary": "Google SRE book concepts — US loops treat these as core.",
            "minutes": 16,
            "quiz_slug": "observability-basics",
            "outcomes": ("Run error budget meeting narrative",),
            "body": """
## SRE interview staples

- SLI/SLO/error budget policy
- Toil measurement and elimination targets (<50% toil)
- Incident command, severity levels, postmortem culture
- Capacity planning from traffic forecasts
- HA: N+1, zone redundancy, graceful degradation

## Observability

Prometheus histograms, exemplars, OpenTelemetry, high-cardinality pitfalls,
sampling strategies for traces at scale.

## Question

*"Should we launch feature if error budget is 90% consumed?"*

Discuss risk, stakeholder trade-off, partial rollout, freeze policy — show judgment not dogma.
""",
        },
        {
            "slug": "us-security-compliance",
            "title": "Week 3: Security — SOC2, FedRAMP awareness",
            "summary": "DevSecOps expectations at US enterprise and gov contractors.",
            "minutes": 14,
            "quiz_slug": "security-basics",
            "outcomes": ("Map SOC2 trust principles to your pipeline",),
            "body": """
## Compliance touchpoints

**SOC2** — security, availability, confidentiality controls auditors test.
**FedRAMP** — gov cloud; stricter change and access (awareness if applying to contractors).
**PCI** — if payment path touches your infra.

## Pipeline controls

Immutable artifacts, signed images (Cosign), SBOM, branch protection, MFA,
break-glass audited, vulnerability SLAs by severity.
""",
        },
        {
            "slug": "us-behavioral-negotiation",
            "title": "Week 4: Behavioral loops & offer negotiation",
            "summary": "STAR, Leadership Principles, and US comp (base, RSU, signing).",
            "minutes": 15,
            "outcomes": ("Prepare 10 STAR stories and comp negotiation anchors",),
            "body": """
## Behavioral depth

US panels probe **conflict, failure, influence without authority, mentoring, ambiguity**.
Use STAR; keep stories 2–3 minutes; quantify results.

## Compensation

Base salary + **RSU/equity** + signing bonus + relocation. Negotiate total comp;
levels.fyi for anchors. Multiple offers strengthen leverage.

## Visa negotiation

Clarify: filing fees, premium processing, immigration lawyer, H-1B lottery backup plan,
green card PERM timeline (often multi-year — ask honestly).
""",
        },
        {
            "slug": "us-system-design-infra",
            "title": "Week 4: Infrastructure system design mocks",
            "summary": "Design CDN, CI platform, or metrics pipeline — US senior bar.",
            "minutes": 16,
            "quiz_slug": "system-design-basics",
            "outcomes": ("Complete one 45-minute infra design mock aloud",),
            "body": """
## Sample prompts

- Design GitHub Actions–scale CI for 10k repos
- Global metrics ingestion (Prometheus remote write)
- Zero-downtime migration from data center to AWS
- Multi-tenant Kubernetes platform for internal teams

## Framework

Requirements → scale estimates → API/data model → high-level diagram → deep dive
bottleneck → failure modes → observability → cost.

## Practice

Record 45 min session; cut filler words; check you stated assumptions upfront.
""",
        },
        {
            "slug": "us-mock-drills-final",
            "title": "Week 4: Final mocks & interview checklist",
            "summary": "Full-loop simulation and H-1B timeline coordination.",
            "minutes": 14,
            "outcomes": ("Run full mock loop and finalize cheat sheet",),
            "body": """
## Full mock day

1. 30 min scripting
2. 45 min infra design (EKS platform)
3. 30 min behavioral (LP-style)
4. 15 min your questions for them

## Cheat sheet

AWS map | EKS patterns | SLO math | STAR titles | Sponsor tier list | Comp targets

## Ready when

- Quizzes passed including system design
- 2+ sponsor employers in pipeline
- Immigration lawyer consult for your nationality situation
- Demo project with README metrics

The US market rewards depth and clear communication under pressure. You've got this.
""",
        },
    ],
}
