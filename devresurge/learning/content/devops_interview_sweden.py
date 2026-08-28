ROADMAP = {
    "slug": "devops-interview-sweden",
    "title": "30-day DevOps sprint: Sweden & visa sponsors",
    "tagline": "Interview-ready for Swedish employers who sponsor work permits — Azure, K8s, and Nordic hiring culture.",
    "description": (
        "A one-month plan for DevOps roles at visa-sponsoring companies in Sweden: "
        "Volvo Group, Spotify, Klarna, Ericsson, Scania, IKEA Tech, and similar "
        "employers. Covers the Swedish job market, work-permit basics, technical "
        "interviews, and the Azure/Kubernetes stack common in Nordic enterprise."
    ),
    "domain": "devops",
    "level": "intermediate",
    "icon": "🇸🇪",
    "order": 46,
    "audience": (
        "International engineers targeting Swedish DevOps roles with employer "
        "sponsorship — not EU citizens without existing work rights."
    ),
    "outcomes": (
        "Identify visa-sponsoring employers and role signals in job posts",
        "Prepare for Swedish-style technical and collaborative interviews",
        "Demonstrate Azure, Kubernetes, and enterprise CI/CD fluency",
    ),
    "related_quiz_slugs": (
        "linux-shell",
        "git-collaboration",
        "containers-docker",
        "cicd-devops",
        "observability-basics",
    ),
    "lessons": [
        {
            "slug": "se-devops-battle-plan",
            "title": "Week 0: Sweden sprint battle plan",
            "summary": "Daily schedule, what Swedish teams hire for, and how this course fits.",
            "minutes": 12,
            "outcomes": ("Block four weeks of study and application time",),
            "body": """
## Why Sweden for DevOps

Sweden has a persistent shortage of senior engineers. Many employers **sponsor
work permits** for qualified DevOps, platform, and SRE candidates — especially
in Gothenburg (automotive/industrial), Stockholm (fintech/media), and Malmö/Lund
(tech hubs).

## This sprint vs other DevResurge paths

- **DevOps & SRE** roadmap — deep technical craft (take in parallel)
- **30-day DevOps interview sprint** — generic enterprise prep
- **This course** — Sweden-specific employers, visa signals, Nordic culture

## Four-week schedule (≈1 hr/day)

| Week | Focus |
|------|-------|
| 1 | Visa landscape + foundations + job search |
| 2 | Azure, CI/CD, containers (Swedish enterprise stack) |
| 3 | IaC, security, observability |
| 4 | Behavioral fit, mocks, relocation prep |

## What Swedish interviewers score

- **Collaboration** — flat hierarchies, consensus, no hero culture
- **Safety & quality** — especially automotive, telecom, fintech
- **English fluency** — Swedish is a bonus, rarely required for DevOps
- **Technical depth** — pipelines, K8s, cloud, incident response
- **Sustainability of pace** — burnout is taken seriously; show balance

> Not legal advice. Always confirm visa rules with Migrationsverket and your employer's relocation team.

## Pass criteria — Sweden track

| Gate | Requirement |
|------|-------------|
| Visa research | Read [Migrationsverket work permit overview](https://www.migrationsverket.se/English/Private-individuals/Working-in-Sweden.html) |
| Employers | Apply to 10+ roles with sponsorship mention or accredited HR confirmation |
| Quizzes | Pass Linux, Git, Docker, CI/CD, Observability on DevResurge |
| Portfolio | Pipeline demo targeting Azure/AKS stack |
| Language | English interview-ready; basic Swedish phrases for daily life (optional) |
""",
        },
        {
            "slug": "se-visa-sponsor-landscape",
            "title": "Week 1: Work permits & sponsor signals",
            "summary": "How Swedish employer sponsorship works and what to verify before you relocate.",
            "minutes": 14,
            "outcomes": ("Spot legitimate sponsorship offers vs vague promises",),
            "body": """
## Main routes (high level)

**Work permit (arbetstillstånd)** — employer applies after you have a signed
job offer meeting salary and insurance requirements. Processing via
Migrationsverket; timelines vary by nationality and volume.

**EU Blue Card** — for higher qualifications/salary thresholds; path toward
long-term residence for some profiles.

**EU/EEA citizens** — generally no work permit needed (different rules apply).

## What sponsors must typically show

- Job offer matching market salary and role requirements
- Union/opinion process (kollektivavtal context) for many employers
- Insurance and employment terms meeting migration rules
- Genuine need — role shouldn't be fillable instantly locally (varies)

## Red flags in job posts

- "No sponsorship" stated upfront — skip unless you already have work rights
- Vague contractor-only offers without permit clarity
- Salary below Swedish market for the title
- No relocation support mentioned for international hires

## Green flags

- Explicit "we sponsor work permits" or relocation package
- Large established employers (Volvo, Ericsson, Spotify, Klarna, Scania)
- HR/relocation contact in recruiting process
- Written offer before you quit your current job abroad

## Your checklist before accepting

1. Written offer with start date and location
2. Confirmation employer handles permit application
3. Salary in SEK gross/month — compare to market (LinkedIn, Glassdoor, union data)
4. Probation period and notice terms
5. Remote-start possibilities while permit processes (employer-dependent)

## Pair with the **30-day DevOps interview sprint** for deep technical prep.
""",
        },
        {
            "slug": "se-employers-and-stacks",
            "title": "Week 1: Sponsor employers & tech stacks",
            "summary": "Where DevOps roles cluster and which tools appear repeatedly in Sweden.",
            "minutes": 15,
            "outcomes": ("Shortlist 10 target employers matching your stack",),
            "body": """
## Visa-sponsoring employer clusters

**Automotive & industrial (Gothenburg, Skövde)**
Volvo Group, Volvo Cars, Scania, SKF — Azure, AKS, GitHub/Azure DevOps,
strong safety/process culture.

**Telecom & hardware (Stockholm, Lund)**
Ericsson, ARM (Cambridge/Lund ties) — large-scale infra, hybrid cloud,
long release trains.

**Fintech & product (Stockholm)**
Klarna, Spotify, King (Activision), Mojang, iZettle/PayPal — K8s, AWS/GCP
mix, high deployment frequency.

**Retail & enterprise**
IKEA, H&M Group tech, Assa Abloy — Azure-heavy enterprise, internal platforms.

**Consultancies (sponsor but verify project stability)**
Netlight, Semcon, Cyient, global SIs — good for entry to Sweden; ask about
bench time and permit continuity.

## Stack frequency in Swedish DevOps interviews

| Layer | Common tools |
|-------|----------------|
| Cloud | Azure (dominant enterprise), AWS at product cos |
| Orchestration | Kubernetes (AKS), Helm, GitOps |
| CI/CD | Azure DevOps, GitHub Actions, Argo CD |
| IaC | Terraform, Bicep |
| Observability | Grafana, Prometheus, Azure Monitor, Datadog |
| Scripting | Python, Bash, some Go |

## Job search tactics

- LinkedIn with location Stockholm/Gothenburg + "DevOps" + filter company size
- Each company's careers page — many bypass aggregators
- Referrals via DevResurge network or Swedish tech meetups (remote OK pre-move)
- Mention **work permit need early** — saves everyone's time

## Application artifact

Tailor CV to **impact metrics**: deploy frequency, MTTR, cost saved, incidents
prevented. Swedish hiring managers dislike buzzword soup.
""",
        },
        {
            "slug": "se-foundations-interview",
            "title": "Week 1: Linux, Git & networking (interview bar)",
            "summary": "The baseline every Swedish DevOps loop expects — condensed with drill links.",
            "minutes": 14,
            "quiz_slug": "linux-shell",
            "outcomes": ("Pass the linux-shell quiz comfortably",),
            "body": """
## Non-negotiable foundations

Swedish loops rarely skip basics even for senior titles:

**Linux** — processes, logs, permissions, `curl -v`, `dig`, `ss`, disk/debug
**Git** — trunk-based flow, PR reviews, revert/cherry-pick for hotfixes
**Networking** — DNS, TLS, load balancers, 502 vs 504 vs timeout

## Typical phone-screen questions

- Walk through debugging "service unreachable after deploy"
- Explain blue/green vs rolling deploy
- How do you store secrets in Kubernetes?
- Describe your last production incident (STAR format)

## Hands-on minimum before Week 2

Complete on DevResurge:

1. **linux-shell** quiz
2. **git-collaboration** quiz
3. Lessons from **DevOps & SRE** roadmap: `linux-and-networking-ops`, `git-like-a-pro` (foundations)

## 30-minute drill

Write answers (out loud) for:

1. Pod CrashLoopBackOff — first five kubectl commands
2. Pipeline green but prod broken — what differs stage vs prod?
3. Force push to main — why it's unacceptable on a platform team
""",
        },
        {
            "slug": "se-azure-k8s-stack",
            "title": "Week 2: Azure & AKS for Swedish enterprise",
            "summary": "The cloud stack you'll whiteboard at Volvo, Ericsson, and large Nordic employers.",
            "minutes": 16,
            "quiz_slug": "containers-docker",
            "outcomes": ("Map an app to AKS, ACR, Key Vault, and Monitor",),
            "body": """
## Why Azure dominates Swedish enterprise

Microsoft partnership history, hybrid needs, and corporate procurement favor
**Azure** at industrial and legacy enterprise. Product companies may use AWS/GCP
but AKS knowledge still transfers.

## Interview architecture (draw this)

```
Internet → Front Door/App Gateway → AKS Ingress → Service → Pods
                                              ↓
                                         Azure Monitor / Log Analytics
Secrets: Key Vault + Workload Identity
Images: ACR with managed identity pull
```

## AKS topics that come up

- Node pools (system vs user), upgrades, surge during node drain
- Network policies and private clusters
- Pod identity / workload identity to Key Vault
- Horizontal Pod Autoscaler + cluster autoscaler interaction
- Rolling updates and rollback (`kubectl rollout undo`)

## Azure DevOps integration

YAML pipelines building to ACR, deploying manifests via GitOps or `helm upgrade`,
environment approvals for prod, variable groups linked to Key Vault.

## Sample question

*"Design CI/CD for a microservice on AKS with Swedish data residency concerns."*

Discuss: region choice (North Europe / Sweden Central where available), private
endpoints, encryption at rest, audit logging, no secrets in Git, approval gates.
""",
        },
        {
            "slug": "se-cicd-pipeline-interview",
            "title": "Week 2: CI/CD interview answers",
            "summary": "Pipeline design, quality gates, and safe rollouts for regulated Nordic teams.",
            "minutes": 15,
            "quiz_slug": "cicd-devops",
            "outcomes": ("Whiteboard an 8-stage pipeline in under 5 minutes",),
            "body": """
## Pipeline every Swedish enterprise expects

Build once → test → scan → deploy staging → integration → approve → prod → monitor

## Quality gates (automotive/fintech especially)

- Unit + integration tests on every PR
- SAST/SCA and container scanning
- IaC plan review for Terraform changes
- Manual approval only where regulation requires — not for every typo
- Traceability: git SHA on every deployed artifact

## Rollout vocabulary

Know rolling, blue/green, canary, and feature flags — with trade-offs.

## Behavioral tie-in

Swedish teams value **"lagom"** — not too fast to be reckless, not so slow that
competitors win. Tell a story about balancing speed and safety with data
(deploy frequency vs incident rate).

## Weekend lab

Containerize a small API; pipeline on GitHub Actions or Azure DevOps free tier;
deploy to AKS free/simulator or minikube; document rollback in README.
""",
        },
        {
            "slug": "se-terraform-iac",
            "title": "Week 3: Terraform & IaC interviews",
            "summary": "State, modules, drift, and review culture in Swedish platform teams.",
            "minutes": 14,
            "outcomes": ("Explain remote state and blast-radius in a PR review",),
            "body": """
## Terraform interview staples

- Remote state (Azure Storage + locking)
- Modules for AKS, networking, Key Vault
- `plan` in CI on every PR — human review of destroy/changes
- Drift detection and import of legacy resources
- Environment separation via workspaces or directory per env

## Swedish enterprise nuance

Platform teams often serve **many internal product teams**. Interviewers want
hearing about:

- Self-service modules with guardrails (policy-as-code)
- Standard tags for cost allocation
- Change windows for shared infrastructure
- Documentation in English (internal lingua franca)

## Scenario

*"Terraform apply failed halfway — what now?"*

Re-run plan (declarative recovery), never delete state, coordinate locks,
communicate in team channel, fix dependency ordering — no hero `-target` without team OK.
""",
        },
        {
            "slug": "se-observability-incidents",
            "title": "Week 3: Observability, SLOs & incidents",
            "summary": "SLIs, alerting, and blameless postmortems — Nordic on-call expectations.",
            "minutes": 15,
            "quiz_slug": "observability-basics",
            "outcomes": ("Define SLIs for a service and one actionable alert",),
            "body": """
## Observability stack in Sweden

Prometheus/Grafana, Azure Monitor, Application Insights, ELK/OpenSearch,
Datadog at scale-ups. OpenTelemetry adoption growing.

## Interview answers

- SLI → SLO → error budget → release decisions
- Alert on symptom burn, not CPU curiosity
- Structured logs with trace IDs
- Runbooks in English, linked from alerts

## Incident culture

Swedish employers (especially automotive) emphasize **safety metaphors** in
software: mitigate first, transparent comms, systemic fixes in postmortems —
no blame, no hiding.

## STAR story to prepare

Production incident where you rolled back or scaled, communicated status, and
shipped a preventive fix (better alert, automation, runbook).
""",
        },
        {
            "slug": "se-security-compliance",
            "title": "Week 3: DevSecOps & compliance awareness",
            "summary": "Security gates, supply chain, and GDPR/industrial quality context.",
            "minutes": 14,
            "quiz_slug": "security-basics",
            "outcomes": ("Name five security checks in your ideal pipeline",),
            "body": """
## Pipeline security gates

Secret scanning, SAST, dependency CVE gates, container scan, signed images,
IaC policy checks (Checkov/tfsec).

## GDPR & EU data

Swedish/EU employers care about data residency, retention, encryption,
access logging, and DPIAs for new systems — DevOps enables compliance but legal
owns interpretation.

## Automotive/industrial (ISO 26262 / ASPICE awareness)

You don't need certification — show respect for traceability, change control,
and separation of duties between dev and prod deploy.

## Interview question

*"Developer wants to skip security scan to hit a deadline."*

Data-driven answer: show CVE history, MTTR when issues reach prod, propose
parallel scans or risk acceptance process with security sign-off — not silent skip.
""",
        },
        {
            "slug": "se-behavioral-culture",
            "title": "Week 4: Behavioral fit & Swedish work culture",
            "summary": "STAR stories, fika culture, direct feedback, and work-life balance signals.",
            "minutes": 14,
            "outcomes": ("Prepare five STAR stories for Swedish-style interviews",),
            "body": """
## Cultural expectations (generalizations — verify per team)

- **Flat hierarchy** — challenge ideas respectfully; "boss said so" is weak
- **Consensus** — document decisions; async written proposals common
- **Work-life balance** — long hours bragging hurts you; sustainable pace wins
- **Fika** — social coffee breaks; show you're a team human
- **Direct but polite feedback** — receive and give constructively

## Stories to prepare (STAR)

1. Automated painful manual work
2. Disagreement resolved with data
3. Production incident handled calmly
4. Mentored junior or improved docs
5. Learned new stack under deadline

## Questions to ask them

- On-call rotation and compensation?
- Platform team vs embedded DevOps in squads?
- How do you measure reliability (SLOs)?
- Relocation support and permit timeline experience?

## Language

English interviews are standard. Learning basic Swedish helps daily life;
rarely tested for DevOps roles.
""",
        },
        {
            "slug": "se-relocation-practical",
            "title": "Week 4: Relocation & first 90 days",
            "summary": "Personnummer, housing, taxes — practical prep after the offer.",
            "minutes": 12,
            "outcomes": ("Draft a relocation checklist for your move timeline",),
            "body": """
## After signed offer (not legal advice)

1. Employer starts work permit process — stay responsive for document requests
2. Plan housing (Stockholm/Gothenburg competitive — employer relocation help varies)
3. **Personnummer** via Skatteverket — needed for bank, phone, many services
4. Understand gross vs net salary; Swedish taxes fund strong social services
5. Union membership optional but common (Unionen, Akademikerförbund etc.)

## First 90 days on the job

- Learn internal platform docs before proposing rewrites
- Pair with on-call buddy early
- Map stakeholders: security, network, product owners
- Ship one small improvement with measurable impact

## Visa continuity

Understand what happens if role ends — notice period, permit tied to employer,
path to permanent residence over years (rules change — verify officially).

## Keep interviewing skills warm

Even after hire, internal mobility is strong — your DevOps craft keeps compounding.
""",
        },
        {
            "slug": "se-mock-drills-final",
            "title": "Week 4: Mock drills & final checklist",
            "summary": "Timed scenarios and interview-day execution for Swedish loops.",
            "minutes": 14,
            "outcomes": ("Complete two timed mocks and your one-page cheat sheet",),
            "body": """
## Mock 1 — Pipeline on AKS (20 min)

Design CI/CD for Java/Node microservice: PR tests, image to ACR, staging,
approval, canary prod, rollback.

## Mock 2 — Debug (15 min)

502 after deploy: probes, ports, ingress, recent manifest diff.

## Mock 3 — Behavioral (10 min)

"Tell me about improving deployment safety without slowing teams."

## One-page cheat sheet

Pipeline stages | AKS rollback | Key Vault patterns | SLI/SLO | STAR bullets |
Swedish employer research notes

## Interview day

Sleep, test video setup, think aloud, admit gaps honestly, ask good questions.

## You are ready when

- Quizzes passed on DevResurge (Linux, Git, Docker, CI/CD, Observability)
- One demo pipeline in portfolio
- Three polished STAR stories
- Clear list of sponsor employers applied to

> Grattis in advance — Sweden rewards engineers who ship safely and collaborate well.
""",
        },
        {
            "slug": "se-complete-resources",
            "title": "Sweden: complete links & pass checklist",
            "summary": "Immigration, employers, Azure/K8s docs, quizzes, and final gates.",
            "minutes": 16,
            "outcomes": ("Confirm every box before accepting a sponsored offer",),
            "body": """
## Final checklist — Sweden DevOps interviews

- [ ] 13 lessons cleared on this questline
- [ ] Verified employer on careers page + sponsorship in writing
- [ ] [Migrationsverket](https://www.migrationsverket.se/English.html) process understood
- [ ] Salary researched ([Unionen salary info](https://www.unionen.se/rad-och-stod/salary-and-labour-market))
- [ ] Quizzes passed: Linux, Git, Docker, CI/CD, Observability
- [ ] AKS demo project with README rollback section
- [ ] Housing/relocation plan for target city (Stockholm/Gothenburg)
- [ ] Five STAR stories + three technical mocks completed

## Study if any topic below is weak

- [Azure AKS learning path](https://learn.microsoft.com/en-us/training/paths/intro-to-kubernetes-on-azure/)
- [Terraform AzureRM docs](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs)
- [Google SRE books](https://sre.google/books/) — chapters on SLIs and postmortems
""",
        },
    ],
}
