ROADMAP = {
    "slug": "system-design",
    "title": "System design",
    "tagline": "From napkin sketches to FAANG design-round fluency.",
    "description": (
        "Requirements, capacity, APIs, data models, scaling levers, and "
        "reliability patterns used in real large-scale systems."
    ),
    "domain": "systems",
    "level": "intermediate",
    "icon": "▣",
    "order": 30,
    "audience": "Engineers preparing for design interviews and owning services.",
    "outcomes": (
        "Drive a 45-minute design discussion with structure",
        "Choose storage, cache, and queue patterns deliberately",
        "Call out bottlenecks, failure modes, and trade-offs",
    ),
    "related_quiz_slugs": ("system-design-basics", "http-apis"),
    "lessons": [
        {
            "slug": "design-interview-framework",
            "title": "Design interview framework",
            "summary": "Clarify → estimate → API → data → high-level → deep dives → scale.",
            "minutes": 12,
            "quiz_slug": "system-design-basics",
            "outcomes": ("Never freeze — always have a next step",),
            "body": """
## 45-minute spine

1. **Requirements** — functional + non-functional (QPS, latency, consistency).
2. **Back-of-envelope** — users, QPS, storage, bandwidth.
3. **API sketch** — resources, idempotency, pagination.
4. **Data model** — entities, keys, access patterns.
5. **High-level diagram** — clients, LB, services, DB, cache, queue.
6. **Deep dives** — hottest path, consistency, failure handling.
7. **Scale & evolve** — bottlenecks, sharding, multi-region (if asked).

## Clarify ruthlessly

Ask: read/write ratio? strong consistency needed? mobile offline? retention?

## Communication

Draw boxes; narrate trade-offs; invite interviewer constraints.
""",
        },
        {
            "slug": "capacity-and-slo",
            "title": "Capacity math and SLOs",
            "summary": "QPS, storage, p99 latency, error budgets — speak in numbers.",
            "minutes": 12,
            "outcomes": ("Estimate load without a calculator panic",),
            "body": """
## Quick estimates

- 1M DAU × 10 actions/day ≈ 10M events/day ≈ ~115 QPS average (bursts higher).
- Peak ≈ 2–5× average unless told otherwise.
- Storage: records × size × replication × retention.

## Latency budgets

If p99 API must be 200ms, DB + downstream + network must fit. Caching and parallelism buy budget.

## SLOs & error budgets

- Availability 99.9% ≈ ~43 min downtime/month.
- Error budget tells you when to slow feature work for reliability.

## Practice

Design for URL shortener: 100M new URLs/month, 10:1 read/write — estimate storage and QPS.
""",
        },
        {
            "slug": "data-and-storage",
            "title": "Choosing data stores",
            "summary": "SQL vs NoSQL vs blob vs search — pick for access patterns.",
            "minutes": 14,
            "outcomes": ("Map access patterns to storage tech",),
            "body": """
## Decision drivers

- Access pattern (key lookup, range, full-text, graph)
- Consistency needs
- Write volume / append-only?
- Query flexibility vs scale

## Rough map

- **Relational** — transactions, joins, mature tooling
- **KV / document** — simple primary-key scale-out
- **Wide-column** — large-scale time-series / sparse rows
- **Blob** — images, videos, large objects
- **Search** — inverted index relevance
- **Cache** — ephemeral acceleration, not source of truth

## Anti-pattern

Choosing Mongo "because JSON" when you need multi-row transactions.

## Exercise

For a news feed: list read/write patterns first, then pick stores.
""",
        },
        {
            "slug": "caching-queues-cdn",
            "title": "Caches, queues, and CDNs",
            "summary": "The three levers that save databases and smooth spikes.",
            "minutes": 14,
            "outcomes": ("Place cache/queue/CDN with clear invalidation stories",),
            "body": """
## Caching

- **CDN** for static & edge content
- **App cache** (Redis) for hot keys / sessions
- Patterns: cache-aside, write-through, TTL + stampede protection

Invalidation is the hard part — design keys and TTLs intentionally.

## Queues

Use for:

- Async fan-out (emails, thumbnails)
- Load leveling
- Decoupling producers/consumers

Decide: at-least-once vs exactly-once *effect* (idempotent consumers).

## Backpressure

When consumers lag, shedding load beats unbounded queue growth.
""",
        },
        {
            "slug": "reliability-patterns",
            "title": "Reliability patterns",
            "summary": "Timeouts, retries, idempotency, circuit breakers, graceful degradation.",
            "minutes": 14,
            "outcomes": ("Design for failure as the default",),
            "body": """
## Defaults of resilient services

- Timeouts on every remote call
- Retries with **jittered exponential backoff**
- Idempotency keys for unsafe side effects
- Circuit breakers / bulkheads to contain failure
- Graceful degradation (serve stale/cached when possible)

## Consistency trade-offs

Say CAP-ish trade-offs in plain language: during partition, prefer availability or correct reads?

## Observability

You can't operate what you can't see: RED metrics (rate, errors, duration) + traces on critical paths.

## Deep dive prompt

Design payment capture: exactly-once *effect* with at-least-once delivery.
""",
        },
        {
            "slug": "classic-designs",
            "title": "Classic designs to rehearse",
            "summary": "URL shortener, news feed, chat, rate limiter — reusable building blocks.",
            "minutes": 16,
            "outcomes": ("Reuse components across prompts",),
            "body": """
## URL shortener

- Key generation (hash vs counter + base62)
- 301/302 semantics & analytics
- Hot-key caching

## News feed

- Push vs pull vs hybrid fanout
- Ranking and pagination cursors
- Celebrity problem

## Chat / messaging

- WebSockets / long poll
- Message ordering per conversation
- Presence and delivery receipts

## Rate limiter

- Token bucket / sliding window
- Redis counters
- Per-user vs per-IP vs global

## Practice plan

Whiteboard each once weekly; vary constraints each time.
""",
        },
    ],
}
