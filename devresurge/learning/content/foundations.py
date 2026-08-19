ROADMAP = {
    "slug": "strong-foundations",
    "title": "Strong foundations",
    "tagline": "The CS + SWE baseline elite teams assume you already have.",
    "description": (
        "Fresh-grad to hire-ready: how computers, networks, code, and teams "
        "actually work. Master this track before specialized paths."
    ),
    "domain": "core",
    "level": "foundations",
    "icon": "◆",
    "order": 10,
    "audience": "New grads and career switchers aiming at top product companies.",
    "outcomes": (
        "Explain how a request travels from browser to database and back",
        "Write clear, tested code with intentional trade-offs",
        "Use Git, reviews, and ownership like a professional engineer",
        "Debug with evidence instead of guessing",
    ),
    "related_quiz_slugs": (
        "python-fundamentals",
        "git-collaboration",
        "http-apis",
        "linux-shell",
        "testing-fundamentals",
    ),
    "lessons": [
        {
            "slug": "how-software-ships",
            "title": "How software actually ships",
            "summary": "Product → design → code → review → CI → deploy → observe → iterate.",
            "minutes": 10,
            "outcomes": (
                "Map the full delivery loop",
                "Know what 'done' means beyond a PR merge",
            ),
            "body": """
## The delivery loop

Merging a PR is the tutorial island. The real map is:

1. **Problem** — who hurts, what constraint, what success metric?
2. **Design** — interfaces, data model, failure modes (even a short design doc).
3. **Implement** — smallest change that proves the idea.
4. **Review** — correctness, readability, security, operability.
5. **Verify** — tests + staging + feature flags when risk is high.
6. **Ship** — deploy with rollback plan.
7. **Observe** — metrics, logs, traces; watch the blast radius.
8. **Learn** — post-ship notes beat silent heroics.

Elite engineers optimize the **whole loop**, not just typing speed.

## Ownership mindset

At FAANG-level teams, you own outcomes:

- If your change breaks prod, you lead the fix — even if CI was green.
- "Works on my machine" is not a release criterion.
- Docs and runbooks are part of the feature.

## Practical habits

- Prefer **vertical slices** (end-to-end) over horizontal layers that never integrate.
- Keep PRs reviewable: ~200–400 lines of meaningful diff when possible.
- Write the **rollback** before the rollout for risky changes.

## Checkpoint

Before your next feature, write one paragraph: problem, success metric, rollback.
""",
        },
        {
            "slug": "computers-and-complexity",
            "title": "Computers, memory, and complexity",
            "summary": "CPU, RAM, disk, Big-O — enough to reason about performance.",
            "minutes": 14,
            "outcomes": (
                "Estimate time/space for common operations",
                "Spot O(n²) traps in interviews and production",
            ),
            "body": """
## Mental model

- **CPU** executes instructions; cache misses are expensive.
- **RAM** is fast and scarce relative to disk.
- **Disk / network** are orders of magnitude slower than RAM.
- **Latency vs throughput** are different goals — optimize the one users feel.

## Big-O that actually matters

Know these cold:

- Array index: O(1); scan: O(n)
- Hash map average get/put: O(1); worst: O(n)
- Balanced BST ops: O(log n)
- Sorting comparison-based: O(n log n)
- Nested loops over n×n: O(n²) — interview and prod killer

## Constants matter too

O(n) with a network call per item can lose to O(n log n) in memory.
Always ask: **where does the data live?**

## Practice

For any slow endpoint: count DB queries, payload size, and lock duration.
Fix the largest bottleneck first — usually I/O, not micro-optimizing Python loops.
""",
        },
        {
            "slug": "networking-basics",
            "title": "Networking for application engineers",
            "summary": "DNS, TCP, TLS, HTTP — the path every API request takes.",
            "minutes": 14,
            "quiz_slug": "networking-fundamentals",
            "outcomes": (
                "Trace a request through DNS → TLS → HTTP",
                "Distinguish 4xx vs 5xx and idempotent methods",
            ),
            "body": """
## Path of a request

1. **DNS** resolves `api.example.com` → IP.
2. **TCP** handshake establishes a reliable byte stream.
3. **TLS** encrypts the channel (certificates, SNI).
4. **HTTP** sends method, path, headers, body.
5. Load balancer / reverse proxy routes to a service.
6. App handles auth, business logic, DB/cache.
7. Response returns; connection may be reused (keep-alive / HTTP/2).

## HTTP that seniors expect

- **GET** safe + idempotent; **PUT/DELETE** idempotent; **POST** usually not.
- **4xx** = client/request problem; **5xx** = server failed its job.
- Status **429** = rate limited; don't retry blindly without backoff.
- Prefer **idempotency keys** for payment-like POSTs.

## Debugging checklist

- Wrong host / DNS cache?
- TLS cert expired or hostname mismatch?
- Timeout too aggressive under load?
- Missing `Content-Type` or auth header?

## Lab

Use `curl -v` against a public API and label each stage of the handshake in the output.
""",
        },
        {
            "slug": "git-like-a-pro",
            "title": "Git and code review like a pro",
            "summary": "History hygiene, branching, and reviews that raise the bar.",
            "minutes": 12,
            "quiz_slug": "git-collaboration",
            "outcomes": (
                "Keep main releasable",
                "Give and receive high-signal review comments",
            ),
            "body": """
## Non-negotiables

- Never force-push **shared** main.
- Prefer small, bisectable commits with why-focused messages.
- Rebase (or merge) your feature branch onto latest main before review.

## Review as a skill

Great reviews ask:

- Is the design right for the problem?
- What fails under load / empty input / partial outage?
- Are tests proving behavior, not implementation trivia?
- Will the next engineer understand this in 6 months?

Tone: **curious and specific**, not vague ("this is messy").

## Local workflow

```
git switch -c feat/short-name
# …work…
git commit -m "Explain why, not only what"
git push -u origin HEAD
# open PR with context + test plan
```

## Checkpoint

On your next PR, add a **Test plan** checklist and a **Risk** note (what could break).
""",
        },
        {
            "slug": "debugging-and-testing",
            "title": "Debugging with evidence + testing judgment",
            "summary": "Reproduce, isolate, fix, prevent — and test what protects users.",
            "minutes": 14,
            "quiz_slug": "testing-fundamentals",
            "outcomes": (
                "Run a disciplined debug loop",
                "Choose unit vs integration tests intentionally",
            ),
            "body": """
## Debug loop

1. **Reproduce** reliably (or capture failing inputs).
2. **Isolate** — binary search the change set / layer.
3. **Instrument** — logs, metrics, a temporary assertion.
4. **Fix** the root cause, not the symptom.
5. **Prevent** — a regression test that would have failed.

Guessing wastes days. Evidence shortens incidents.

## Testing pyramid (pragmatic)

- **Unit** — pure logic, fast, many.
- **Integration** — DB/API boundaries that actually break.
- **E2E** — few critical user journeys; keep them stable.

Prefer testing **observable behavior**. Avoid locking tests to private helpers.

## Flakes are production debt

A flaky suite trains the team to ignore red CI. Quarantine or fix immediately.

## Exercise

Take a recent bug. Write the smallest test that fails without the fix and passes with it.
""",
        },
        {
            "slug": "communication-and-impact",
            "title": "Communication, impact, and leveling up",
            "summary": "How strong engineers create leverage beyond their own keyboard.",
            "minutes": 10,
            "outcomes": (
                "Write crisp design/status updates",
                "Aim work at measurable impact",
            ),
            "body": """
## Writing is a core engineering skill

At top companies, promotion packets and design reviews reward clarity:

- Context → options → recommendation → risks → ask.
- Prefer numbers: latency p99, error rate, cost, time saved.
- Separate facts from opinions.

## Impact > activity

Busy ≠ leveled. Track:

- User-facing outcomes (conversion, reliability, latency).
- Engineering leverage (shared libraries, deleted complexity).
- Mentorship and unblocking others.

## Career compounding

- Build a public **proof portfolio** (projects + quizzes + writeups).
- Seek feedback early; don't wait for annual reviews.
- Learn adjacent domains (DB, networking, product) — T-shaped beats narrow.

## Next

Continue to **DSA** and **System design** tracks in parallel with shipping real projects.
""",
        },
    ],
}
