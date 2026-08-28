ROADMAP = {
    "slug": "devops-interview-uk",
    "title": "30-day DevOps sprint: UK & visa sponsors",
    "tagline": "Skilled Worker sponsors — fintech, scale-ups, AWS/GCP, and UK compliance culture.",
    "description": (
        "A one-month DevOps interview plan for United Kingdom roles at employers "
        "with Skilled Worker sponsor licences. Covers London fintech (Revolut, Monzo, "
        "Wise), scale-ups, regulated finance, NHS digital, and the GitOps/Kubernetes "
        "patterns common in UK platform teams."
    ),
    "domain": "devops",
    "level": "intermediate",
    "icon": "🇬🇧",
    "order": 51,
    "audience": (
        "International engineers targeting UK DevOps/platform roles requiring "
        "Skilled Worker visa sponsorship."
    ),
    "outcomes": (
        "Verify sponsor licence status and SOC code fit in job posts",
        "Interview confidently at UK fintech and enterprise employers",
        "Demonstrate AWS/GCP, Kubernetes, GitOps, and FCA-aware delivery",
    ),
    "related_quiz_slugs": (
        "linux-shell",
        "git-collaboration",
        "containers-docker",
        "cicd-devops",
        "observability-basics",
        "security-basics",
    ),
    "lessons": [
        {
            "slug": "uk-devops-battle-plan",
            "title": "Week 0: UK sprint battle plan",
            "summary": "Skilled Worker context, London vs regional hubs, four-week schedule.",
            "minutes": 12,
            "outcomes": ("Align study with Certificate of Sponsorship timeline",),
            "body": """
## UK DevOps market

London dominates (fintech, Big Tech EU HQs, consultancies). Manchester, Edinburgh,
Cambridge, Bristol strong for platform roles. Post-Brexit **Skilled Worker visa**
replaced Tier 2 General — employers need **sponsor licence** + CoS (Certificate of
Sponsorship).

## Four-week plan

| Week | Focus |
|------|-------|
| 1 | Skilled Worker + sponsors + foundations |
| 2 | AWS/GCP + K8s + GitOps |
| 3 | IaC, FCA/security, observability |
| 4 | Behavioral, mocks, relocation |

## Salary threshold awareness

Minimum salary rules tie to going rates and SOC codes — verify current Home Office
guidance for DevOps-adjacent codes (e.g. IT business analyst, programmer, IT specialist
— exact SOC matching matters).

> Not immigration advice. Confirm with UK employer's mobility team or OISC-regulated adviser.
""",
        },
        {
            "slug": "uk-visa-sponsor-landscape",
            "title": "Week 1: Skilled Worker visa & sponsors",
            "summary": "Sponsor licence, CoS, SOC codes, and ILR pathway context.",
            "minutes": 15,
            "outcomes": ("Check employer on UK sponsor register before interviewing",),
            "body": """
## Skilled Worker essentials

1. Employer holds valid **sponsor licence**
2. Job meets skill/salary thresholds for assigned **SOC code**
3. Employer issues **Certificate of Sponsorship (CoS)**
4. You apply for visa with CoS, English requirement, maintenance funds (rules vary)

## Verify sponsors

UK government **Register of Licensed Sponsors** — search employer name; check tier and status.

## Green flags

- HR confirms Skilled Worker sponsorship in writing
- Role SOC code discussed openly
- Salary stated gross £ meets threshold for that code
- Established mobility process (big banks, scale-ups, consultancies)

## Red flags

- Employer not on register
- "Contractor inside IR35 only" with no sponsorship
- Below-market pay "we'll fix after probation"

## ILR context (long-term)

Generally 5 years on Skilled Worker route toward indefinite leave to remain — rules
evolve; don't rely on course summary for life planning.
""",
        },
        {
            "slug": "uk-employers-and-stacks",
            "title": "Week 1: UK sponsor employers & stacks",
            "summary": "Fintech, banks, BBC, NHS digital — where platform roles concentrate.",
            "minutes": 15,
            "outcomes": ("Shortlist 15 licensed sponsors matching your stack",),
            "body": """
## Sponsor-rich sectors

**Fintech & banking (London)**
Revolut, Monzo, Starling, Wise, Barclays, HSBC, Lloyds — Kubernetes, AWS/GCP,
strong compliance interview angle.

**Scale-ups & product**
Deliveroo, Sky Bet, BBC, Guardian, Autotrader — platform teams, GitOps, Datadog.

**Consultancies & SI**
Thoughtworks, EPAM, Capgemini — sponsor but clarify bench between projects.

**Health & public**
NHS digital suppliers, ARM (Cambridge) — security clearance possible.

## UK stack patterns

| Pattern | Tools |
|---------|-------|
| Cloud | AWS dominant; GCP at some fintech |
| K8s | EKS/GKE, Helm, Argo CD/Flux |
| IaC | Terraform standard |
| CI | GitHub Actions, CircleCI, GitLab |
| Observability | Datadog, Prometheus, Splunk in banks |

## Job search

LinkedIn London + "visa sponsorship", Otta, Cord, company careers, **Workable** boards.
""",
        },
        {
            "slug": "uk-foundations-interview",
            "title": "Week 1: Foundations for UK loops",
            "summary": "Linux, Git, networking — plus pair programming culture at UK fintech.",
            "minutes": 14,
            "quiz_slug": "linux-shell",
            "outcomes": ("Pass core DevResurge foundation quizzes",),
            "body": """
## UK interview formats

- **Take-home** infra task (Terraform module, pipeline YAML) — common at scale-ups
- **Pairing** on pipeline fix or kubectl debug
- **System design** for platform (less common junior, standard senior)

## Technical baseline

Same global DevOps bar: shell, Git, HTTP, containers, cloud CLI.

## Fintech extra

Explain change management, audit logs, segregation of duties — unprompted bonus points.

Complete quizzes: **linux-shell**, **git-collaboration**, **networking-fundamentals**.
""",
        },
        {
            "slug": "uk-kubernetes-gitops",
            "title": "Week 2: Kubernetes & GitOps",
            "summary": "EKS/GKE, Argo CD, progressive delivery — UK platform default.",
            "minutes": 16,
            "quiz_slug": "containers-docker",
            "outcomes": ("Explain GitOps rollback vs kubectl rollback",),
            "body": """
## GitOps interview flow

```
Git merge → Argo CD sync → cluster state matches repo
Rollback = revert Git commit or pin previous manifest tag
```

## Topics

Helm charts vs Kustomize, ApplicationSets for multi-env, sealed secrets/external secrets,
NetworkPolicy, Pod Security Standards, cluster upgrades without downtime.

## Progressive delivery

Argo Rollouts canaries, Flagger, service mesh (Istio/Linkerd) where maturity warrants.

## Question

*"Developer kubectl apply'd to prod bypassing GitOps."*

Detect drift (Argo OutOfSync), revoke direct cluster admin, educate, enforce admission
controller, audit log review.
""",
        },
        {
            "slug": "uk-aws-gcp-cloud",
            "title": "Week 2: AWS & GCP for UK employers",
            "summary": "Multi-cloud fluency — many London shops run AWS or GCP exclusively.",
            "minutes": 15,
            "outcomes": ("Compare EKS vs GKE for a fintech microservices platform",),
            "body": """
## AWS (common)

EKS, IRSA, ALB ingress, VPC design, KMS encryption, CloudTrail, AWS Config rules.

## GCP (fintech adopters)

GKE, Workload Identity, Cloud Load Balancing, Binary Authorization for images.

## UK data residency

Post-GDPR UK GDPR regime — discuss region (eu-west-2 London), DPA with cloud provider,
encryption, data processing agreements.

## Whiteboard

Multi-account/project setup: prod/nonprod separation, CI OIDC to cloud, central logging account.
""",
        },
        {
            "slug": "uk-cicd-regulated",
            "title": "Week 2–3: CI/CD in regulated UK finance",
            "summary": "FCA-aware delivery, audit trails, and controlled prod access.",
            "minutes": 15,
            "quiz_slug": "cicd-devops",
            "outcomes": ("Design pipeline with immutable audit log",),
            "body": """
## FCA operational resilience (awareness)

Important business services, impact tolerances, self-assessment — DevOps implements
monitoring, DR testing, change records.

## Pipeline controls banks expect

- Immutable build logs retained years
- Four-eyes approval for prod
- Automated tests + manual gate for critical systems
- Segregation: devs cannot deploy prod directly

## Scale-up contrast

Move fast with automated canary; still show audit via Git history + deployment annotations.

## Scenario

*"Auditor asks who deployed version X at time T."*

Git SHA → pipeline run ID → deployment record → CloudTrail/audit log chain.
""",
        },
        {
            "slug": "uk-terraform-iac",
            "title": "Week 3: Terraform & platform standards",
            "summary": "Modules, policy-as-code, and UK enterprise tagging.",
            "minutes": 14,
            "outcomes": ("Review a Terraform PR like a UK platform team lead",),
            "body": """
## IaC interview focus

Remote state, module boundaries, `terraform plan` in CI, Checkov/tfsec gates,
prevent_destroy on stateful resources, import strategy for acquisitions.

## FinOps

UK enterprises face cloud cost scrutiny — tags for cost centre, budgets, anomaly alerts.

## Platform product mindset

Self-service namespace provisioning with quotas; document in internal portal; measure adoption.
""",
        },
        {
            "slug": "uk-observability-incidents",
            "title": "Week 3: Observability & incidents",
            "summary": "SLOs, on-call, and postmortems — UK on-call compensation varies.",
            "minutes": 15,
            "quiz_slug": "observability-basics",
            "outcomes": ("Define SLOs for a payments API",),
            "body": """
## Tooling

Datadog very common in London fintech; Prometheus stack at infra-native cos; Splunk in banks.

## On-call

Ask: rotation length, compensation (time off in lieu vs pay), escalation to engineering manager.

## Incident + regulatory

Payment outages may trigger comms to compliance — show awareness in STAR stories without overclaiming legal knowledge.
""",
        },
        {
            "slug": "uk-security-gdpr",
            "title": "Week 3: Security, GDPR & supply chain",
            "summary": "DevSecOps plus UK/EU privacy expectations.",
            "minutes": 14,
            "quiz_slug": "security-basics",
            "outcomes": ("Explain how CI/CD supports GDPR technical measures",),
            "body": """
## GDPR technical measures (DevOps angle)

Encryption at rest/transit, access logging, retention automation, pseudonymisation in non-prod,
breach detection tooling, DPIA support with engineering input.

## Supply chain

Dependabot, signed containers, admission controllers rejecting unsigned images in prod.

## Interview trap

*"Copy prod DB to staging for debugging."*

Reject — use masked/synthetic data; audit access; least privilege.
""",
        },
        {
            "slug": "uk-behavioral-culture",
            "title": "Week 4: Behavioral & UK workplace culture",
            "summary": "Politeness, direct feedback, pub test, and diversity awareness.",
            "minutes": 14,
            "outcomes": ("Prepare STAR stories for UK panel interviews",),
            "body": """
## Cultural notes

- Professional politeness; less brag than US, more than some Nordic cultures
- **Pub lunch** social norm on some teams — soft rapport builder
- Bank vs startup tone — adapt stories
- Right to work checks — sponsorship handled by employer HR

## Questions to ask

- CoS timeline after offer?
- Skilled Worker costs covered?
- On-call and hybrid policy (London office expectations)?
- Visa extension and ILR support long-term?
""",
        },
        {
            "slug": "uk-relocation-practical",
            "title": "Week 4: Relocation & settling in the UK",
            "summary": "NI number, NHS, housing, and first 90 days.",
            "minutes": 12,
            "outcomes": ("Draft relocation checklist from visa to Day 1",),
            "body": """
## After offer

CoS → visa application → biometric appointment → BRP/digital status → travel → start date.

## Practical setup

**National Insurance** number, bank account (often needs proof of address), GP registration,
council tax awareness, London housing costs (negotiate relocation stipend).

## First 90 days

Learn change advisory process if bank; ship small reliability win; build security stakeholder relationships.
""",
        },
        {
            "slug": "uk-mock-drills-final",
            "title": "Week 4: Mock drills & final checklist",
            "summary": "GitOps design, FCA scenario, Skilled Worker-ready portfolio.",
            "minutes": 14,
            "outcomes": ("Complete mocks and one-page UK cheat sheet",),
            "body": """
## Mock 1 — GitOps platform (20 min)

Multi-env Argo CD, secrets, canary, audit trail.

## Mock 2 — Regulated deploy (15 min)

Emergency prod fix during change freeze — controlled exception path.

## Mock 3 — Sponsor HR (10 min)

Questions you'd ask about CoS, SOC code, salary threshold.

## Cheat sheet

Skilled Worker steps | Sponsor register | GitOps flow | FCA awareness bullets | Target employers

## Ready when

Licensed sponsor list applied, take-home quality demo repo, quizzes passed, STAR stories ready.

Best of luck — London platform teams hire engineers who ship safely in regulated environments.
""",
        },
    ],
}
