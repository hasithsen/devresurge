ROADMAP = {
    "slug": "elite-engineer-path",
    "title": "Elite engineer path",
    "tagline": "The master roadmap: foundations → proof → FAANG-level signal.",
    "description": (
        "A sequenced plan for fresh grads: what to learn when, how to practice, "
        "what to ship, and how to turn skill into hireable proof on DevResurge."
    ),
    "domain": "career",
    "level": "foundations",
    "icon": "▲",
    "order": 5,
    "audience": "Ambitious grads who want a clear multi-month path, not random tutorials.",
    "outcomes": (
        "Follow a 6-month sequencing plan without thrashing",
        "Build a proof portfolio recruiters and engineers respect",
        "Combine roadmaps + quizzes into measurable progress",
    ),
    "related_quiz_slugs": (
        "python-fundamentals",
        "git-collaboration",
        "data-structures",
        "system-design-basics",
        "cicd-devops",
    ),
    "lessons": [
        {
            "slug": "north-star",
            "title": "North star: what 'elite' means",
            "summary": "Not leetcode alone — ownership, judgment, communication, proof.",
            "minutes": 10,
            "outcomes": ("Define personal excellence metrics",),
            "body": """## Elite ≠ trivia

Imagine two candidates. One recites 47 sorting algorithms. The other shipped
a rate-limited API, wrote the runbook, and can explain the trade-off in a
paragraph. Guess who the staff engineer wants on-call with them.

Top companies hire for:

- **Problem decomposition** under ambiguity
- **Code quality** that survives teams
- **Systems judgment** (trade-offs, failure modes)
- **Collaboration** (reviews, writing, mentorship)
- **Impact** (shipped outcomes)

LeetCode is the **filter**. It is not the **job**. Treat it like gym cardio —
necessary, not the sport.

## Your DevResurge advantage

## Your DevResurge advantage

Publish a technical README: stack, projects, quiz-backed badges, endorsements.
LinkedIn remains the network; here you show **signal**.

## Weekly scoreboard

- 1 substantial PR / project milestone
- 3–5 DSA problems with the interview script
- 1 systems lesson + notes
- 1 quiz pass or retry
""",
        },
        {
            "slug": "six-month-plan",
            "title": "Six-month sequencing plan",
            "summary": "Months 1–2 foundations, 3–4 depth, 5–6 proof + interviews.",
            "minutes": 14,
            "outcomes": ("Pick this week's focus without FOMO",),
            "body": """## Months 1–2 — Foundations

- Strong foundations roadmap (all lessons)
- Git + HTTP + Linux + testing quizzes
- Ship project #1: full-stack CRUD with auth, tests, CI

## Months 3–4 — Depth

- DSA patterns (daily practice)
- Databases + backend roadmaps
- Project #2: real complexity (jobs/queues, caching, or collaborative feature)
- Start system design weekly

## Months 5–6 — Signal

- System design + distributed systems
- DevOps/SRE roadmap; containerize and deploy project
- Mock interviews (coding + design)
- Polish DevResurge profile + public writeups

## Parallel rule

Never drop **shipping**. Theory without artifacts is invisible.
""",
        },
        {
            "slug": "projects-that-matter",
            "title": "Projects that matter",
            "summary": "Choose projects that demonstrate production instincts.",
            "minutes": 12,
            "outcomes": ("Scope a portfolio project with elite signals",),
            "body": """## Portfolio bar

Weak: todo app clones with no tests.
Strong: constrained real problem + trade-off writeup + deploy + metrics.

## Signals to include

- Authz that isn't swiss cheese
- Migrations and seed data
- CI pipeline
- Observability (even basic request metrics)
- README with architecture diagram and failure modes

## Idea seeds

- Rate-limited public API with quotas
- Link-in-bio analytics (privacy-first)
- Mini job queue + workers
- Collaborative markdown notes with conflict story

## Publish

Put the project on your DevResurge profile with stack tags and a crisp README link.
""",
        },
        {
            "slug": "practice-system",
            "title": "Practice system (DSA + design)",
            "summary": "Spaced practice, pattern catalogs, and mock interview cadence.",
            "minutes": 12,
            "quiz_slug": "algorithms-patterns",
            "outcomes": ("Install a sustainable practice loop",),
            "body": """## DSA loop (60–90 min)

1. Pick a pattern focus for the week
2. Warm-up easy (15m)
3. Timed medium (25–35m) with interview script
4. Review optimal approach + spaced retry in 3 days

## Design loop (weekly)

1. One prompt on a whiteboard/paper
2. 35 minutes timed
3. Compare to a reference; write 10-line postmortem

## Tracking

Keep a simple log: date, problem, pattern, time, mistake class.
Mistake classes > problem counts.

## Pairing

Mock with a peer monthly — communication is scored.
""",
        },
        {
            "slug": "interview-weeks",
            "title": "Interview weeks playbook",
            "summary": "How to ramp when applications and onsites go live.",
            "minutes": 12,
            "quiz_slug": "system-design-basics",
            "outcomes": ("Execute a calm interview week",),
            "body": """## Two weeks out

- Revisit weak DSA patterns
- Rehearse 4 classic system designs
- Sleep and exercise non-negotiable

## Day before

Light review only. Prepare questions for them (team, on-call, code quality).

## Day of

- Clarify → examples → plan → code → test
- For design: numbers early; trade-offs aloud
- If stuck: narrate options; ask for a hint strategically

## After

Write a private debrief within an hour: what broke, what to drill.

## Signal stack

Update DevResurge badges after each quiz pass — visible proof compounds.
""",
        },
        {
            "slug": "habit-of-leverage",
            "title": "The habit of leverage",
            "summary": "Compound learning: teaching, writing, and reusable tools.",
            "minutes": 10,
            "outcomes": ("Turn learning into durable leverage",),
            "body": """## Leverage loops

- Teach a concept in a short post → gaps appear → mastery
- Build tiny tools you reuse (scripts, templates, checklists)
- Review others' PRs for pattern exposure

## Avoid tutorial fog

If you can't explain it or ship it, you don't own it yet.

## Long game

Elite careers are compounding systems: skill × proof × network × reputation.
DevResurge helps the proof layer — keep shipping.

## Next actions

1. Finish **Strong foundations**
2. Start **DSA** daily
3. Pass related quizzes for badges
4. Ship project #1 with CI
""",
        },
    ],
}
