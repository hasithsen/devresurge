"""Generate merged interview cores + shared regional elective packs."""

from __future__ import annotations

from typing import Any

RELOCATION_REGIONS: dict[str, dict[str, Any]] = {
    "sweden": {
        "slug": "relocation-sweden",
        "code": "se",
        "flag": "🇸🇪",
        "title": "Sweden relocation & visa elective",
        "order": 100,
        "visa_ref": "visa_sweden",
        "employers_ref": "employers_sweden",
    },
    "australia": {
        "slug": "relocation-australia",
        "code": "au",
        "flag": "🇦🇺",
        "title": "Australia relocation & visa elective",
        "order": 101,
        "visa_ref": "visa_australia",
        "employers_ref": "employers_australia",
    },
    "new-zealand": {
        "slug": "relocation-new-zealand",
        "code": "nz",
        "flag": "🇳🇿",
        "title": "New Zealand relocation & visa elective",
        "order": 102,
        "visa_ref": "visa_nz",
        "employers_ref": "employers_nz",
    },
    "usa": {
        "slug": "relocation-usa",
        "code": "us",
        "flag": "🇺🇸",
        "title": "USA relocation & visa elective",
        "order": 103,
        "visa_ref": "visa_usa",
        "employers_ref": "employers_usa",
    },
    "uk": {
        "slug": "relocation-uk",
        "code": "uk",
        "flag": "🇬🇧",
        "title": "UK relocation & visa elective",
        "order": 104,
        "visa_ref": "visa_uk",
        "employers_ref": "employers_uk",
    },
}

RELOCATION_SLUGS: tuple[str, ...] = tuple(r["slug"] for r in RELOCATION_REGIONS.values())

INTERVIEW_CORE_SLUGS: tuple[str, ...] = (
    "devops-interview",
    "devsecops-interview",
    "data-eng-interview",
    "data-science-interview",
    "qa-interview",
    "backend-interview",
    "cloud-interview",
)

DATA_FUNDAMENTALS_SLUG = "data-fundamentals-elective"

ROLES: dict[str, dict[str, Any]] = {
    "data-eng": {
        "slug": "data-eng-interview",
        "slug_short": "de",
        "title": "Data engineering interview sprint",
        "domain": "data",
        "icon": "📊",
        "order": 60,
        "level": "intermediate",
        "tagline": "Pipelines, warehouses, Spark, dbt, and data quality — interview-ready in 30 days.",
        "description": (
            "Universal data engineering interview prep: SQL, modeling, batch/stream pipelines, "
            "quality, and cloud warehouses. Pair with the "
            "[Data fundamentals elective](/learn/data-fundamentals-elective/) if you need a "
            "structured SQL/Python refresh, and a **regional elective** for visa sponsorship "
            "guidance."
        ),
        "audience": "Engineers targeting data platform, analytics, or DE roles globally.",
        "outcomes": (
            "Design batch and streaming pipelines with clear SLAs",
            "Answer SQL, modeling, and data quality interview questions",
            "Discuss Spark, Airflow/dbt, and warehouse trade-offs confidently",
        ),
        "quizzes": (
            "sql-fundamentals",
            "databases-internals",
            "python-fundamentals",
            "testing-fundamentals",
        ),
        "portfolio": "End-to-end pipeline: ingest → transform (dbt/Spark) → tests → metrics",
    },
    "data-science": {
        "slug": "data-science-interview",
        "slug_short": "ds",
        "title": "Data science interview sprint",
        "domain": "data",
        "icon": "🔬",
        "order": 61,
        "level": "intermediate",
        "tagline": "Statistics, ML, experimentation, and impact storytelling — interview-ready in 30 days.",
        "description": (
            "Universal data **science** interview prep: probability, SQL, feature engineering, "
            "supervised/unsupervised ML, A/B testing, and production ML basics. Pairs with the "
            "[Data engineering sprint](/learn/data-eng-interview/) and optional "
            "[Data fundamentals elective](/learn/data-fundamentals-elective/)."
        ),
        "audience": "Data scientists, ML engineers, and analysts moving into product DS roles.",
        "outcomes": (
            "Explain ML metrics, bias-variance, and model selection trade-offs",
            "Design experiments and interpret A/B test results without p-hacking",
            "Communicate business impact with clear metrics and stakeholder stories",
        ),
        "quizzes": (
            "sql-fundamentals",
            "python-fundamentals",
            "data-structures",
            "algorithms-patterns",
        ),
        "portfolio": "Notebook or repo: problem → EDA → model → metrics → deployment or API sketch",
    },
    "devsecops": {
        "slug": "devsecops-interview",
        "slug_short": "dso",
        "title": "DevSecOps interview sprint",
        "domain": "security",
        "icon": "🛡",
        "order": 46,
        "level": "intermediate",
        "tagline": "Shift-left security, supply chain, cloud hardening, and compliance — 30 days.",
        "description": (
            "Universal DevSecOps interview prep: pipeline security gates, SAST/SCA, container "
            "and cloud hardening, IAM, compliance awareness, and collaboration with DevOps/SRE. "
            "Pair with [DevOps interview sprint](/learn/devops-interview/) for delivery depth."
        ),
        "audience": "Security-minded engineers, AppSec champions, and platform security roles.",
        "outcomes": (
            "Design CI/CD pipelines with proportional security gates",
            "Explain supply-chain controls: SBOM, signing, secret scanning",
            "Threat-model a service and map controls to SOC2/GDPR-style requirements",
        ),
        "quizzes": (
            "security-basics",
            "cicd-devops",
            "containers-docker",
            "linux-shell",
        ),
        "portfolio": "Pipeline YAML with scan gates + threat model doc + hardened Dockerfile",
    },
    "qa": {
        "slug": "qa-interview",
        "slug_short": "qa",
        "title": "QA / SDET interview sprint",
        "domain": "qa",
        "icon": "🧪",
        "order": 70,
        "level": "intermediate",
        "tagline": "Test design, automation, CI gates, and quality leadership — 30 days.",
        "description": (
            "Universal QA and SDET interview prep: test plans, API/UI automation, CI strategy, "
            "and behavioral stories. Add a **regional elective** for visa-specific employer and "
            "culture guidance."
        ),
        "audience": "QA engineers and SDET candidates interviewing globally.",
        "outcomes": (
            "Design risk-based test plans and automation strategy",
            "Build API and UI automation with CI integration",
            "Explain flaky-test triage and release quality gates",
        ),
        "quizzes": (
            "testing-fundamentals",
            "cicd-devops",
            "http-apis",
            "python-fundamentals",
        ),
        "portfolio": "Test repo: API + UI suites, CI YAML, flake-handling doc",
    },
    "backend": {
        "slug": "backend-interview",
        "slug_short": "be",
        "title": "Backend engineering interview sprint",
        "domain": "backend",
        "icon": "⚡",
        "order": 80,
        "level": "intermediate",
        "tagline": "APIs, SQL, caching, messaging, and system design — 30 days.",
        "description": (
            "Universal backend interview prep: REST, databases, caching, operability, and design "
            "rounds. Select a **regional elective** when targeting sponsored roles abroad."
        ),
        "audience": "Backend and API engineers preparing for product and enterprise loops.",
        "outcomes": (
            "Design APIs with auth, pagination, and clear error contracts",
            "Reason about SQL, indexes, and consistency under load",
            "Whiteboard backend services with scaling and failure modes",
        ),
        "quizzes": (
            "http-apis",
            "sql-fundamentals",
            "django-basics",
            "system-design-basics",
            "security-basics",
        ),
        "portfolio": "API with auth, tests, migrations, OpenAPI, deploy/rollback README",
    },
    "cloud": {
        "slug": "cloud-interview",
        "slug_short": "ce",
        "title": "Cloud engineering interview sprint",
        "domain": "cloud",
        "icon": "☁",
        "order": 90,
        "level": "intermediate",
        "tagline": "Landing zones, IaC, networking, DR, and migration — 30 days.",
        "description": (
            "Universal cloud architect/engineer interview prep: multi-account design, Terraform, "
            "IAM, FinOps, and migration. Add a **regional elective** for visa sponsors in your "
            "target market."
        ),
        "audience": "Cloud platform and infrastructure engineers interviewing globally.",
        "outcomes": (
            "Design landing zones with least privilege and guardrails",
            "Explain Terraform workflows and Well-Architected trade-offs",
            "Present migration and DR plans with RTO/RPO reasoning",
        ),
        "quizzes": (
            "cicd-devops",
            "networking-fundamentals",
            "security-basics",
            "linux-shell",
        ),
        "portfolio": "Terraform modules + architecture diagram + blast-radius notes",
    },
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


def _role_core_content(role_key: str) -> dict[str, str]:
    if role_key == "data-eng":
        return {
            "foundations": """## Shared data foundations (DE + DS)

SQL, Python, and data intuition — both data engineering and data science loops test these.

- JOINs, window functions (`ROW_NUMBER`, `LAG`), aggregations, subqueries
- Python: pandas basics, reading/writing data, pytest for transforms
- Explain a metric definition before debating tools

**Optional:** complete [Data fundamentals elective](/learn/data-fundamentals-elective/) if rusty.

**Role clarity:** DE owns **reliable data movement and modeling**; DS owns **inference and decisions from data**. Many teams blur the line — show both craft and judgment.

Pass [SQL fundamentals](/quizzes/sql-fundamentals/) and [Python fundamentals](/quizzes/python-fundamentals/).
Also explore [Data science sprint](/learn/data-science-interview/) if your target role is model-heavy.
""",
            "core1": """## Data modeling & warehousing

- **Medallion:** bronze (raw) → silver (cleaned) → gold (business-ready)
- **Star schema:** fact table grain, dimensions, surrogate keys
- **SCD Type 1 vs 2** — when history matters for analytics
- **Grain statement:** "One row per order line per day" — say it in every design answer

## Interview prompt

*"Design analytics schema for e-commerce orders with returns."*

State grain, fact/dimension split, and one SCD decision with trade-offs.
""",
            "core2": """## Batch pipelines & orchestration

- **Extract:** full vs incremental (watermark, CDC)
- **Orchestration:** Airflow/Prefect/Dagster — retries, SLAs, alerting
- **dbt:** models, tests, docs, incremental materializations
- **Idempotent backfills** — re-run without double-counting

## Answer spine

Source → land raw → transform → publish marts → monitor freshness.
""",
            "core3": """## Streaming & CDC

- Kafka: topics, partitions, consumer groups, offsets
- **At-least-once** processing + idempotent sinks
- CDC (Debezium) → stream processing → warehouse
- **Late data:** watermarks, allowed lateness

When streaming vs batch: latency needs vs cost/complexity.
""",
            "core4": """## Data quality & observability

- dbt tests, Great Expectations, custom SQL checks
- **Freshness SLAs** and volume anomaly alerts
- Lineage (dbt docs, OpenLineage, DataHub awareness)
- Incident: "CEO metric wrong" → pipeline runs → row counts → schema drift → reprocess

Pair with [Databases deep](/learn/databases-deep/) for SQL internals.
""",
            "core5": """## Cloud warehouses & lakehouse

| Platform | Interview talking points |
|----------|-------------------------|
| Snowflake | Virtual warehouses, micro-partitions, stages |
| BigQuery | Partitioning, slots, nested/repeated fields |
| Databricks | Delta Lake, Unity Catalog, Spark integration |
| Redshift/Synapse | Distribution keys, workload management |

Know one stack deeply; compare cost, ops burden, and lock-in for others.
""",
        }
    if role_key == "data-science":
        return {
            "foundations": """## Shared data foundations (DE + DS)

Statistics, SQL, and Python — every DS loop tests literacy here before ML depth.

- Descriptive stats, distributions, correlation vs causation
- SQL for feature extraction and cohort analysis
- Python: pandas, numpy, sklearn basics, readable notebooks

**Optional:** [Data fundamentals elective](/learn/data-fundamentals-elective/) for structured refresh.

**Pair with DE sprint** if the role builds features/pipelines: [Data engineering](/learn/data-eng-interview/).

Pass [SQL](/quizzes/sql-fundamentals/) and [Python](/quizzes/python-fundamentals/) quizzes; [Data structures](/quizzes/data-structures/) for coding rounds.
""",
            "core1": """## Statistics & probability for interviews

- Mean/median, variance, confidence intervals (interpret, don't memorize formulas only)
- **Bias-variance trade-off** — under/overfitting in plain language
- Common distributions (normal, binomial, Poisson) — when they apply
- **Base rate fallacy** — show up in case questions

Explain how you'd detect a misleading metric in a dashboard.
""",
            "core2": """## Machine learning fundamentals

- Supervised: regression vs classification; linear, tree, ensemble models
- Unsupervised: clustering, dimensionality reduction — when useful
- **Metrics:** precision/recall, ROC-AUC, RMSE — pick metric to business cost
- **Train/validation/test** split; cross-validation; data leakage pitfalls

Interview: *"How would you predict customer churn?"* — features, metric, baseline, iteration.
""",
            "core3": """## Experimentation & causal thinking

- A/B test design: sample size, power, guardrail metrics
- **P-hacking and peeking** — sequential testing awareness
- Difference-in-differences, instrumental variables (high-level awareness)
- When correlation is enough vs when you need experiments

Tell a story about an experiment that changed a product decision.
""",
            "core4": """## ML in production (ML engineer angle)

- Feature stores, batch vs online features
- Model serving: batch scores vs real-time API
- Monitoring: prediction drift, data drift, performance decay
- Collaboration with DE on pipelines — who owns what

DS who understands deployment beats notebook-only candidates.
""",
            "core5": """## Case studies & communication

- Structure: business question → data → method → result → recommendation → risks
- **Executive summary first** — numbers with context
- Ethics: fairness, privacy, GDPR-style minimization
- Questions to ask: decision being made, success metric, timeline

Practice 15-min case aloud: fraud detection, recommendation, pricing — pick one.
""",
        }
    if role_key == "devsecops":
        return {
            "foundations": """## Security foundations for DevSecOps

- **CIA triad** + STRIDE threat modeling at service level
- OWASP Top 10 — know how to test and prevent in CI
- Least privilege, defense in depth, fail secure

Pass [Security basics](/quizzes/security-basics/) and [Linux shell](/quizzes/linux-shell/).

Pair with [DevOps interview sprint](/learn/devops-interview/) — DevSecOps interviews assume pipeline fluency.
""",
            "core1": """## Shift-left in CI/CD

Security gates in order of cost vs value:

1. Secret scanning (gitleaks) on every commit
2. SAST on PR
3. SCA / dependency CVE gates
4. Container image scan before registry push
5. IaC scan (Checkov/tfsec) on Terraform PRs
6. DAST in staging for critical apps

**Proportional control** — not every deploy needs manual security sign-off if automation proves low escape rate.
""",
            "core2": """## Supply chain security

- **SBOM** generation and storage with artifacts
- Sign images (Cosign) and verify at deploy (admission controller)
- Pin dependencies; review transitive updates
- Minimal base images; non-root containers

Interview: *"Developer wants to skip scan for hotfix."* — risk data, exception process, rollback ready.
""",
            "core3": """## Cloud & container hardening

- IAM: roles not users, short-lived creds, OIDC for CI
- K8s: NetworkPolicy, Pod Security Standards, workload identity
- Secrets: vault/Key Vault — never in Git or image layers
- Encryption at rest/transit, audit logging

Draw trust boundaries for a microservice handling PII.
""",
            "core4": """## Compliance & audit collaboration

- **SOC 2** trust principles mapped to pipeline controls
- GDPR: data minimization, retention, access logging
- Separation of duties: who can deploy prod vs who approves
- Audit trail: git SHA → pipeline → deployment record

You enable compliance; legal/compliance owns interpretation.
""",
            "core5": """## SecOps collaboration & incidents

- Vulnerability SLAs by severity (CVSS + exploitability)
- Security incident vs availability incident — coordinated response
- Blameless postmortems include security contributing factors
- Purple teaming awareness — validate controls, don't just checkbox

STAR story: prevented or responded to a security issue with systemic fix.
""",
        }
    if role_key == "qa":
        return {
            "foundations": """## Test fundamentals

Pyramid/trophy, equivalence partitioning, risk-based prioritization.

Pass [Testing fundamentals](/quizzes/testing-fundamentals/).
""",
            "core1": """## Test design

Plans, traceability, exploratory charters, crisp bug reports.
""",
            "core2": """## API automation

pytest + httpx, contract tests, CI on every PR.
""",
            "core3": """## UI automation & SDET

Playwright/Cypress, stable selectors, parallel CI, flake quarantine policy.
""",
            "core4": """## CI quality gates

Stages, coverage as signal, load smoke tests, release criteria.
""",
            "core5": """## Security & performance awareness

OWASP collaboration, load vs stress vs soak — when each matters.
""",
        }
    if role_key == "backend":
        return {
            "foundations": """## HTTP & SQL baseline

REST, status codes, pagination, indexes, transactions.

Pass [HTTP APIs](/quizzes/http-apis/) and [SQL fundamentals](/quizzes/sql-fundamentals/).
""",
            "core1": """## API design & auth

REST contracts, OAuth/JWT overview, idempotency, rate limits.
""",
            "core2": """## Databases & migrations

Isolation levels, N+1, expand/contract migrations.
""",
            "core3": """## Caching & messaging

Cache-aside, Redis, queues, idempotent consumers, outbox pattern.
""",
            "core4": """## Operability & security

Health checks, structured logs, authz on every object.
""",
            "core5": """## System design

45-min framework — practice URL shortener, rate limiter from [System design](/learn/system-design/).
""",
        }
    return {
        "foundations": """## Cloud fundamentals

Regions/AZs, shared responsibility, IAM, VPC/VNet basics.

Pass [Networking](/quizzes/networking-fundamentals/) and [Linux shell](/quizzes/linux-shell/).
""",
        "core1": """## Landing zones

Multi-account/org structure, policies, tagging, guardrails.
""",
        "core2": """## Infrastructure as code

Terraform modules, remote state, plan review in CI, drift.
""",
        "core3": """## Compute platforms

EKS/AKS/Lambda/App Service decision matrix, autoscaling.
""",
        "core4": """## Security, DR & FinOps

Encryption, backup/RTO/RPO, cost controls, Well-Architected reviews.
""",
        "core5": """## Migration & hybrid

6 R's, strangler fig, hybrid connectivity — vs hands-on DevOps on-call roles.
""",
    }


def _regional_employers_market(region_key: str) -> str:
    markets = {
        "sweden": """| Discipline | Notable sponsors & stacks |
|------------|---------------------------|
| DevOps/SRE | Volvo Group/Cars, Scania, IFS, Ericsson — Azure, AKS, GitHub |
| DevSecOps | Same enterprises + fintech — pipeline gates, ISO/SOC culture |
| Data eng | Spotify, Klarna, IKEA, Ericsson — Spark, BigQuery/Snowflake |
| Data science | Spotify, Klarna, King — experimentation, ML platforms |
| QA/SDET | Automotive quality culture, fintech product teams |
| Backend | Klarna, Mojang, payments APIs at scale |
| Cloud | Enterprise Azure, industrial hybrid cloud |
""",
        "australia": """| Discipline | Notable sponsors & stacks |
|------------|---------------------------|
| DevOps/SRE | Atlassian, IFS, banks, Telstra — AWS EKS, change control |
| DevSecOps | Banks (CPS 234), Atlassian — Essential Eight alignment |
| Data eng | CBA, NAB, Woolworths — Redshift, Databricks |
| Data science | Banks, Atlassian, Canva — experimentation platforms |
| QA/SDET | Banks (audit evidence), Atlassian, gov digital |
| Backend | Atlassian, Canva, REA — Java/Python microservices |
| Cloud | Big bank migration programs, AWS/Azure |
""",
        "new-zealand": """| Discipline | Notable sponsors & stacks |
|------------|---------------------------|
| All roles | Xero, Datacom — lean teams, end-to-end ownership |
| DevOps/SRE | Smaller platforms, AWS/Azure, pragmatic automation |
| DevSecOps | Health tech, SaaS — practical controls, smaller AppSec teams |
| Data eng / science | Xero analytics, agritech — SQL + pragmatic ML |
| QA/SDET | Health tech, SaaS — manual + automation blend |
""",
        "usa": """| Discipline | Notable sponsors & stacks |
|------------|---------------------------|
| All | H-1B Tier-1 filers — depth + system design at senior levels |
| DevOps/SRE | Tier-1 + IFS, Oracle, SAP — H-1B history varies by team |
| DevSecOps | Supply chain focus, SOC2, FedRAMP-aware contractors |
| Data eng | Lakehouse, Kafka, strict SQL + distributed systems |
| Data science | ML platform, causal inference, PhD-friendly loops at research labs |
| QA/SDET | SDET coding rounds, CI at scale |
| Backend | Standard coding + design loops |
| Cloud | Solutions architect vs engineer — clarify title early |
""",
        "uk": """| Discipline | Notable sponsors & stacks |
|------------|---------------------------|
| DevOps/SRE | Fintech GitOps, regulated deploy audit trails |
| DevSecOps | FCA resilience, GDPR, supply-chain scrutiny in fintech |
| Data eng | Revolut, Monzo, banks — GDPR, lineage |
| Data science | Revolut, Monzo, BBC — experimentation, responsible AI |
| QA/SDET | Fintech compliance testing, BBC digital |
| Backend | Go/Java microservices, change advisory |
| Cloud | Landing zones, FCA-aware resilience |
""",
    }
    return markets.get(region_key, "Research employers on official career pages.")


def _regional_culture(region_key: str) -> str:
    cultures = {
        "sweden": """- Flat hierarchy — challenge ideas respectfully
- Consensus and written decisions; **lagom** pace (safe speed)
- English interviews standard; Swedish helps daily life
- Fika and sustainable work-life balance are cultural signals
""",
        "australia": """- Direct but informal communication; first names common
- **Tall poppy syndrome** — team wins over solo hero stories
- Work-life balance valued; visa via 482/186 + ACS for many ICT roles
""",
        "new-zealand": """- Humble, practical tone in interviews (**Kiwi humility**)
- Small market — generalist ownership common
- Accredited Employer Work Visa — verify employer accreditation early
""",
        "usa": """- Think aloud in technical loops; STAR behavioral depth
- Leadership Principles at Amazon-style companies
- H-1B lottery timing — plan Tier-1 sponsors and O-1 backup
- Negotiate total comp (base + equity + signing)
""",
        "uk": """- Professional politeness + structured STAR answers
- Skilled Worker visa + sponsor register verification mandatory
- Fintech: regulated change control and audit awareness
- Good closing questions signal seniority
""",
    }
    return cultures.get(region_key, "")


def _related_electives_for_role(role_key: str) -> tuple[str, ...]:
    base: tuple[str, ...] = RELOCATION_SLUGS
    if role_key in ("data-eng", "data-science"):
        sibling = "data-science-interview" if role_key == "data-eng" else "data-eng-interview"
        return (*base, DATA_FUNDAMENTALS_SLUG, sibling)
    if role_key == "devsecops":
        return (*base, "devops-interview")
    return base


def _extra_battle_plan_notes(role_key: str) -> str:
    if role_key in ("data-eng", "data-science"):
        sibling = "Data science" if role_key == "data-eng" else "Data engineering"
        slug = "data-science-interview" if role_key == "data-eng" else "data-eng-interview"
        return f"""### Data track electives

- [Data fundamentals elective](/learn/{DATA_FUNDAMENTALS_SLUG}/) — shared SQL, Python, stats refresh (both DE & DS)
- [{sibling} sprint](/learn/{slug}/) — explore the sibling path if job descriptions blur roles
"""
    if role_key == "devsecops":
        return """### Recommended pairing

- [DevOps interview sprint](/learn/devops-interview/) — delivery, K8s, and on-call craft DevSecOps builds on
"""
    return ""


def build_core_roadmap(role_key: str) -> dict[str, Any]:
    role = ROLES[role_key]
    short = role["slug_short"]
    core = _role_core_content(role_key)
    elective_links = "\n".join(
        f"- [{RELOCATION_REGIONS[r]['flag']} {RELOCATION_REGIONS[r]['title']}](/learn/{RELOCATION_REGIONS[r]['slug']}/)"
        for r in ("sweden", "australia", "new-zealand", "usa", "uk")
    )

    lessons: list[dict[str, Any]] = [
        _lesson(
            f"{short}-battle-plan",
            "Week 0: Your 30-day battle plan",
            "Universal schedule, pass gates, and how to pick a regional elective.",
            f"""## How this questline works

**Core sprint (this map)** — technical and behavioral skills every market tests.

**Regional elective (pick one)** — visa routes, local employers, culture, relocation admin.
Run your core sprint in parallel; add the elective if you target sponsored roles abroad.

### Select your regional elective

{elective_links}
{_extra_battle_plan_notes(role_key)}

## Four-week schedule (~1 hr/day)

| Week | Focus |
|------|-------|
| 1 | Foundations + portfolio planning |
| 2 | Core technical depth (topics 1–2) |
| 3 | Core technical depth (topics 3–5) |
| 4 | Behavioral, mocks, final checklist |

## Pass criteria

| Gate | Requirement |
|------|-------------|
| Quizzes | Pass all related DevResurge quizzes |
| Portfolio | {role["portfolio"]} |
| Elective | Complete one regional pack if visa sponsorship needed |
| Mocks | 2 technical + 1 behavioral (recorded) |
""",
            outcomes=("Pick core sprint + optional regional elective",),
        ),
        _lesson(
            f"{short}-foundations",
            "Week 1: Foundations interview bar",
            "Baseline every loop tests before depth topics.",
            core["foundations"],
            quiz_slug=role["quizzes"][0],
            outcomes=("Pass foundation quizzes",),
        ),
        _lesson(
            f"{short}-week1-checkpoint",
            "Week 1 checkpoint",
            "Self-audit before Week 2 depth.",
            """Rate each 1–5 (target 4+): portfolio pitch, foundation quizzes, daily streak.
Pick one interview question from references; answer aloud in 20 minutes.
""",
            outcomes=("Complete honest self-audit",),
        ),
    ]

    titles = {
        "data-eng": (
            ("Week 2: Data modeling & warehousing", "Star schema, grain, medallion."),
            ("Week 2: Batch pipelines & orchestration", "Airflow, dbt, backfills."),
            ("Week 3: Streaming & CDC", "Kafka, late data."),
            ("Week 3: Data quality & observability", "Tests, SLAs, incidents."),
            ("Week 3: Cloud warehouses & lakehouse", "Snowflake, BigQuery, Databricks."),
        ),
        "data-science": (
            ("Week 2: Statistics & probability", "Distributions, bias-variance."),
            ("Week 2: Machine learning fundamentals", "Metrics, baselines, leakage."),
            ("Week 3: Experimentation & causality", "A/B tests, guardrails."),
            ("Week 3: ML in production", "Features, serving, drift."),
            ("Week 3: Case studies & communication", "Business impact storytelling."),
        ),
        "devsecops": (
            ("Week 2: Shift-left in CI/CD", "Pipeline security gates."),
            ("Week 2: Supply chain security", "SBOM, signing, SCA."),
            ("Week 3: Cloud & container hardening", "IAM, K8s policy, secrets."),
            ("Week 3: Compliance & audit", "SOC2, GDPR, segregation of duties."),
            ("Week 3: SecOps collaboration", "Incidents, vuln SLAs, purple team."),
        ),
        "qa": (
            ("Week 2: Test design", "Plans, risk, traceability."),
            ("Week 2: API automation", "pytest, CI integration."),
            ("Week 3: UI automation", "Playwright, flake policy."),
            ("Week 3: CI quality gates", "Pipeline stages, release bar."),
            ("Week 3: Security & performance", "OWASP, load basics."),
        ),
        "backend": (
            ("Week 2: API design & auth", "REST, OAuth/JWT."),
            ("Week 2: Databases", "SQL, migrations."),
            ("Week 3: Caching & messaging", "Redis, queues."),
            ("Week 3: Operability & security", "Logs, authz."),
            ("Week 3: System design", "45-min framework."),
        ),
        "cloud": (
            ("Week 2: Landing zones", "Multi-account governance."),
            ("Week 2: Infrastructure as code", "Terraform, drift."),
            ("Week 3: Compute platforms", "EKS/AKS/Lambda matrix."),
            ("Week 3: Security, DR & FinOps", "Backup, cost, encryption."),
            ("Week 3: Migration & hybrid", "6 R's, strangler pattern."),
        ),
    }[role_key]

    quiz_idx = 1
    for i, key in enumerate(("core1", "core2", "core3", "core4", "core5"), start=0):
        t, s = titles[i]
        q = role["quizzes"][quiz_idx] if quiz_idx < len(role["quizzes"]) else None
        quiz_idx += 1
        lessons.append(
            _lesson(
                f"{short}-{key}",
                t,
                s,
                core[key],
                quiz_slug=q,
                outcomes=(f"Explain {key} in an interview",),
            )
        )

    lessons.extend(
        [
            _lesson(
                f"{short}-behavioral",
                "Week 4: Behavioral prep",
                "STAR stories that work in any culture — tune examples in your elective.",
                """Prepare five STAR stories: shipped impact, incident/quality fix, disagreement, mentoring, fast learning.

Regional electives add culture-specific behavioral tips for your target country.
""",
                outcomes=("Draft five STAR stories under 3 minutes each",),
            ),
            _lesson(
                f"{short}-mock-final",
                "Week 4: Mock drills & interview day",
                "Timed technical + portfolio + behavioral practice.",
                """## Mocks

1. Technical (25 min) — use role question bank in references
2. Portfolio defense (15 min)
3. Behavioral (10 min)

## Interview day

Clarify questions, think aloud, admit gaps honestly, ask strong closing questions.
""",
                outcomes=("Complete two timed mocks",),
            ),
            _lesson(
                f"{short}-complete-resources",
                "Complete pass checklist",
                "Final audit before booking interviews.",
                """- [ ] Core lessons cleared
- [ ] Quizzes passed
- [ ] Portfolio live with README metrics
- [ ] Regional elective cleared (if visa path)
- [ ] Mocks recorded + cheat sheet written
""",
                minutes=16,
                outcomes=("All pass gates green",),
            ),
        ]
    )

    return {
        "slug": role["slug"],
        "title": role["title"],
        "tagline": role["tagline"],
        "description": role["description"],
        "domain": role["domain"],
        "level": role["level"],
        "icon": role["icon"],
        "order": role["order"],
        "audience": role["audience"],
        "outcomes": role["outcomes"],
        "related_quiz_slugs": role["quizzes"],
        "track": "interview",
        "related_roadmap_slugs": _related_electives_for_role(role_key),
        "lessons": lessons,
    }


def build_data_fundamentals_elective() -> dict[str, Any]:
    return {
        "slug": DATA_FUNDAMENTALS_SLUG,
        "title": "Data fundamentals elective",
        "tagline": "Shared SQL, Python, and stats refresh for data engineering and data science sprints.",
        "description": (
            "Optional add-on for [Data engineering](/learn/data-eng-interview/) and "
            "[Data science](/learn/data-science-interview/) sprints. Complete once if you "
            "need a structured refresher before depth topics — avoids duplicating content "
            "across both tracks."
        ),
        "domain": "data",
        "level": "foundations",
        "icon": "📐",
        "order": 62,
        "audience": "Candidates starting DE or DS sprints who want SQL/Python/stats aligned first.",
        "outcomes": (
            "Pass SQL and Python interview drills confidently",
            "Explain descriptive stats and experimental thinking",
            "Know when to pursue DE vs DS sibling sprint",
        ),
        "related_quiz_slugs": ("sql-fundamentals", "python-fundamentals"),
        "track": "elective",
        "related_roadmap_slugs": ("data-eng-interview", "data-science-interview"),
        "elective": True,
        "lessons": [
            _lesson(
                "df-intro",
                "How this elective fits DE & DS",
                "One shared foundation — two specialized sprints.",
                """## Why this exists

Data **engineering** and data **science** interviews overlap on SQL, Python, and thinking clearly about data — then diverge:

| Track | Primary interview focus |
|-------|-------------------------|
| [Data engineering](/learn/data-eng-interview/) | Pipelines, modeling, quality, warehouses |
| [Data science](/learn/data-science-interview/) | Statistics, ML, experiments, impact stories |

Complete this elective **once**, then run the sprint that matches your target roles (or both sequentially if hybrid).

Also add a [regional elective](/learn/relocation-sweden/) if you need visa guidance.
""",
                outcomes=("Choose DE, DS, or both core sprints",),
            ),
            _lesson(
                "df-sql",
                "SQL depth for data interviews",
                "Window functions, CTEs, and analytical queries.",
                """## Must-know SQL

- JOINs (inner/left), GROUP BY, HAVING pitfalls
- Window functions: `ROW_NUMBER`, `RANK`, `LAG`, running totals
- CTEs for readable multi-step logic
- Cohort retention query pattern

## Drill

Write SQL: monthly active users with month-over-month change — explain grain aloud.

Pass [SQL fundamentals](/quizzes/sql-fundamentals/) quiz.
""",
                quiz_slug="sql-fundamentals",
                outcomes=("Write analytical SQL without googling syntax",),
            ),
            _lesson(
                "df-python",
                "Python for data work",
                "pandas, numpy, and clean notebook habits.",
                """## Python bar

- pandas: filter, groupby, merge, handle nulls
- numpy: vectorization mindset (avoid row loops)
- Read/write CSV/Parquet; basic pytest for transforms
- Notebook hygiene: top-down narrative, named metrics

Pass [Python fundamentals](/quizzes/python-fundamentals/) quiz.
""",
                quiz_slug="python-fundamentals",
                outcomes=("Manipulate a dataset in pandas confidently",),
            ),
            _lesson(
                "df-stats",
                "Statistics refresher",
                "What DS loops test; what DE quality teams expect.",
                """## Core concepts

- Mean vs median — when median wins
- Variance, standard deviation, correlation ≠ causation
- Confidence intervals — intuitive interpretation
- Type I/II errors — link to A/B testing (DS path)

DE candidates: use stats language for **data quality** and anomaly detection.
DS candidates: go deeper in the [Data science sprint](/learn/data-science-interview/).
""",
                outcomes=("Explain a metric and its limitations",),
            ),
            _lesson(
                "df-checklist",
                "Data fundamentals complete",
                "Ready for DE or DS core sprint.",
                """- [ ] SQL drill completed
- [ ] Python/pandas drill completed
- [ ] SQL + Python quizzes passed
- [ ] Chosen DE, DS, or both core sprints
- [ ] Regional elective started if visa path
""",
                minutes=10,
                outcomes=("Proceed to chosen core sprint Week 1",),
            ),
        ],
    }


SPONSOR_PATH_BY_REGION: dict[str, str] = {
    "sweden": "sponsor-employers-sweden",
    "australia": "sponsor-employers-australia",
    "usa": "sponsor-employers-usa",
}


def build_relocation_roadmap(region_key: str) -> dict[str, Any]:
    region = RELOCATION_REGIONS[region_key]
    code = region["code"]
    culture = _regional_culture(region_key)
    employers = _regional_employers_market(region_key)
    sponsor_slug = SPONSOR_PATH_BY_REGION.get(region_key)
    sponsor_block = ""
    if sponsor_slug:
        sponsor_block = (
            "### Migration sponsor deep-dive (recommended)\n\n"
            "If you target **Volvo, IFS, or similar visa sponsors** in this market, "
            "add the dedicated employer path:\n\n"
            f"- [Migration sponsor path](/learn/{sponsor_slug}/) — "
            "interview stacks, application tactics, checklists"
        )

    core_links = "\n".join(
        f"- [{s.replace('-', ' ').title()}](/learn/{s}/)" for s in INTERVIEW_CORE_SLUGS
    )
    related = list(INTERVIEW_CORE_SLUGS)
    if sponsor_slug:
        related.insert(0, sponsor_slug)

    intro_parts = [
        f"## You chose: {region['title']}",
        "",
        "This elective is **optional** and **shared across disciplines**. "
        "Complete it once alongside any core interview sprint(s) you are running.",
        "",
        "### Compatible core sprints",
        "",
        core_links,
    ]
    if sponsor_block:
        intro_parts.extend(["", sponsor_block])
    intro_parts.extend(
        [
            "",
            "> Not legal advice. Verify immigration rules with official government sources.",
        ],
    )
    intro_body = "\n".join(intro_parts)

    lessons = [
        _lesson(
            f"reloc-{code}-intro",
            "How to use this regional elective",
            "Pair with any interview sprint — visa, employers, culture, relocation.",
            intro_body,
            outcomes=("Link this elective to your active core sprint",),
        ),
        _lesson(
            f"reloc-{code}-visa",
            "Visa sponsorship landscape",
            "Routes, sponsor signals, red flags, pre-offer checklist.",
            """## Sponsorship basics

Use official immigration links below. Confirm sponsorship in writing before relocating.

## Green flags

- Explicit visa sponsorship in offer or job post
- Employer experienced with mobility for your nationality
- Role aligns with skilled occupation / SOC requirements
- HR answers visa questions clearly

## Red flags

- "Full working rights only" with no exceptions
- Unaccredited / unlicensed sponsors (verify registers)
- Below-market pay for the region and title
""",
            outcomes=("Verify sponsor legitimacy",),
        ),
        _lesson(
            f"reloc-{code}-employers",
            "Employers & job market (all disciplines)",
            "Who sponsors DevOps, data, QA, backend, and cloud roles here.",
            f"""## Market map

{employers}

## Job search tactics

- Company careers pages first
- LinkedIn + "sponsorship" + your discipline
- Mention visa need early in process
- CV leads with measurable impact metrics
""",
            outcomes=("Shortlist 10+ target employers",),
        ),
        _lesson(
            f"reloc-{code}-culture",
            "Workplace culture & behavioral fit",
            "Regional norms for interviews and team collaboration.",
            f"""## Culture signals

{culture}

## Behavioral prep

Use STAR format from your core sprint; adapt tone and examples to regional norms above.

## Questions to ask employers

- Visa timeline and costs covered?
- On-call / quality expectations?
- Hybrid/office policy and relocation support?
""",
            outcomes=("Adapt STAR stories to regional culture",),
        ),
        _lesson(
            f"reloc-{code}-settling",
            "Relocation & first 90 days",
            "Admin checklist and proving value after arrival.",
            """## After signed offer

Complete visa steps promptly; track document deadlines.

## First 90 days

- Learn systems before proposing rewrites
- Ship one measurable improvement
- Build security/ops/product relationships
- Document runbooks for the next hire

## Long-term

Understand renewal and permanent residency paths — rules change; verify officially.
""",
            outcomes=("Draft personal relocation checklist",),
        ),
        _lesson(
            f"reloc-{code}-checklist",
            "Regional elective complete checklist",
            "Final gates before you relocate or sign.",
            """- [ ] Official visa route understood
- [ ] Sponsor verified (register / accreditation where applicable)
- [ ] Salary meets visa and market bars
- [ ] Core interview sprint progressing in parallel
- [ ] Housing/admin plan drafted
- [ ] Culture & behavioral stories adapted
""",
            minutes=12,
            outcomes=("Clear every box before signing",),
        ),
    ]

    return {
        "slug": region["slug"],
        "title": region["title"],
        "tagline": f"Optional add-on: visa, employers, and culture for {region_key.replace('-', ' ').title()}.",
        "description": (
            f"Select this elective when targeting visa-sponsored roles in "
            f"{region_key.replace('-', ' ').title()}. Works with any core interview sprint — "
            "complete once, reuse across disciplines."
        ),
        "domain": "relocation",
        "level": "foundations",
        "icon": region["flag"],
        "order": region["order"],
        "audience": "International candidates who need country-specific visa and culture guidance.",
        "outcomes": (
            "Navigate sponsorship rules for this market",
            "Target the right employers across DevOps, DevSecOps, data, QA, backend, and cloud",
            "Adapt behavioral interview style to local workplace culture",
        ),
        "related_quiz_slugs": (),
        "track": "relocation",
        "related_roadmap_slugs": tuple(related),
        "elective": True,
        "lessons": lessons,
    }


def all_career_roadmaps() -> tuple[dict[str, Any], ...]:
    cores = [build_core_roadmap(role_key) for role_key in ROLES]
    data_fundamentals = build_data_fundamentals_elective()
    regions = [build_relocation_roadmap(region_key) for region_key in RELOCATION_REGIONS]
    return (*cores, data_fundamentals, *regions)
