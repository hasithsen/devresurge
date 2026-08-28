ROADMAP = {
    "slug": "devops-interview-australia",
    "title": "30-day DevOps sprint: Australia & visa sponsors",
    "tagline": "Prep for sponsor employers — Atlassian, banks, Canva, AWS-heavy stacks, and Skilled visa routes.",
    "description": (
        "A one-month DevOps interview plan for Australia-focused roles at employers "
        "who sponsor skilled migration visas (482 TSS, 186 ENS, and related paths). "
        "Covers the AU job market, ACS skills assessment signals, technical interviews "
        "at product companies and regulated banks, and the AWS/Kubernetes patterns "
        "common in Sydney and Melbourne."
    ),
    "domain": "devops",
    "level": "intermediate",
    "icon": "🇦🇺",
    "order": 47,
    "audience": (
        "International engineers targeting Australian DevOps/platform roles with "
        "employer nomination and visa sponsorship."
    ),
    "outcomes": (
        "Navigate sponsor job posts and visa pathway vocabulary confidently",
        "Interview well at AU product companies and regulated enterprises",
        "Demonstrate AWS, Kubernetes, and compliance-aware delivery",
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
            "slug": "au-devops-battle-plan",
            "title": "Week 0: Australia sprint battle plan",
            "summary": "Four-week schedule tuned for AU time zones, sponsors, and interview loops.",
            "minutes": 12,
            "outcomes": ("Plan study around applications and skills assessment prep",),
            "body": """
## Why Australia for DevOps

Sydney and Melbourne host global HQs (Atlassian, Canva) and major bank tech
centres. Employers routinely **nominate** overseas candidates for **Temporary
Skill Shortage (482)** and **Employer Nomination Scheme (186)** visas when
local talent is scarce.

## Weekly focus

| Week | Theme |
|------|-------|
| 1 | Visa routes + AU job market + foundations |
| 2 | AWS, EKS/ECS, CI/CD at scale |
| 3 | IaC, security, APRA-aware delivery |
| 4 | Behavioral, mocks, relocation |

## Parallel DevResurge paths

Use **DevOps & SRE** for depth and **30-day DevOps interview sprint** for extra drills.

> Immigration rules change. This is education, not legal advice — verify with a registered migration agent or Home Affairs.

## Pass criteria — Australia track

| Gate | Requirement |
|------|-------------|
| Skills assessment | Start [ACS assessment](https://www.acs.org.au/msa/overview.html) early if required |
| Visa | Confirm role on [skilled occupation list](https://immi.homeaffairs.gov.au/visas/working-in-australia/skill-occupation-list) |
| Quizzes | Pass Linux, Git, Docker, CI/CD, Observability, Security |
| Portfolio | AWS EKS or enterprise pipeline demo with audit trail narrative |
| Employers | 15+ applications to sponsors (product + bank targets) |
""",
        },
        {
            "slug": "au-visa-sponsor-landscape",
            "title": "Week 1: Skilled visas & sponsor signals",
            "summary": "482, 186, skills lists, ACS, and what 'sponsorship available' really means.",
            "minutes": 15,
            "outcomes": ("Verify a role is on a sponsorable occupation list",),
            "body": """
## Common employer-sponsored routes

**482 Temporary Skill Shortage** — employer sponsors you for a role on the
**Skilled Occupation List**; pathways toward permanent residency for some streams.

**186 Employer Nomination Scheme** — permanent residency via employer nomination
(often after 482 or direct for senior roles).

**Skills assessment (ACS)** — many ICT roles need Australian Computer Society
assessment of qualifications + experience before visa application.

## DevOps-relevant occupation titles (verify current lists)

Often lodged under **DevOps Engineer**, **Analyst Programmer**, **Developer
Programmer**, or **ICT Security Specialist** depending on duties — employer and
agent choose the closest match.

## Green flags in job ads

- "Visa sponsorship available" or "482/186"
- Listed on ANZSCO-aligned title with seniority matching your experience
- HR mentions nomination after offer
- Regulated employer with established mobility program (big four banks, telcos)

## Red flags

- "Must have full working rights" with no exception
- Contractor-only ABN roles with no nomination path
- Salary below market for Sydney/Melbourne senior DevOps
- Startup promising PR without written nomination policy

## Your pre-offer checklist

1. Role description matches your CV for ACS if needed
2. Written sponsorship intent from employer
3. Salary meets visa/market bar (Sydney cost of living is high)
4. Location/hybrid policy clear
5. Timeline for skills assessment if not yet done
""",
        },
        {
            "slug": "au-employers-and-stacks",
            "title": "Week 1: Sponsor employers & AU stacks",
            "summary": "Atlassian, banks, telcos, scale-ups — where DevOps roles and AWS dominate.",
            "minutes": 15,
            "outcomes": ("Build a target list of 15 sponsorable AU employers",),
            "body": """
## Major sponsor clusters

**Product & tech (Sydney)**
Atlassian, Canva, Google AU, Amazon AU, Salesforce — high bar, strong AWS/K8s,
system design in loops.

**Banking & finance (Sydney/Melbourne)**
CBA, NAB, ANZ, Westpac, Macquarie — APRA CPS 234, change control, hybrid cloud,
often AWS or private cloud.

**Retail & platforms**
Woolworths, Coles, REA Group, Seek, Afterpay/Block — platform teams, Kubernetes,
GitOps.

**Telco & infra**
Telstra, Optus — large-scale networking + cloud migration programs.

**Consultancies**
Deloitte, Accenture, local SIs — sponsor but clarify bench risk and project continuity.

## Stack patterns

| Sector | Typical stack |
|--------|----------------|
| Product | AWS, EKS, Terraform, GitHub Actions |
| Banks | AWS/Azure, strict IAM, Splunk/Dynatrace, ServiceNow change |
| Scale-ups | AWS/GCP, Datadog, Argo CD |

## Job search

- LinkedIn location Sydney/Melbourne + "sponsorship"
- Careers pages directly — many AU roles never hit aggregators
- Referrals via local meetups (DevOps Sydney, AWS User Groups)

## CV tip for AU

Quantify reliability work: SLOs met, incident reduction, cost optimisation (AUD),
audit findings closed.
""",
        },
        {
            "slug": "au-foundations-interview",
            "title": "Week 1: Foundations interview bar",
            "summary": "Linux, Git, networking — AU loops test basics even at senior bands.",
            "minutes": 14,
            "quiz_slug": "linux-shell",
            "outcomes": ("Pass linux-shell and git-collaboration quizzes",),
            "body": """
## AU interview baseline

Phone screens often include live troubleshooting narratives and pipeline design
before onsite/system design rounds at larger employers.

**Must know:** shell debugging, Git flow, HTTP/TLS, DNS, load balancers,
difference between 4xx/5xx at the edge vs app.

## Bank vs product difference

**Banks** — change windows, CAB approval, segregation of duties, audit trails.
**Product** — velocity, feature flags, experimentation, faster rollbacks.

Tailor stories to the employer type.

## Drills (30 min)

1. Explain last production incident with timeline (STAR)
2. Whiteboard CI/CD for a microservice on AWS
3. How do you rotate secrets without downtime?

Complete DevResurge quizzes: **linux-shell**, **git-collaboration**, **networking-fundamentals**.
""",
        },
        {
            "slug": "au-aws-eks-stack",
            "title": "Week 2: AWS & EKS for Australian employers",
            "summary": "The cloud stack you'll draw in Sydney and Melbourne interviews.",
            "minutes": 16,
            "quiz_slug": "containers-docker",
            "outcomes": ("Explain EKS networking and IAM roles for service accounts",),
            "body": """
## AWS building blocks for DevOps interviews

- **EKS** + Fargate or managed node groups
- **ECR** for images
- **IAM** roles for service accounts (IRSA)
- **Secrets Manager / Parameter Store**
- **CloudWatch** metrics, logs, alarms
- **ALB** + Ingress controller
- **Route 53** DNS
- **Terraform** or CloudFormation

## Architecture whiteboard

```
Route 53 → ALB → EKS Ingress → Service → Pods
                              ↓
                         CloudWatch / X-Ray
Secrets: Secrets Manager via External Secrets Operator
CI: CodePipeline / GitHub Actions → ECR → GitOps deploy
```

## Common questions

- How do you do zero-downtime deploys on EKS?
- Private cluster access for CI runners
- Cost control: spot nodes, rightsizing, idle namespaces
- Multi-AZ failure — what breaks first?

## Regulated employer angle

Mention encryption (KMS), CloudTrail audit, VPC endpoints, no public S3 buckets,
least-privilege IAM — banks love hearing this unprompted.
""",
        },
        {
            "slug": "au-cicd-compliance",
            "title": "Week 2: CI/CD & compliance-aware delivery",
            "summary": "Pipelines that satisfy product speed and bank-grade controls.",
            "minutes": 15,
            "quiz_slug": "cicd-devops",
            "outcomes": ("Design a pipeline with audit trail and approval gates",),
            "body": """
## Pipeline stages (AU enterprise)

PR validation → build artifact → security scan → deploy non-prod → automated
tests → change record (banks) → prod approval → progressive deploy → smoke +
SLO watch

## APRA CPS 234 (awareness for bank roles)

Information security capability, incident reporting, third-party risk — DevOps
implements controls: logging, access reviews, vulnerability management, backup/DR tests.

## Product company pipeline

Feature flags, canary via ALB weighted targets or Argo Rollouts, automated
rollback on error budget burn.

## Interview scenario

*"Security mandates manual prod gate; team wants daily deploys."*

Answer: automate everything before gate, small batches, pre-approved change
templates, metrics proving low incident rate, exception process for emergencies.
""",
        },
        {
            "slug": "au-terraform-iac",
            "title": "Week 3: Terraform on AWS",
            "summary": "Modules, state in S3+DynamoDB, and PR plan reviews.",
            "minutes": 14,
            "outcomes": ("Describe IaC review process for a platform team",),
            "body": """
## Terraform staples in AU interviews

- Remote state S3 + DynamoDB lock
- Modules for VPC, EKS, RDS
- `terraform plan` in CI on every PR
- OIDC federation for GitHub Actions → AWS (no long-lived keys)
- Tagging strategy for cost centres (FinOps matters in AU enterprises)

## Scenario questions

State lock contention, drift from console edits, importing legacy VPC, protecting
prod RDS with `prevent_destroy`.

## Platform team pattern

Golden paths: approved modules only, guardrails with OPA/Sentinel/Checkov,
self-service namespaces on shared EKS.
""",
        },
        {
            "slug": "au-observability-incidents",
            "title": "Week 3: Observability & incident response",
            "summary": "SLOs, paging, and postmortems — AU on-call culture.",
            "minutes": 15,
            "quiz_slug": "observability-basics",
            "outcomes": ("Define error budget policy for a critical service",),
            "body": """
## Tooling landscape

CloudWatch, Prometheus/Grafana, Datadog, New Relic, Splunk in banks, PagerDuty/Opsgenie.

## Interview topics

SLI/SLO/error budget, burn-rate alerts, structured logging, distributed tracing,
runbooks linked from alerts.

## AU timezone reality

Follow-the-sun or local on-call — ask employers explicitly. Fair compensation for
out-of-hours varies (award/enterprise agreements in some employers).

## STAR incident story

Mitigate → communicate → fix → postmortem actions tracked to completion —
mention regulatory notification if applicable (bank context).
""",
        },
        {
            "slug": "au-security-devsecops",
            "title": "Week 3: DevSecOps for regulated AU",
            "summary": "Shift-left security, Essential Eight awareness, container hardening.",
            "minutes": 14,
            "quiz_slug": "security-basics",
            "outcomes": ("Map Essential Eight controls to pipeline stages",),
            "body": """
## Australian Cyber Security Centre — Essential Eight (awareness)

Maturity model many enterprises align to: patching, MFA, macros, application
control, restrict admin, backups, etc. DevOps touches patching automation,
hardening AMIs, backup verification.

## Pipeline gates

Secret scanning, SCA, container scan, IaC scan, signed commits/images where required.

## Interview question

*"Developer wants admin on prod AWS account."*

Least privilege, break-glass process, session logging, time-bound elevation —
never standing admin for apps.
""",
        },
        {
            "slug": "au-behavioral-culture",
            "title": "Week 4: Behavioral & AU workplace culture",
            "summary": "Direct communication, tall poppy awareness, and team fit stories.",
            "minutes": 14,
            "outcomes": ("Prepare five STAR stories for AU panel interviews",),
            "body": """
## Cultural notes

- **Direct but informal** — first names common; still be respectful
- **Tall poppy syndrome** — celebrate team wins; avoid arrogant solo hero narrative
- **Work-life balance** — cricket/footy small talk helps rapport
- **Diversity** — many teams are multicultural; inclusion matters in stories

## Common behavioral prompts

- Conflict with developer about release risk
- Improved deployment frequency safely
- Learned AWS/K8s on the job
- Handled audit finding from missing controls

## Questions to ask

- Sponsorship timeline and costs covered?
- On-call rotation and compensation?
- Cloud roadmap (multi-cloud exit, FinOps)?
- Internal mobility Sydney ↔ Melbourne?
""",
        },
        {
            "slug": "au-relocation-practical",
            "title": "Week 4: Relocation & settling in",
            "summary": "TFN, super, healthcare, housing — after the sponsored offer.",
            "minutes": 12,
            "outcomes": ("Draft a 90-day relocation checklist",),
            "body": """
## After offer (not migration advice)

1. Skills assessment if required (ACS) — start early, it's slow
2. Employer nomination + visa application via agent or in-house mobility
3. **TFN** (tax file number), **superannuation** fund choice
4. Medicare levy surcharge / private health considerations for visa holders
5. Housing — Sydney/Melbourne competitive; negotiate relocation stipend

## First 90 days

Learn change management process before pushing pipeline overhauls. Ship one
visible reliability win. Build relationships with security and network teams.

## Long-term

482 → PR pathways depend on occupation, employer, and policy year — plan with
qualified migration advice.
""",
        },
        {
            "slug": "au-mock-drills-final",
            "title": "Week 4: Mock drills & final checklist",
            "summary": "EKS pipeline design, bank compliance angle, interview day.",
            "minutes": 14,
            "outcomes": ("Complete two timed mocks and cheat sheet",),
            "body": """
## Mock 1 — EKS CI/CD (20 min)

GitHub Actions → ECR → GitOps to EKS with scan gates and prod approval.

## Mock 2 — Bank scenario (15 min)

Deploy during change freeze exception — how do you document, approve, rollback?

## Mock 3 — Troubleshoot (10 min)

Intermittent 504 — ALB idle timeout vs app timeout vs DB pool.

## Cheat sheet

AWS services map | EKS rollback | IRSA | SLI/SLO | ACS/visa status | Target employers

## Ready when

Quizzes passed, one AWS demo project, sponsor list applied, migration agent consult if needed.

Good luck — fair dinkum reliability engineers are in demand down under.
""",
        },
        {
            "slug": "au-complete-resources",
            "title": "Australia: complete links & pass checklist",
            "summary": "482/186, ACS, APRA, AWS/EKS docs, employers, and final gates.",
            "minutes": 16,
            "outcomes": ("Verify readiness before signing a sponsored offer",),
            "body": """
## Final checklist — Australia DevOps interviews

- [ ] 13 lessons cleared
- [ ] ACS outcome received (if required for your pathway)
- [ ] Written sponsorship intent (482 or 186 pathway named)
- [ ] [Home Affairs skilled visas](https://immi.homeaffairs.gov.au/visas/working-in-australia) reviewed
- [ ] Quizzes passed including [Security basics](/quizzes/security-basics/)
- [ ] EKS pipeline demo + change-audit story for bank interviews
- [ ] [Essential Eight](https://www.cyber.gov.au/resources-business-and-government/essential-cyber-security/essential-eight) controls mapped to your pipeline
- [ ] TFN/super/relocation checklist drafted

## Deep dives

- [AWS EKS workshop](https://www.aws.amazon.com/eks/resources/)
- [APRA CPS 234 PDF](https://www.apra.gov.au/sites/default/files/cps-234.pdf)
- [DORA metrics](https://dora.dev/) — cite in behavioral stories
""",
        },
    ],
}
