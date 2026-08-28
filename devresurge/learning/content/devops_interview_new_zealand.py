ROADMAP = {
    "slug": "devops-interview-new-zealand",
    "title": "30-day DevOps sprint: New Zealand & visa sponsors",
    "tagline": "Accredited Employer roles, Xero-scale product cos, and practical AWS/Azure DevOps prep.",
    "description": (
        "A one-month DevOps interview plan for New Zealand employers on the "
        "Accredited Employer Work Visa (AEWV) pathway and Skilled Migrant routes. "
        "Covers Auckland and Wellington tech employers, smaller-team expectations, "
        "and the hands-on cloud skills NZ companies need."
    ),
    "domain": "devops",
    "level": "intermediate",
    "icon": "🇳🇿",
    "order": 48,
    "audience": (
        "Engineers abroad targeting NZ DevOps roles with accredited employer "
        "sponsorship or skilled migration."
    ),
    "outcomes": (
        "Target AEWV-accredited employers and realistic NZ DevOps roles",
        "Interview as a broad platform generalist — common in NZ team sizes",
        "Show AWS/Azure, K8s, and pragmatic automation skills",
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
            "slug": "nz-devops-battle-plan",
            "title": "Week 0: New Zealand sprint battle plan",
            "summary": "Smaller market, high bar for self-sufficiency — how to use four weeks well.",
            "minutes": 12,
            "outcomes": ("Set weekly goals for study and NZ-focused applications",),
            "body": """
## Why New Zealand

Smaller than Australia but strong product exports (Xero, Pushpay, Datacom).
Teams are **lean** — DevOps engineers often wear platform, some SRE, and tooling
hats. Employers on the **Accredited Employer Work Visa** list can hire migrants
when no suitable local candidate exists.

## Market reality

- Auckland = largest tech hub; Wellington = government + SaaS
- Salaries lower than US/Sydney but quality of life high
- Sponsorship exists but **fewer roles** — apply widely, refine fast
- Remote-from-NZ for global cos is possible but visa still needs local employer

## Four-week plan

| Week | Focus |
|------|-------|
| 1 | AEWV + employers + foundations |
| 2 | Cloud (AWS/Azure) + CI/CD |
| 3 | K8s, IaC, security |
| 4 | Culture, mocks, relocation |

> Not immigration advice. Check Immigration New Zealand and licensed advisers for current rules.

## Pass criteria — New Zealand track

| Gate | Requirement |
|------|-------------|
| Accredited employer | Verify on [INZ accredited list](https://www.immigration.govt.nz/employers/accreditation-and-accredited-employers/accredited-employers/) |
| Quizzes | Pass Linux, Git, Docker, CI/CD on DevResurge |
| Portfolio | Public GitHub — app + pipeline + minimal Terraform |
| Generalist proof | One story showing solo on-call / end-to-end ownership |
| Applications | 10+ accredited employers contacted |
""",
        },
        {
            "slug": "nz-visa-sponsor-landscape",
            "title": "Week 1: AEWV & sponsorship basics",
            "summary": "Accredited employers, job checks, and Skilled Migrant context.",
            "minutes": 14,
            "outcomes": ("Confirm an employer is accredited before deep interviewing",),
            "body": """
## Accredited Employer Work Visa (AEWV)

Employers must be **accredited** with Immigration NZ. They advertise, attempt
local recruitment, then can offer migrant candidates meeting skill/salary thresholds.

## Skilled Migrant Category (SMC)

Points-based residence pathway — separate from employer visa but relevant long-term.
DevOps experience + age + qualification points — policies change; verify live criteria.

## Job check signals

- Employer name on accredited list (verify on INZ website)
- Salary at or above median wage thresholds for role band
- Full-time permanent or fixed-term with path explained
- Job description matching ANZSCO DevOps-adjacent titles

## Red flags

- Unaccredited employer promising visa
- Cash-only contracting without visa clarity
- Roles far below your experience "for visa purposes only"

## Practical tip

Ask HR early: *"Are you an accredited employer and has this role passed job check?"*
Legitimate teams answer clearly.
""",
        },
        {
            "slug": "nz-employers-and-stacks",
            "title": "Week 1: NZ employers & stacks",
            "summary": "Xero, Datacom, F&P, government digital — who hires DevOps with sponsorship.",
            "minutes": 14,
            "outcomes": ("Research 10 accredited NZ employers with open platform roles",),
            "body": """
## Sponsor-capable employers (verify accreditation + openings)

**Product & SaaS**
Xero, Pushpay, Orion Health, Vend (Lightspeed), Raygun — AWS/Azure, K8s,
strong engineering culture.

**Services & enterprise**
Datacom, Fisher & Paykel Healthcare, Air New Zealand digital — hybrid infra,
client or internal platforms.

**Government & crown**
Digital.govt.nz ecosystem, IRD, MBIE contractors — security clearance possible,
change control heavy.

**Global with NZ offices**
Amazon, Microsoft, Google (limited headcount) — competitive, still sponsor in some cases.

## NZ stack reality

Smaller teams → you touch **Terraform + CI + K8s + monitoring** in one role.
Less specialization than London or SF; more end-to-end ownership.

| Tool | Frequency |
|------|-----------|
| AWS / Azure | Both common; know one deeply |
| Kubernetes | Growing; managed services preferred |
| Terraform | Standard IaC |
| GitHub Actions | Very common |
| Datadog / CloudWatch | Monitoring |

## Job search

Trade Me Jobs, Seek NZ, LinkedIn (Auckland), company careers pages, NZ tech Slack groups.
""",
        },
        {
            "slug": "nz-foundations-interview",
            "title": "Week 1: Foundations — lean team bar",
            "summary": "Linux, Git, scripting — NZ expects you to debug without a huge platform team.",
            "minutes": 14,
            "quiz_slug": "linux-shell",
            "outcomes": ("Demonstrate self-sufficient debugging in interviews",),
            "body": """
## Generalist expectation

Interviewers often ask: *"You're the only platform person on call — walk us through..."*

Be ready for end-to-end ownership stories: built pipeline, fixed prod, wrote runbook,
trained developers.

## Technical baseline

Shell scripting (Bash/Python), Git, Docker, basic SQL, HTTP debugging, cloud CLI comfort.

## Quizzes to pass

**linux-shell**, **git-collaboration**, **containers-docker** on DevResurge.

## Drill

45-minute scenario: deploy failed Friday 5pm — mitigate, communicate, Monday root cause.
Write timeline as if for postmortem.
""",
        },
        {
            "slug": "nz-cloud-cicd",
            "title": "Week 2: Cloud & CI/CD for NZ teams",
            "summary": "Pragmatic pipelines on AWS or Azure without platform team overhead.",
            "minutes": 15,
            "quiz_slug": "cicd-devops",
            "outcomes": ("Build a simple pipeline README you'd show in an NZ interview",),
            "body": """
## Right-sized CI/CD

NZ employers value **maintainable** over **clever**:

- GitHub Actions or Azure DevOps YAML
- Build → test → scan → deploy to staging → manual prod (early stage) or GitOps (mature)
- Same artifact promoted across envs
- Rollback documented in README

## AWS vs Azure choice

Match the employer's stack in interviews. If unknown, show AWS ECR+EKS or Azure ACR+AKS
fluency — principles transfer.

## Cost consciousness

Smaller companies watch cloud bills — mention FinOps: idle resources, right-sizing,
spot/preemptible where safe, budget alerts.

## Portfolio piece

Public GitHub repo: small API + Dockerfile + pipeline + terraform for one resource group.
NZ hiring managers **do** look at GitHub when CV claims cloud skills.
""",
        },
        {
            "slug": "nz-kubernetes-iac",
            "title": "Week 2–3: Kubernetes & Terraform",
            "summary": "Managed K8s and IaC — the combo NZ scale-ups expect you to run.",
            "minutes": 15,
            "outcomes": ("Explain deploy and rollback on managed Kubernetes",),
            "body": """
## Kubernetes interview topics

Deployments, Services, Ingress, ConfigMaps/Secrets, probes, HPA, namespaces for
env isolation, `kubectl rollout undo`.

## Terraform interview topics

Remote state, modules, plan in CI, never commit secrets, tag resources for cost team.

## NZ scale reality

Many teams run **one** shared cluster with namespace isolation rather than cluster-per-service.
Be ready to discuss multi-tenancy guardrails: NetworkPolicy, ResourceQuota, RBAC.

## Scenario

*"Startup has 3 services, 2 engineers — design minimal platform."*

Answer: managed K8s or even ECS/Fargate, one pipeline template, central logging,
Terraform for VPC+cluster, defer service mesh until pain justifies it.
""",
        },
        {
            "slug": "nz-observability-incidents",
            "title": "Week 3: Observability & on-call in small teams",
            "summary": "When you're pager + platform + sometimes backend support.",
            "minutes": 14,
            "quiz_slug": "observability-basics",
            "outcomes": ("Define minimal viable observability for a small SaaS",),
            "body": """
## MVP observability stack

Metrics (Prometheus/CloudWatch), logs (structured JSON), uptime checks, one dashboard
with golden signals, alerts that page only on user impact.

## Small-team on-call

Escalation paths, runbooks, "wake up only for SLO breach" discipline, blameless
postmortems even with 5 people.

## Interview story

Time you reduced alert noise 50% — NZ teams hate pager fatigue as much as FAANG.

Complete **observability-basics** quiz.
""",
        },
        {
            "slug": "nz-security-basics",
            "title": "Week 3: Security for NZ SaaS & gov-adjacent",
            "summary": "OWASP basics, secrets, NZ Privacy Act awareness.",
            "minutes": 13,
            "outcomes": ("List security controls you'd add in first 90 days",),
            "body": """
## Privacy Act 2020 (awareness)

Personal information handling, breach notification — DevOps enables logging access,
encryption, backup retention policies.

## Practical security

No secrets in Git, MFA on cloud root, least privilege IAM, dependency scanning,
patch automation.

## Gov-adjacent roles

May require NZ citizenship or clearance — read job fine print before investing interview prep.
""",
        },
        {
            "slug": "nz-behavioral-culture",
            "title": "Week 4: Behavioral & Kiwi workplace culture",
            "summary": "Humble competence, teamwork, and honest communication.",
            "minutes": 13,
            "outcomes": ("Prepare STAR stories emphasizing team outcomes",),
            "body": """
## Cultural fit signals

- **Humility** — "we fixed" not "I saved"
- **Practicality** — perfect is enemy of shipped
- **Outdoor/life balance** — sustainable pace is valued
- **Direct honesty** — admit what you don't know

## Questions to ask

- Accredited employer status and visa timeline?
- On-call expectations for platform role?
- Cloud spend ownership — who watches budget?
- Remote/hybrid policy post-visa?

## Stories to prepare

Automated toil, incident handled calmly, learned cloud stack quickly, improved dev self-service.
""",
        },
        {
            "slug": "nz-relocation-practical",
            "title": "Week 4: Relocation & first months in NZ",
            "summary": "IRD, KiwiSaver, housing, and building local network.",
            "minutes": 12,
            "outcomes": ("Draft relocation timeline from offer to arrival",),
            "body": """
## After offer

Visa application with accredited employer support, medical/police certs as required,
housing search (Auckland tight), **IRD** number for tax, **KiwiSaver** decision.

## Community

NZ Tech Podcast, DevOps Auckland meetups, local coffee chats — network accelerates next role if startup folds.

## Realistic expectations

Market is small — role may blend DevOps + sysadmin + security. Flexibility is feature for visa path.
""",
        },
        {
            "slug": "nz-mock-drills-final",
            "title": "Week 4: Mock drills & final checklist",
            "summary": "Generalist scenarios and interview-day prep for NZ loops.",
            "minutes": 14,
            "outcomes": ("Complete mocks and one-page cheat sheet",),
            "body": """
## Mock 1 — Lean platform (20 min)

3 services, 2 engineers — design CI/CD + monitoring + IaC outline.

## Mock 2 — On-call (15 min)

Site down Saturday — your first 10 minutes as solo platform engineer.

## Mock 3 — Visa-aware HR screen (10 min)

Explain why NZ, timeline, accreditation questions you'd ask.

## Ready when

- GitHub demo project live
- Quizzes passed
- 10 accredited employers contacted
- STAR stories polished

Kia kaha — strong generalists who ship reliably are exactly what NZ teams need.
""",
        },
        {
            "slug": "nz-complete-resources",
            "title": "New Zealand: complete links & pass checklist",
            "summary": "AEWV, accredited employers, cloud docs, and final gates.",
            "minutes": 15,
            "outcomes": ("Confirm readiness before relocating to Aotearoa",),
            "body": """
## Final checklist — NZ DevOps interviews

- [ ] 12 lessons cleared
- [ ] Employer verified accredited + job check understood
- [ ] [AEWV overview](https://www.immigration.govt.nz/visas/work/accredited-employer-work-visa/) read
- [ ] GitHub portfolio live with README architecture
- [ ] Quizzes passed (Linux, Git, Docker, CI/CD, Observability)
- [ ] IRD/KiwiSaver/housing plan drafted
- [ ] Technical + behavioral mocks recorded

## Employers to monitor

Check careers pages weekly — NZ market is small; speed matters when roles open.
""",
        },
    ],
}
