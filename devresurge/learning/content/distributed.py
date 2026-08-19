ROADMAP = {
    "slug": "distributed-systems",
    "title": "Distributed systems",
    "tagline": "Consistency, consensus, and failure — the advanced core.",
    "description": (
        "The concepts behind large-scale services: partial failure, replication, "
        "consensus, messaging semantics, and designing for the real world."
    ),
    "domain": "systems",
    "level": "advanced",
    "icon": "⬡",
    "order": 70,
    "audience": "Engineers ready to go deeper than single-node thinking.",
    "outcomes": (
        "Explain consistency models in plain language",
        "Design consumers that survive at-least-once delivery",
        "Reason about leader election and split brain risks",
    ),
    "related_quiz_slugs": ("distributed-systems-basics", "observability-basics"),
    "lessons": [
        {
            "slug": "partial-failure",
            "title": "Partial failure is normal",
            "summary": "Networks lie; clocks drift; retries duplicate — design for it.",
            "minutes": 12,
            "quiz_slug": "distributed-systems-basics",
            "outcomes": ("Stop assuming reliable networks",),
            "body": """
## Truths of distributed systems

- Messages can be delayed, duplicated, or reordered
- Nodes can pause (GC) and look dead
- Clocks are not perfectly synchronized
- You observe the system through incomplete signals

## Practical consequences

- Timeouts everywhere
- Idempotent handlers
- Explicit retry policies
- Quorums instead of "ask one node"

## Phrase to remember

**There is no "now" across machines** — only messages and local state.
""",
        },
        {
            "slug": "replication-consistency",
            "title": "Replication and consistency",
            "summary": "Leader/follower, quorum, linearizability vs eventual.",
            "minutes": 16,
            "outcomes": ("Match consistency to product needs",),
            "body": """
## Replication styles

- Single-leader
- Multi-leader
- Leaderless (quorum R/W)

## Consistency spectrum (plain English)

- **Linearizable** — reads see latest acknowledged write (expensive)
- **Sequential / causal** — weaker but useful
- **Eventual** — replicas converge; reads may be stale

## CAP as a conversation tool

During partition, you choose behavior. Don't recite CAP — apply it to the feature.

## Product examples

- Bank balance transfer: strong consistency
- Social like counts: often eventual is fine
""",
        },
        {
            "slug": "consensus-and-leadership",
            "title": "Consensus and leadership",
            "summary": "Why Raft/Paxos exist; split brain; fencing tokens.",
            "minutes": 14,
            "outcomes": ("Explain leader election risks",),
            "body": """
## Why consensus

Agreeing on a value/leader among unreliable nodes needs a protocol (Raft/Paxos family).

## Split brain

Two leaders accepting writes = corruption. Fencing tokens / epoch numbers reject stale leaders.

## Use managed primitives

Prefer battle-tested stores (etcd, ZooKeeper, cloud consensus services) over rolling your own.

## Interview angle

You don't implement Raft live — you explain why naive "ping the leader" fails.
""",
        },
        {
            "slug": "messaging-semantics",
            "title": "Messaging semantics",
            "summary": "At-most-once, at-least-once, exactly-once *effects*.",
            "minutes": 14,
            "outcomes": ("Build idempotent consumers",),
            "body": """
## Delivery guarantees

- **At-most-once** — may lose messages
- **At-least-once** — may duplicate (common default)
- **Exactly-once** — hard; usually "effectively once" via idempotency + dedupe store

## Consumer patterns

- Deduplicate by message id
- Transactional outbox on produce side
- Poison message handling / DLQ
- Ordering: per-partition keys, not global fantasy

## Kafka-ish intuition

Partitions scale throughput; key chooses partition; consumers track offsets.
""",
        },
        {
            "slug": "distributed-design-drills",
            "title": "Design drills",
            "summary": "Unique ID generation, distributed locks, and saga workflows.",
            "minutes": 14,
            "outcomes": ("Apply patterns to classic prompts",),
            "body": """
## Unique IDs

- DB sequences (single point)
- Snowflake-style (timestamp + worker + seq)
- ULID/UUIDv7 for sortable ids

## Distributed locks

Dangerous if misused. Prefer lease + fencing. Often a DB constraint is safer than a lock.

## Sagas

Long business workflows across services: orchestrate steps with compensations on failure.

## Practice prompts

- Global rate limiter
- Exactly-once payment capture
- Multi-region read-local / write-global notes app
""",
        },
    ],
}
