"""Hooks + boss fights that make each lesson feel like a quest."""

from __future__ import annotations

# lesson_slug -> (hook, boss_fight)
FLAVOR: dict[str, tuple[str, str]] = {
    "north-star": (
        "LeetCode is the bouncer. The party is ownership, judgment, and proof.",
        "Write your personal scoreboard: one shipping metric, one systems skill, one people skill.",
    ),
    "six-month-plan": (
        "You don't need 47 tabs. You need a sequence that compounds.",
        "Block this week's calendar: 1 ship, 4 DSA reps, 1 systems note. Screenshot it.",
    ),
    "projects-that-matter": (
        "Todo clones are camouflage. Production instincts are the costume that gets you hired.",
        "Scope a project with authz, CI, a migration, and a failure-mode README paragraph.",
    ),
    "practice-system": (
        "Elite practice is a loop, not a binge. Spaced reps beat heroic weekends.",
        "Log three problems with pattern + mistake class. Retry the miss in 72 hours.",
    ),
    "interview-weeks": (
        "Interview week is a sport. Sleep is a performance-enhancing drug.",
        "Rehearse one design aloud in 35 minutes. Write a 10-line debrief after.",
    ),
    "habit-of-leverage": (
        "Teaching is a debugger for your own brain. Write it down or it evaporates.",
        "Explain one concept from this path to a rubber duck (or a human). Note the gaps.",
    ),
    "how-software-ships": (
        "Merging is not shipping. Shipping is users + rollback + watching the blast radius.",
        "For your next change, write: problem, success metric, rollback — before the PR.",
    ),
    "computers-and-complexity": (
        "Your CPU is a sprinter. Disk and network are the ones stuck in traffic.",
        "Pick a slow endpoint you know and guess: queries, payload, or locks? Rank them.",
    ),
    "networking-basics": (
        "Every API call is a tiny road trip: DNS → handshake → TLS → HTTP → hopscotch.",
        "Run `curl -v` against any public API and label DNS, TCP, TLS, and HTTP in the output.",
    ),
    "git-like-a-pro": (
        "History is a team sport. Force-pushing shared main is lighting the stadium on fire.",
        "Open your next PR with a test plan and a one-line risk note. That's the whole meta.",
    ),
    "debugging-and-testing": (
        "Guessing is a hobby. Evidence is a career. Reproduce, isolate, fix, prevent.",
        "Take a real bug. Write the smallest test that fails without the fix.",
    ),
    "communication-and-impact": (
        "Busy looks like work. Impact looks like numbers, writing, and unblocked teammates.",
        "Rewrite a status update as: context → options → recommendation → risks → ask.",
    ),
    "interview-operating-system": (
        "Silent geniuses lose to clear, solid engineers. Narrate the movie as you shoot it.",
        "Solve one easy problem out loud with the 7-step script — even if you're alone.",
    ),
    "arrays-hashes-pointers": (
        "Hash maps are the interview's Swiss Army knife. Two pointers are the other blade.",
        "Time-box 25 minutes: two-sum + longest substring without repeating characters.",
    ),
    "trees-and-recursion": (
        "Trees are just linked lists that learned to multitask. Base cases first, ego second.",
        "Implement max depth and validate-BST. Say the base case before you type it.",
    ),
    "graphs-essentials": (
        "If it has dependencies, islands, or 'can I reach B from A?' — congratulations, it's a graph.",
        "Code number-of-islands or course-schedule. State O(V+E) like you mean it.",
    ),
    "heaps-intervals-binary-search": (
        "Heaps fetch the VIP. Binary search on the answer space is cheating — legal cheating.",
        "Solve one 'search the minimum feasible X' prompt. Prove monotonicity first.",
    ),
    "dynamic-programming": (
        "DP is not magic. It's 'what have I already decided?' plus a spreadsheet in disguise.",
        "Coin change or house robber: write state, transition, base case — then code.",
    ),
    "design-interview-framework": (
        "Don't freeze. Clarify, estimate, box-draw, deep-dive. The spine saves you.",
        "Whiteboard a URL shortener for 15 minutes using the 7-step spine. No peeking.",
    ),
    "capacity-and-slo": (
        "Hand-wavy 'it'll scale' is fanfic. QPS, storage, and p99 are the plot.",
        "Estimate QPS + storage for 1M DAU × 10 actions/day. Show your napkin math.",
    ),
    "data-and-storage": (
        "Pick the store for the access pattern, not the conference talk.",
        "For a news feed, list 3 read/write patterns, then name a store for each — and why not the others.",
    ),
    "caching-queues-cdn": (
        "Caches lie on purpose. Queues buy time. CDNs move the party to the edge.",
        "Sketch cache-aside for a hot profile page. Include stampede protection and TTL.",
    ),
    "reliability-patterns": (
        "Failure is the default weather. Timeouts, retries with jitter, and idempotency are umbrellas.",
        "Design payment capture: at-least-once delivery, exactly-once *effect*. Name the key.",
    ),
    "classic-designs": (
        "URL shortener, feed, chat, rate limiter — same Lego, different instruction booklet.",
        "Pick two classics. List the one bottleneck you'd deep-dive first in each.",
    ),
    "api-craft": (
        "APIs are promises. Breaking them is how you collect angry clients as a hobby.",
        "Write an error body + cursor pagination sketch for a list endpoint you like.",
    ),
    "transactions-and-integrity": (
        "Dual-writes are how money grows extra copies of itself. The database wants a monopoly.",
        "Describe transferring $5 between two accounts under concurrency without negative balances.",
    ),
    "schema-migrations": (
        "Expand, backfill, switch, contract. Dropping a column mid-rollout is a jump scare.",
        "Plan a rename of `user.name` → `display_name` for a rolling deploy. Four steps.",
    ),
    "service-boundaries": (
        "A distributed monolith is a monolith that also has network latency. Charming.",
        "Draw a module boundary in an app you know. If you can't, you're not ready to split.",
    ),
    "security-in-backends": (
        "Security is not a pepper-spray plugin. It's authorization on every object, every time.",
        "Pick an endpoint. Threat-model: who, whose data, blast radius, one IDOR test.",
    ),
    "operability": (
        "3am-you is a stakeholder. Instrument the feature like they're holding the pager.",
        "Write a 5-line runbook for 'p99 latency 10×': dashboards, first checks, rollback.",
    ),
    "cicd-pipeline": (
        "Green on your laptop is folklore. Green in CI on a tagged artifact is civilization.",
        "Sketch your dream pipeline in 8 boxes. Circle where you'd fail fastest.",
    ),
    "containers-runtime": (
        "A container is a process in a nice coat. Don't bake secrets into the lining.",
        "Write a 6-line Dockerfile wish-list: non-root, multi-stage, healthcheck, pin, no secrets, limits.",
    ),
    "linux-and-networking-ops": (
        "When prod sneezes, `ss`, `dig`, and `curl -v` are the tissues.",
        "Write a decision tree: A cannot reach B. DNS? listen? firewall? TLS?",
    ),
    "iac-and-environments": (
        "ClickOps is a magic trick that forgets the rabbit. IaC leaves a paper trail.",
        "List three prod/stage differences that should be config, not snowflake servers.",
    ),
    "observability-sre": (
        "If a tree falls in prod and nobody has an SLI, did it page? Please no.",
        "Define one SLI and SLO for a service you know. What alert would actually be actionable?",
    ),
    "incidents": (
        "Mitigate first, narrate second, blame never. The timeline is the product.",
        "Tabletop: deploy then p99 explodes. First 5 minutes — who does what?",
    ),
    "relational-mental-model": (
        "Tables are not IKEA shelves. They exist to answer queries without lying.",
        "Model a 'user has many projects' schema with keys and one constraint you'd refuse to skip.",
    ),
    "indexes-and-plans": (
        "An index is a cheat sheet. `EXPLAIN` is catching the planner in the act.",
        "For `WHERE email = ?`, say which index you'd add — and what write cost you just accepted.",
    ),
    "transactions-locking": (
        "Isolation levels are how databases gossip. Higher walls, longer lines at the lock.",
        "Name one anomaly Read Committed allows and how you'd stop a lost update.",
    ),
    "scaling-sql": (
        "Shard last. Indexes, cache, replicas, then drama. Hot rows are villains with a single chair.",
        "Rank four scaling levers for a read-heavy app. Which one would you try this week?",
    ),
    "beyond-relational": (
        "Postgres isn't jealous. Redis, search, and warehouses just have different hobbies.",
        "Pick a feature. Say which specialized store you'd add — and what remains source of truth.",
    ),
    "partial-failure": (
        "The network is a gossiping toddler. Timeouts, duplicates, and lies are the curriculum.",
        "List three things your last API client assumes are true. Cross out the ones that aren't.",
    ),
    "replication-consistency": (
        "Stale reads are a product decision, not a moral failing. Bank transfers disagree.",
        "For likes vs money, pick a consistency model and defend it in two sentences.",
    ),
    "consensus-and-leadership": (
        "Two leaders writing is a soap opera called Split Brain. Fencing tokens cancel the sequel.",
        "Explain why 'ping the leader, if quiet I am leader' fails. No Raft implementation required.",
    ),
    "messaging-semantics": (
        "At-least-once means déjà vu. Idempotent consumers are how you stay sane.",
        "Design a consumer that can see the same payment event twice without charging twice.",
    ),
    "distributed-design-drills": (
        "Unique IDs, locks, sagas — the gym circuit for distributed intuition.",
        "Pick one: global rate limiter, payment capture, or multi-region notes. Outline the hard part.",
    ),
}


def flavor_for(lesson_slug: str) -> tuple[str, str]:
    return FLAVOR.get(
        lesson_slug,
        (
            "Clear this quest. Future-you on-call will send a thank-you PR.",
            "Write one sentence you'll remember in an interview. Say it out loud.",
        ),
    )
