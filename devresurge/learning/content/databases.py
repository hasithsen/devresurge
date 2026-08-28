ROADMAP = {
    "slug": "databases-deep",
    "title": "Databases deep dive",
    "tagline": "Indexes, plans, transactions, and storage engines that scale.",
    "description": (
        "Go beyond CRUD: how indexes work, how to read query plans, "
        "isolation pitfalls, and when specialized stores win."
    ),
    "domain": "data",
    "level": "intermediate",
    "icon": "⊆",
    "order": 60,
    "audience": "Anyone who touches SQL in production — which is almost everyone.",
    "outcomes": (
        "Design indexes from query patterns",
        "Read EXPLAIN output for common disasters",
        "Choose consistency and storage trade-offs consciously",
    ),
    "related_quiz_slugs": ("sql-fundamentals", "databases-internals"),
    "lessons": [
        {
            "slug": "relational-mental-model",
            "title": "Relational mental model",
            "summary": "Keys, normalization, and modeling for access patterns.",
            "minutes": 12,
            "quiz_slug": "sql-fundamentals",
            "outcomes": ("Model entities with clear keys and constraints",),
            "body": """## Design from queries

Schema exists to answer access patterns efficiently — not to win purity contests.

- Normalize to reduce update anomalies
- Selectively denormalize for read-heavy paths (with clear ownership of truth)

## Keys

- Primary keys preferably immutable
- Natural vs surrogate keys trade-offs
- Composite keys for membership tables

## Integrity

Foreign keys and unique constraints are production safety rails.
""",
        },
        {
            "slug": "indexes-and-plans",
            "title": "Indexes and query plans",
            "summary": "B-trees, covering indexes, and EXPLAIN as a daily tool.",
            "minutes": 16,
            "quiz_slug": "databases-internals",
            "outcomes": ("Fix a slow query with an intentional index",),
            "body": """## B-tree intuition

Indexes keep ordered structures so lookups/ranges aren't full scans.

- Equality and range filters love the right index
- Leading column matters in composites
- `LIKE '%foo'` generally can't use a normal B-tree well

## Covering indexes

If all needed columns are in the index, skip heap/table lookups.

## EXPLAIN focus

Look for:

- Seq Scan on large tables (sometimes ok, often not)
- Nested Loop explosions
- Sort / HashAgg memory spills
- Rows estimates wildly wrong → stats issues

## Cost of indexes

Every index slows writes and uses space. Index what you query.
""",
        },
        {
            "slug": "transactions-locking",
            "title": "Transactions, locking, and anomalies",
            "summary": "Dirty reads, non-repeatable reads, phantoms, deadlocks.",
            "minutes": 14,
            "outcomes": ("Pick isolation levels with eyes open",),
            "body": """## Anomalies

- Dirty read
- Non-repeatable read
- Phantom read
- Lost update

Higher isolation reduces anomalies and can increase lock contention.

## Locking tips

- Keep transactions short
- Consistent lock ordering prevents deadlocks
- Optimistic concurrency (version column) for contended rows

## Practical default

Many apps run Read Committed + careful application checks; know when you need stronger.
""",
        },
        {
            "slug": "scaling-sql",
            "title": "Scaling SQL systems",
            "summary": "Replicas, partitioning, connection pooling, and hot rows.",
            "minutes": 14,
            "outcomes": ("Name scaling levers before microservices",),
            "body": """## Vertical then horizontal

1. Fix queries/indexes
2. Cache hot reads
3. Read replicas for read-heavy workloads
4. Partition/shard when a single primary can't keep up

## Pooling

Apps exhaust DB connections fast. Use pooling (PgBouncer, etc.).

## Hot rows

Counters on one row serialize writers — shard counters or use aggregation patterns.

## Migrations at scale

Online schema change tools; batched backfills; expand/contract.
""",
        },
        {
            "slug": "beyond-relational",
            "title": "Beyond relational",
            "summary": "KV, document, search, warehouse — right tool, right job.",
            "minutes": 12,
            "outcomes": ("Avoid hype-driven database choices",),
            "body": """## When specialized stores win

- **Redis** — hot ephemeral state, rate limits, queues (carefully)
- **Document** — flexible documents with mostly PK access
- **Search** — relevance and full-text
- **Warehouse / OLAP** — analytics scans, not OLTP transactions
- **Blob** — large objects

## Consistency reminder

Caches and search indexes are usually **derived**. Design repair paths.

## Decision template

Write access patterns + consistency needs + ops maturity before picking tech.
""",
        },
    ],
}
