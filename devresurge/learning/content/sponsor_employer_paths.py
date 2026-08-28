"""Employer-focused migration sponsor paths — Sweden, Australia, USA."""

from __future__ import annotations

from typing import Any

INTERVIEW_CORE_LINKS = """
- [DevOps interview sprint](/learn/devops-interview/) · [DevSecOps](/learn/devsecops-interview/)
- [Data engineering](/learn/data-eng-interview/) · [Data science](/learn/data-science-interview/)
- [QA / SDET](/learn/qa-interview/) · [Backend](/learn/backend-interview/) · [Cloud](/learn/cloud-interview/)
"""

REGIONAL_LINKS = {
    "sweden": "[🇸🇪 Sweden relocation elective](/learn/relocation-sweden/)",
    "australia": "[🇦🇺 Australia relocation elective](/learn/relocation-australia/)",
    "usa": "[🇺🇸 USA relocation elective](/learn/relocation-usa/)",
}


def _lesson(
    slug: str,
    title: str,
    summary: str,
    body: str,
    *,
    minutes: int = 14,
    quiz_slug: str | None = None,
    outcomes: tuple[str, ...] = (),
) -> dict[str, Any]:
    return {
        "slug": slug,
        "title": title,
        "summary": summary,
        "minutes": minutes,
        "quiz_slug": quiz_slug,
        "outcomes": outcomes,
        "body": body,
    }


def build_sponsor_path_sweden() -> dict[str, Any]:
    return {
        "slug": "sponsor-employers-sweden",
        "title": "Sweden migration sponsors — Volvo, IFS & industrial",
        "tagline": "Visa-sponsoring employers: automotive, enterprise SaaS, telecom, and Nordic product teams.",
        "description": (
            "Deep employer guide for international candidates targeting **Swedish work permits** "
            "at Volvo Group, IFS, Ericsson, Scania, SKF, and similar sponsors. Pair with the "
            "[Sweden relocation elective](/learn/relocation-sweden/) and a core interview sprint."
        ),
        "domain": "relocation",
        "level": "intermediate",
        "icon": "🇸🇪",
        "order": 105,
        "audience": (
            "Engineers pursuing visa-sponsored roles in Sweden at industrial, enterprise, "
            "or product employers."
        ),
        "outcomes": (
            "Shortlist Volvo ecosystem, IFS, and peer sponsors with realistic stack fit",
            "Prepare for enterprise Azure/Kubernetes interviews (distinct from hyperscale loops)",
            "Run a structured application and interview plan in parallel with core sprints",
        ),
        "related_quiz_slugs": (
            "cicd-devops",
            "containers-docker",
            "linux-shell",
            "security-basics",
        ),
        "track": "sponsor",
        "related_roadmap_slugs": (
            "relocation-sweden",
            "devops-interview",
            "devsecops-interview",
        ),
        "elective": True,
        "lessons": [
            _lesson(
                "sp-se-intro",
                "How to use this sponsor path",
                "Volvo, IFS, and peers — paired with regional + core sprints.",
                f"""
## Three layers (run in parallel)

1. **Core interview sprint** — technical depth ([DevOps](/learn/devops-interview/) recommended)
2. **[Sweden relocation elective](/learn/relocation-sweden/)** — visa rules, culture, settling
3. **This sponsor path** — employer-specific stacks, loops, and application tactics

{INTERVIEW_CORE_LINKS}

> Not legal advice. Confirm sponsorship in writing before relocating.
""",
                outcomes=("Link all three layers in your study plan",),
            ),
            _lesson(
                "sp-se-volvo-ecosystem",
                "Volvo ecosystem — Group, Cars, Scania",
                "Automotive/industrial Azure platforms and interview culture.",
                """
## Know the landscape

| Entity | Focus | Typical locations |
|--------|-------|-------------------|
| **Volvo Group** | Trucks, buses, construction, marine | Gothenburg, Lund, global |
| **Volvo Cars** | Passenger vehicles, software-defined car | Gothenburg, Stockholm |
| **Scania** | Heavy vehicles (Volvo Group) | Södertälje, global |

All are large **work-permit sponsors** for senior engineers when local talent is scarce — verify per role on official career pages.

## Tech stack interviewers expect

- **Azure** — AKS, ACR, Key Vault, Monitor, Entra ID
- **CI/CD** — Azure DevOps Pipelines and/or GitHub Actions
- **IaC** — Terraform or Bicep; module boundaries and state discipline
- **Quality culture** — traceability, change control, rollback readiness (safety metaphors matter)

## Interview loop (typical)

1. Recruiter screen — visa need stated early; salary band vs kollektivavtal context
2. Hiring manager — ownership, cross-team collaboration
3. Technical — pipeline design, K8s troubleshooting, Azure architecture (whiteboard)
4. Behavioral — STAR with **safety, quality, transparency** themes
5. Panel or team fit — flat hierarchy; respectful challenge is welcome

## Different from hyperscale loops

Less algorithm trivia; more **judgment, Azure delivery, and operational maturity**.
Use [DevOps interview sprint](/learn/devops-interview/) for SRE fundamentals; use this lesson for **enterprise framing**.

## Application tactics

- Search official career portals + "work permit" / "relocation support" in posts
- Highlight measurable pipeline, reliability, and incident outcomes
- Ask: team stack, on-call, hybrid policy, visa timeline and costs covered
""",
                quiz_slug="cicd-devops",
                outcomes=("Explain Volvo-style enterprise DevOps stack in 3 minutes",),
            ),
            _lesson(
                "sp-se-ifs-platform",
                "IFS — global enterprise cloud platform",
                "ERP/EAM/FSM SaaS, multi-cloud delivery, Lund HQ and global hubs.",
                """
## What IFS builds

**IFS** (HQ Lund, Sweden) delivers enterprise cloud software — ERP, field service (FSM),
asset management (EAM) — to global customers. Platform engineering spans **multi-cloud**
operations, secure SaaS delivery, and regulated enterprise customers.

## Why IFS sponsors international talent

Global product growth + cloud platform expansion → recurring need for platform, DevOps,
SRE, and security engineers. Roles often list English as working language.

## Stack signals (verify per team)

- **Cloud** — AWS and Azure patterns for IFS Cloud; Kubernetes for services
- **CI/CD** — automated test/scan/deploy pipelines; environment promotion
- **Observability** — metrics, logs, traces for multi-tenant SaaS
- **Security** — ISO/SOC-style controls; tenant isolation; supply-chain scanning

## Interview themes

- SaaS reliability and **tenant isolation**
- Pipeline gates without killing release cadence
- Incident response with enterprise customers watching status pages
- Collaboration with dev, QA, and support at enterprise pace

## Locations

- **Sweden** — Lund (HQ), Linköping, Stockholm-area roles
- Also see [Australia](/learn/sponsor-employers-australia/) and [USA](/learn/sponsor-employers-usa/) IFS modules if flexible on region

## Prep pairing

[DevSecOps sprint](/learn/devsecops-interview/) + this lesson if role emphasizes pipeline security.
""",
                outcomes=("Describe SaaS platform DevOps concerns vs single-product startup",),
            ),
            _lesson(
                "sp-se-industrial-peers",
                "Ericsson, SKF, Atlas Copco & industrial peers",
                "Telecom and industrial sponsors beyond automotive.",
                """
## Additional Swedish sponsors (verify openings)

| Employer | Domain | Stack signals |
|----------|--------|---------------|
| **Ericsson** | Telecom infrastructure | Cloud-native, K8s, large-scale automation |
| **SKF** | Industrial bearings | Azure, IoT, manufacturing IT/OT bridge |
| **Atlas Copco** | Industrial equipment | Global IT, automation, hybrid cloud |
| **Sandvik** | Mining/industrial tools | Enterprise cloud, security, global ops |
| **AstraZeneca** | Pharma | Regulated GxP environments, validation culture |

## Product & fintech (also sponsor)

Spotify, Klarna, King, Mojang, Einride — faster product cadence; still verify visa per role.
Pair product companies with hyperscale-style prep from the core DevOps sprint.

## Choosing your lane

| Lane | Interview flavor | Core sprint emphasis |
|------|------------------|----------------------|
| Industrial / automotive | Azure, quality, safety | Enterprise answers + this path |
| Enterprise SaaS (IFS) | SaaS ops, compliance | DevSecOps + platform depth |
| Product | Higher velocity, product metrics | Full DevOps sprint + system design |

Shortlist **10 employers**; track sponsorship mention, stack, city, and application date.
""",
                outcomes=("Build a tiered employer list with stack match scores",),
            ),
            _lesson(
                "sp-se-enterprise-interviews",
                "Enterprise DevOps interviews in Sweden",
                "Azure/K8s loops, behavioral tone, and mock scenarios.",
                """
## Technical scenarios (practice aloud)

1. Design CI/CD for microservices on **AKS** with scan gates and manual prod approval
2. Debug **502** after Ingress change — probes, backend pool, TLS
3. **Terraform** state lock during incident — coordination and safe recovery
4. **Post-deploy** error budget burn — rollback decision in 10 minutes

## Behavioral tone (Sweden)

- Flat hierarchy — disagree with ideas, not people
- Consensus and written follow-ups after meetings
- **Lagom** — sustainable pace; no hero-on-call glorification
- English interviews common; Swedish helps daily life

## Mock week (before onsite)

| Day | Activity |
|-----|----------|
| Mon | Pipeline whiteboard + record 15 min |
| Tue | kubectl debug scenario on kind/AKS lab |
| Wed | Terraform plan review PR exercise |
| Thu | 3 STAR stories with safety/quality angle |
| Fri | Full 60-min mock: tech + behavioral |

Pass [Containers](/quizzes/containers-docker/) and [CI/CD](/quizzes/cicd-devops/) quizzes.
""",
                outcomes=("Complete one recorded enterprise mock interview",),
            ),
            _lesson(
                "sp-se-checklist",
                "Sweden sponsor path — complete checklist",
                "Gates before you sign or relocate.",
                """
- [ ] [Sweden relocation elective](/learn/relocation-sweden/) in progress or complete
- [ ] Core interview sprint Week 2+ complete
- [ ] Volvo / IFS / peer employer list with sponsorship verified
- [ ] Enterprise Azure + K8s mock completed
- [ ] Five STAR stories adapted to Nordic tone
- [ ] Work-permit route confirmed with employer HR (official Migrationsverket links)
- [ ] Salary meets visa maintenance requirements + market band
""",
                minutes=12,
                outcomes=("All gates green before accepting offer",),
            ),
        ],
    }


def build_sponsor_path_australia() -> dict[str, Any]:
    return {
        "slug": "sponsor-employers-australia",
        "title": "Australia migration sponsors — IFS, banks & product",
        "tagline": "482/186 sponsors: enterprise SaaS, Atlassian-scale product, and regulated banks.",
        "description": (
            "Employer guide for **Skilled Migration** routes in Australia — IFS, Atlassian, "
            "major banks, Canva, Telstra, and other documented sponsors. Pair with "
            "[Australia relocation elective](/learn/relocation-australia/)."
        ),
        "domain": "relocation",
        "level": "intermediate",
        "icon": "🇦🇺",
        "order": 106,
        "audience": "International engineers targeting employer-sponsored roles in Australia.",
        "outcomes": (
            "Target IFS, product, and regulated employers with correct visa framing",
            "Prepare for AWS-heavy enterprise and bank compliance interviews",
            "Align ACS skills assessment and occupation lists with your role title",
        ),
        "related_quiz_slugs": (
            "cicd-devops",
            "networking-fundamentals",
            "security-basics",
        ),
        "track": "sponsor",
        "related_roadmap_slugs": (
            "relocation-australia",
            "devops-interview",
            "devsecops-interview",
        ),
        "elective": True,
        "lessons": [
            _lesson(
                "sp-au-intro",
                "How to use this sponsor path",
                "IFS, product cos, and banks — with 482/186 context.",
                f"""
## Parallel study plan

1. Core sprint — [DevOps interview](/learn/devops-interview/) or your discipline
2. [Australia relocation elective](/learn/relocation-australia/) — 482/186, ACS, culture
3. **This path** — sponsor employers and AU-specific interview bars

{INTERVIEW_CORE_LINKS}

Confirm **Skilled Occupation List** alignment and ACS assessment timing early for ICT roles.
""",
                outcomes=("Map visa, ACS, and employer outreach timeline",),
            ),
            _lesson(
                "sp-au-ifs-platform",
                "IFS in Australia",
                "Enterprise cloud platform roles — Sydney, Melbourne, remote-hybrid.",
                """
## IFS in AU

IFS maintains Australian presence supporting APAC customers and global platform delivery.
Platform/DevOps roles may sit in **Sydney**, **Melbourne**, or hybrid arrangements — verify on [IFS careers](https://www.ifs.com/about/careers).

## Interview focus

- Multi-tenant SaaS on AWS (common AU enterprise pattern)
- Change management with enterprise customers
- Observability and incident comms across time zones (APAC + EU/US follow-the-sun)
- Security aligned to customer audit requests

## Visa note

Employer must be willing to **nominate** for 482 TSS or 186 ENS where eligible — ask HR explicitly before deep interview loops.
""",
                outcomes=("Tailor CV to SaaS platform reliability metrics",),
            ),
            _lesson(
                "sp-au-product-sponsors",
                "Atlassian, Canva, REA & product sponsors",
                "High-growth product companies with skilled visa history.",
                """
## Product-tier sponsors (verify per role)

| Employer | Notes |
|----------|-------|
| **Atlassian** | Sydney HQ culture; AWS/K8s at scale; strong engineering bar |
| **Canva** | Sydney; product velocity; platform and security hiring |
| **REA Group** | Melbourne; property tech; mature platform teams |
| **WiseTech / TechnologyOne** | Enterprise software; AU HQ/global |

## Interview bar

Closer to **top-tier product** loops — pair [DevOps interview sprint](/learn/devops-interview/) heavily.
System design and ownership stories matter as much as pipeline craft.

## ACS & title alignment

Job title and duties must match **ANZSCO** occupation for skills assessment — align DevOps/SRE/platform wording consistently across CV, LinkedIn, and ACS application.
""",
                outcomes=("Split targets: product-tier vs enterprise-tier lists",),
            ),
            _lesson(
                "sp-au-banks-regulated",
                "Big banks & regulated employers",
                "CBA, NAB, Westpac, Macquarie — CPS 234 and change advisory.",
                """
## Regulated sponsors

Major banks and insurers sponsor **482/186** for senior platform roles when skills are scarce — competition is high; referrals help.

## Compliance awareness (not lawyer advice)

- **APRA CPS 234** — information security expectations
- **Essential Eight** maturity — patch, MFA, backups, logging
- **Change advisory** — CAB, evidence trails, segregation of duties

## Interview flavor

- Audit-friendly CI/CD: who approved, what tested, rollback evidence
- On-call and **follow-the-sun** handoffs — ask compensation policy
- Less "move fast break things"; more **controlled velocity**

[DevSecOps sprint](/learn/devsecops-interview/) pairs well with bank platform roles.
""",
                quiz_slug="security-basics",
                outcomes=("Explain one pipeline control mapping to CPS 234 themes",),
            ),
            _lesson(
                "sp-au-other-sponsors",
                "Telstra, Woolworths, gov digital & more",
                "Telecom, retail tech, and public-sector digital sponsors.",
                """
## Additional sponsor categories

| Sector | Examples | Signals |
|--------|----------|---------|
| Telecom | Telstra, Optus | Large hybrid cloud, legacy + cloud native |
| Retail | Woolworths, Coles tech | Scale peaks, cost-aware reliability |
| Gov digital | State/federal digital agencies | IRAP, ISM, slower change, strong docs |
| Consulting | Accenture, Deloitte (verify) | Client delivery; clarify visa sponsor entity |

## Job search

- Official careers sites + "visa sponsorship" + "482"
- Avoid roles stating **Australian citizenship/PR only** unless they confirm exceptions
- Track: sponsor name on offer (nomination entity must match)

## Other global enterprise

**Volvo Group** AU operations exist but smaller than SE — Sweden path may be better for automotive focus.
**IFS** covered in prior lesson; also consider SAP, Oracle AU platform roles with sponsor history.
""",
                outcomes=("Contact 15+ employers with documented sponsor patterns",),
            ),
            _lesson(
                "sp-au-checklist",
                "Australia sponsor path — complete checklist",
                "ACS, nomination, and interview gates.",
                """
- [ ] [Australia relocation elective](/learn/relocation-australia/) complete
- [ ] ACS skills assessment submitted or timed (if required)
- [ ] Occupation code matches role duties
- [ ] IFS + product + bank tier lists active
- [ ] Enterprise + product mock interviews recorded
- [ ] 482/186 pathway confirmed with HR before relocating
""",
                minutes=12,
                outcomes=("Clear gates before visa nomination",),
            ),
        ],
    }


def build_sponsor_path_usa() -> dict[str, Any]:
    return {
        "slug": "sponsor-employers-usa",
        "title": "USA migration sponsors — IFS, enterprise & Tier-1",
        "tagline": "H-1B, O-1, and enterprise sponsors — IFS, hyperscale, and global SaaS.",
        "description": (
            "Employer and visa strategy for the **United States** — IFS North America, "
            "Tier-1 tech sponsors, enterprise SaaS, and realistic H-1B planning. Pair with "
            "[USA relocation elective](/learn/relocation-usa/)."
        ),
        "domain": "relocation",
        "level": "intermediate",
        "icon": "🇺🇸",
        "order": 107,
        "audience": "International engineers pursuing US work visa sponsorship.",
        "outcomes": (
            "Build a tiered sponsor list including IFS and enterprise with H-1B history",
            "Choose prep depth: hyperscale core sprint vs enterprise sponsor modules",
            "Plan H-1B timing, O-1 backup, and offer negotiation basics",
        ),
        "related_quiz_slugs": (
            "cicd-devops",
            "system-design-basics",
            "security-basics",
        ),
        "track": "sponsor",
        "related_roadmap_slugs": (
            "relocation-usa",
            "devops-interview",
            "devsecops-interview",
        ),
        "elective": True,
        "lessons": [
            _lesson(
                "sp-us-intro",
                "How to use this sponsor path",
                "Visa tiers, IFS, enterprise, and when to run the hyperscale sprint.",
                f"""
## Two prep tracks (pick primary + backup)

| Target | Prep emphasis |
|--------|----------------|
| **Tier-1 product** (Meta, Google, Amazon, etc.) | [DevOps interview sprint](/learn/devops-interview/) — full depth |
| **Enterprise SaaS** (IFS, Oracle, SAP, ServiceNow) | This path + DevSecOps/platform modules |
| **Industrial US arms** (Volvo Group NA, Ericsson US) | Enterprise Azure + this path |

Always run [USA relocation elective](/learn/relocation-usa/) for H-1B/O-1 mechanics.

{INTERVIEW_CORE_LINKS}
""",
                outcomes=("Pick primary visa strategy and prep track",),
            ),
            _lesson(
                "sp-us-ifs-platform",
                "IFS North America",
                "Enterprise cloud platform — US hubs and SaaS operations.",
                """
## IFS in the USA

IFS operates North American offices supporting sales, services, and **platform engineering**
for IFS Cloud. Search US platform/DevOps/SRE titles on official careers.

## Technical bar

- AWS/EKS-style platform patterns (team-dependent)
- Enterprise change windows and customer communication
- Security questionnaires from Fortune 500 customers
- Global collaboration with Lund HQ and APAC teams

## Visa

IFS has sponsored **H-1B** roles in public filings — verify for **your specific requisition**.
Cap-subject vs cap-exempt does not apply to most private employers — plan for **lottery timing**.

## Interview prep

Less pure algorithm focus than Tier-1; strong **system design + delivery + behavioral** depth.
Prepare SaaS incident and pipeline stories with customer impact metrics.
""",
                outcomes=("Prepare 2 IFS-aligned platform stories with metrics",),
            ),
            _lesson(
                "sp-us-volvo-industrial",
                "Volvo Group & industrial US operations",
                "North American automotive/industrial Azure delivery.",
                """
## Volvo in the USA

**Volvo Group** (trucks, buses, powertrain) and **Volvo Cars** (US operations) hire platform
and DevOps engineers — often aligned with **global Azure/AKS** standards from Sweden.

## When to prioritize this lesson

- Targeting **Gothenburg/Lund** but open to US internal transfer later, OR
- Applying directly to US Volvo/industrial roles with sponsorship

## Stack & culture

Same enterprise themes as [Sweden Volvo module](/learn/sponsor-employers-sweden/) — safety,
quality, traceability — adapted to US labor and on-call norms.

## Peer industrial sponsors

Caterpillar tech, John Deere IT, Siemens USA, Bosch — enterprise cloud; verify H-1B history on USCIS data hub.
""",
                outcomes=("Link US industrial role to global enterprise stack story",),
            ),
            _lesson(
                "sp-us-tier1-hyperscale",
                "Tier-1 tech sponsors (H-1B)",
                "Amazon, Google, Microsoft, Meta — lottery, bar, and prep routing.",
                """
## Tier-1 sponsors

Public H-1B filers with platform orgs: **Amazon**, **Google**, **Microsoft**, **Meta**, **Apple**, **Netflix**, etc.

## Prep routing

Use the full **[DevOps interview sprint](/learn/devops-interview/)** — error budgets, large-scale K8s,
infra system design, scripting rounds. This sponsor path is **supplemental**, not substitute.

## H-1B reality

- Bachelor's + specialty occupation match required
- Lottery registration window — multiple offers increase options but not guarantees
- Cap-exempt: universities and affiliated nonprofits (rare for DevOps)

## O-1 / L-1

Strong publication, talks, or critical role history? Explore **O-1** with immigration counsel.
**L-1** if transferring from same employer abroad (e.g. IFS Sweden → IFS US after 12 months).
""",
                quiz_slug="system-design-basics",
                outcomes=("Register H-1B timeline milestones on calendar",),
            ),
            _lesson(
                "sp-us-enterprise-sponsors",
                "Enterprise SaaS & services sponsors",
                "Oracle, SAP, ServiceNow, Accenture (verify entity), and mid-cap SaaS.",
                """
## Enterprise tier

| Type | Examples | Interview flavor |
|------|----------|------------------|
| Enterprise SaaS | Oracle, SAP, ServiceNow, Workday | Platform + compliance + customer SLAs |
| Cloud providers | AWS, Azure, GCP (professional services vs FTE) | Clarify org — bar varies wildly |
| Consulting | Big 4 / SI — **verify sponsor entity** | Client bench vs internal platform |

## IFS positioning

IFS sits between **product velocity** and **enterprise compliance** — emphasize multi-tenant ops,
release trains, and audit-friendly pipelines in interviews.

## Red flags

- Third-party staffing without direct employer sponsorship
- "We sponsor after 6 months probation" without written policy
- Title inflation without matching SOC/specialty occupation duties
""",
                outcomes=("Verify H-1B employer history for top 10 targets",),
            ),
            _lesson(
                "sp-us-checklist",
                "USA sponsor path — complete checklist",
                "H-1B, mocks, and offer gates.",
                """
- [ ] [USA relocation elective](/learn/relocation-usa/) complete
- [ ] Primary track chosen: Tier-1 vs enterprise (IFS/industrial)
- [ ] [DevOps interview sprint](/learn/devops-interview/) Week 3+ if Tier-1
- [ ] IFS / enterprise stories with customer-impact metrics
- [ ] H-1B registration / lottery plan documented
- [ ] Immigration counsel engaged before signing (recommended)
- [ ] Total comp understood: base, RSU, signing, relocation
""",
                minutes=12,
                outcomes=("Green gates before accepting US offer",),
            ),
        ],
    }


SPONSOR_ROADMAPS: tuple[dict[str, Any], ...] = (
    build_sponsor_path_sweden(),
    build_sponsor_path_australia(),
    build_sponsor_path_usa(),
)
