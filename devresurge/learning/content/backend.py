ROADMAP = {
    "slug": "backend-engineering",
    "title": "Backend engineering",
    "tagline": "APIs, data integrity, and services that survive production.",
    "description": (
        "Build backend systems the way strong product teams expect: clear APIs, "
        "correct transactions, safe migrations, and operable services."
    ),
    "domain": "backend",
    "level": "intermediate",
    "icon": "◈",
    "order": 40,
    "audience": "Backend and fullstack grads leveling toward mid/senior ownership.",
    "outcomes": (
        "Design REST/RPC APIs with versioning and idempotency",
        "Use transactions and isolation levels intentionally",
        "Ship schema changes without downtime",
    ),
    "related_quiz_slugs": (
        "http-apis",
        "sql-fundamentals",
        "django-basics",
        "security-basics",
    ),
    "lessons": [
        {
            "slug": "api-craft",
            "title": "API craft",
            "summary": "Resources, errors, pagination, versioning, idempotency.",
            "minutes": 14,
            "quiz_slug": "http-apis",
            "outcomes": ("Ship APIs clients can love for years",),
            "body": """
## Resource thinking

Model nouns, not RPC soup — unless gRPC/RPC is the team standard.

- Stable URLs, predictable verbs
- Structured error bodies (`code`, `message`, `details`)
- Cursor pagination over brittle offset for large sets
- Explicit versioning strategy (`/v1` or headers)

## Idempotency

For payments, enrollments, side-effecting POSTs: accept `Idempotency-Key`.
Store request hash → response for a retention window.

## Authn/z

- Authentication proves identity; authorization proves permission.
- Prefer short-lived tokens; validate on every sensitive action.
- Never trust client-supplied roles.

## Contract tests

Consumer-driven checks catch breaking changes before prod.
""",
        },
        {
            "slug": "transactions-and-integrity",
            "title": "Transactions and data integrity",
            "summary": "ACID, isolation anomalies, and when to use outbox patterns.",
            "minutes": 16,
            "quiz_slug": "sql-fundamentals",
            "outcomes": ("Prevent lost updates and dual-write bugs",),
            "body": """
## ACID in practice

- Keep transactions **short**
- Know isolation: read committed vs repeatable read vs serializable
- Watch for lost updates — use optimistic versioning or `SELECT … FOR UPDATE` when needed

## Dual-write problem

Writing DB + queue separately can diverge. Prefer:

- **Transactional outbox**
- Or a single source of truth with CDC

## Constraints are features

DB unique constraints, foreign keys, and check constraints catch bugs application code misses.

## Exercise

Implement transfer between two accounts without negative balances under concurrency.
""",
        },
        {
            "slug": "schema-migrations",
            "title": "Safe schema migrations",
            "summary": "Expand/contract, online changes, and zero-downtime deploys.",
            "minutes": 12,
            "outcomes": ("Migrate schemas without locking out users",),
            "body": """
## Expand / contract

1. **Expand** — add nullable columns / new tables; deploy code that writes both.
2. **Backfill** — in batches with throttling.
3. **Switch reads** to new shape.
4. **Contract** — remove old columns after code no longer needs them.

## Dangerous ops

- Long table locks on huge tables
- Rewriting entire tables in one transaction
- Dropping columns still read by old app instances during rolling deploys

## Rule

During rolling deploys, schema must be compatible with **both** old and new code.
""",
        },
        {
            "slug": "service-boundaries",
            "title": "Service boundaries and modularity",
            "summary": "Monolith modularity first; microservices when forced by scale/org.",
            "minutes": 12,
            "outcomes": ("Avoid distributed monoliths",),
            "body": """
## Start modular

A well-modular monolith beats premature microservices:

- Clear module APIs
- No reach-across DB tables between modules
- Async events at true boundaries

## Split when

- Independent deploy/scale needs
- Team ownership boundaries are real
- Failure isolation is required

## Costs of microservices

Network latency, partial failure, distributed tracing needs, ops overhead.

## Heuristic

If you can't draw a clean data boundary, you're not ready to split.
""",
        },
        {
            "slug": "security-in-backends",
            "title": "Security baselines for backends",
            "summary": "OWASP hotspots: injection, auth flaws, SSRF, secrets.",
            "minutes": 12,
            "quiz_slug": "security-basics",
            "outcomes": ("Build with secure defaults",),
            "body": """
## Must-not-miss

- Parameterized queries everywhere
- Output encoding for XSS surfaces
- CSRF protection for cookie sessions
- SSRF defenses when fetching user URLs
- Secret management (no keys in git)
- Least-privilege DB and cloud roles

## Auth mistakes

- Broken object-level authorization (IDOR)
- Trusting JWT payload without signature verify
- Long-lived tokens without revocation story

## Threat model lite

For each endpoint: who can call it, on whose data, what is the blast radius?
""",
        },
        {
            "slug": "operability",
            "title": "Operability: logs, metrics, runbooks",
            "summary": "Make 3am you grateful. Instrument before you need it.",
            "minutes": 12,
            "outcomes": ("Ship features that on-call can diagnose",),
            "body": """
## Three pillars

- **Metrics** — RED/USE; SLIs tied to user pain
- **Logs** — structured, correlatable (`request_id`)
- **Traces** — critical path spans across services

## Runbooks

For each alert: what it means, dashboards, common causes, mitigation, escalation.

## Feature flags

Decouple deploy from release. Progressive delivery reduces blast radius.

## Definition of done

Includes dashboards, alerts, and a rollback path — not just green CI.
""",
        },
    ],
}
