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
    "30-day-battle-plan": (
        "Hyperscale loops test judgment under scale — not Azure flashcards.",
        "Block four weeks: 6 study days + 1 lab. Screenshot your calendar.",
    ),
    "linux-shell-interview": (
        "Interviewers love a calm `curl -v` more than a panicked SSH session.",
        "Write a 6-step debug checklist for 'service A cannot reach B' — no googling.",
    ),
    "git-collaboration-interview": (
        "Trunk-based flow is boring on purpose. Boring ships; drama rolls back.",
        "Draft a 60-second STAR story about improving PR quality on your team.",
    ),
    "networking-http-ops": (
        "Every 502 is a story: DNS, TLS, LB, probe, or the deploy you forgot about.",
        "Draw client → pod on paper. Label where TLS terminates and where probes run.",
    ),
    "week1-checkpoint": (
        "Week 1 is the foundation — skip it and design mocks feel like improv.",
        "Complete the 502 drill and the log-parsing script in 75 minutes total.",
    ),
    "cicd-design-interview": (
        "Build once, promote everywhere — say it like a mantra until they believe you.",
        "Whiteboard 8 pipeline stages in 5 minutes. Circle your fastest fail gate.",
    ),
    "cicd-release-engineering": (
        "Release engineering is how thousands of commits become safe prod — YAML is the proof.",
        "Sketch a pipeline: PR test → OIDC build → scan → staging → canary prod.",
    ),
    "docker-production-interview": (
        "Root in a container is a red flag wearing a security badge.",
        "Write a production Dockerfile outline: multi-stage, non-root, healthcheck, pin.",
    ),
    "kubernetes-production-essentials": (
        "Pods die. Deployments, PDBs, and probes decide whether users notice.",
        "Explain rolling deploy + rollback with probes and limits — out loud, 2 minutes.",
    ),
    "week2-checkpoint": (
        "A public pipeline repo beats ten buzzwords. Interviewers click the README.",
        "Ship the portfolio pipeline this weekend: CI, image, K8s, rollback doc.",
    ),
    "terraform-iac-interview": (
        "State is the source of truth. Lose it and infra becomes fan fiction.",
        "List three Terraform prod risks (state, drift, destroy) and one fix each.",
    ),
    "cloud-platform-engineering": (
        "Platform design is IAM + tenancy + observability — name the trade-offs.",
        "Whiteboard a multi-team K8s platform: isolation, GitOps, on-call, SLO.",
    ),
    "config-secrets-twelve-factor": (
        "Secrets in Git are a time bomb with a merge conflict.",
        "Describe how connection strings reach a pod without ever touching the repo.",
    ),
    "devsecops-supply-chain": (
        "Shift-left means scanners in CI, not security as a deploy-day surprise party.",
        "List five security gates you'd add before prod. Prioritize by blast radius.",
    ),
    "week3-checkpoint": (
        "Infra design rounds freeze without a spine — clarify before you diagram.",
        "Run one 35-minute design mock: global CI for 500 engineers. Timer on.",
    ),
    "observability-slo-interview": (
        "Page on user pain, not CPU curiosity. On-call sleep is a reliability feature.",
        "Define one SLI, one SLO, and one alert you'd actually wake up for.",
    ),
    "incident-response-interview": (
        "Mitigate first, root-cause later. Users don't care about your gdb session.",
        "Write a blameless postmortem outline for a deploy-gone-wrong story.",
    ),
    "behavioral-devops-interview": (
        "Bar-raisers listen for ownership and customer impact — not buzzwords.",
        "Draft five STAR bullets with metrics: automate, conflict, incident, mentor, learn.",
    ),
    "technical-mock-drills": (
        "Full-loop mocks: pipeline, K8s, design, scripting — structure beats panic.",
        "Record 35 minutes: one design mock + one K8s debug. Fix one ramble.",
    ),
    "final-checklist-interview-day": (
        "You've done the reps. Interview day is execution, not cramming.",
        "Handwrite your one-page cheat sheet. Put it away until the night before.",
    ),
    "sprint-complete-resources": (
        "The pass checklist — red gates mean reschedule, not hope.",
        "Walk every box. Portfolio link live before you book loops.",
    ),
    "se-devops-battle-plan": (
        "Sweden rewards calm engineers who ship safely — not heroes who hide incidents.",
        "Block four weeks on your calendar: 5 study slots + 1 employer research session.",
    ),
    "se-visa-sponsor-landscape": (
        "A vague 'we might sponsor' is not a relocation plan. Get it in writing.",
        "List three green flags and three red flags from real Swedish job posts you've seen.",
    ),
    "se-employers-and-stacks": (
        "Gothenburg builds trucks; Stockholm builds playlists — both need pipelines.",
        "Shortlist 10 Swedish employers. Note city, stack, and sponsorship mention.",
    ),
    "se-foundations-interview": (
        "Nordic flat hierarchy still expects you to debug a broken deploy without hand-holding.",
        "Pass linux-shell quiz. Explain CrashLoopBackOff aloud in under 2 minutes.",
    ),
    "se-azure-k8s-stack": (
        "AKS + Key Vault + ACR — the Swedish enterprise hat-trick.",
        "Draw Internet → Ingress → Pod on paper. Label where secrets live.",
    ),
    "se-cicd-pipeline-interview": (
        "Lagom delivery: not reckless speed, not change-advisory paralysis.",
        "Whiteboard 8 pipeline stages. Circle where automotive teams add scan gates.",
    ),
    "se-terraform-iac": (
        "ClickOps in prod is a Swedish no-no when audit asks 'who changed this?'",
        "Write three Terraform PR review checks you'd enforce on a platform team.",
    ),
    "se-observability-incidents": (
        "Blameless postmortems are cultural export — Sweden takes them seriously.",
        "One SLI, one SLO, one alert you'd wake for. Say it like an on-call handoff.",
    ),
    "se-security-compliance": (
        "GDPR and automotive traceability — compliance is a feature, not a meeting.",
        "Name five pipeline security gates. Rank by user blast radius.",
    ),
    "se-behavioral-culture": (
        "Fika is rapport. STAR stories are proof. Bring both.",
        "Draft five STAR bullets tuned for flat hierarchy and team credit.",
    ),
    "se-relocation-practical": (
        "Personnummer unlocks Swedish life — plan housing before you celebrate the offer.",
        "Draft a relocation checklist: offer → permit → housing → personnummer → Day 1.",
    ),
    "se-mock-drills-final": (
        "Azure + safety culture — the Nordic enterprise platform duet.",
        "Two timed mocks: AKS pipeline design + 502 debug. Record one.",
    ),
    "se-complete-resources": (
        "Migrationsverket waits for no one — checklist everything before the offer signature.",
        "Clear every box on the pass checklist. Screenshot for your relocation folder.",
    ),
    "au-devops-battle-plan": (
        "Sydney rent is brutal — your pipeline skills pay the visa and the lease.",
        "Map four weeks on your calendar including ACS prep if you need it.",
    ),
    "au-visa-sponsor-landscape": (
        "482 vs 186 is not trivia — it's your multi-year plan in two acronyms.",
        "Verify one job ad against Skilled Occupation List vocabulary. Screenshot notes.",
    ),
    "au-employers-and-stacks": (
        "Atlassian ships Jira; you ship the CI that doesn't break on Friday.",
        "List 15 AU employers with sponsorship signals. Tag bank vs product.",
    ),
    "au-foundations-interview": (
        "CBA cares about change records; Canva cares about canaries — tailor the story.",
        "Pass linux-shell and git-collaboration quizzes this week.",
    ),
    "au-aws-eks-stack": (
        "IRSA beats long-lived AWS keys like Vegemite beats… actually, nothing beats keys less.",
        "Sketch Route 53 → ALB → EKS with CloudWatch and Secrets Manager labeled.",
    ),
    "au-cicd-compliance": (
        "APRA doesn't want your hero deploy — it wants audit trails and rollback.",
        "Design a pipeline with an immutable audit log from commit to prod.",
    ),
    "au-terraform-iac": (
        "S3 state + DynamoDB lock — say it before they ask where Terraform lives.",
        "Describe OIDC from GitHub Actions to AWS without static credentials.",
    ),
    "au-observability-incidents": (
        "Fair dinkum on-call means actionable pages, not CPU astrology.",
        "Write an error budget policy in five sentences for a payments API.",
    ),
    "au-security-devsecops": (
        "Essential Eight maturity — banks nod when you connect patches to pipelines.",
        "Map three Essential Eight controls to automation you'd own as DevOps.",
    ),
    "au-behavioral-culture": (
        "Tall poppy syndrome: team win, humble tone, metrics not ego.",
        "Prepare five STAR stories. Cut any 'I alone saved prod' bragging.",
    ),
    "au-relocation-practical": (
        "TFN, super, Medicare — admin quests before your first prod deploy.",
        "Draft 90-day relocation checklist from offer letter to first week.",
    ),
    "au-mock-drills-final": (
        "Fair dinkum reliability engineers are hired, not wished into existence.",
        "Mock: EKS pipeline + bank change-freeze exception. Time each 20 min.",
    ),
    "au-complete-resources": (
        "ACS slow, Home Affairs slower — the checklist keeps you honest while you wait.",
        "Every pass gate ticked? If not, you know exactly what to do this week.",
    ),
    "nz-devops-battle-plan": (
        "Small market, lean teams — you're platform, on-call, and sometimes lunch IT.",
        "Set weekly goals: study, applications, one hands-on lab.",
    ),
    "nz-visa-sponsor-landscape": (
        "Accredited employer or bust — verify on INZ before the third interview.",
        "Find three NZ employers on accredited list with platform roles open.",
    ),
    "nz-employers-and-stacks": (
        "Xero exported accounting; you'll export reliable deploys.",
        "Research 10 accredited employers. Note AWS vs Azure and team size.",
    ),
    "nz-foundations-interview": (
        "Solo on-call Saturday — interviewers want to hear you've lived it.",
        "45-min drill: Friday deploy fail → timeline for mitigate + postmortem.",
    ),
    "nz-cloud-cicd": (
        "Right-sized beats clever when the platform team is you plus one hat.",
        "Outline a GitHub Actions pipeline README you'd show in an interview.",
    ),
    "nz-kubernetes-iac": (
        "One shared cluster, many namespaces — NZ scale in one sentence.",
        "Explain rollout undo + Terraform plan review as if to a CTO.",
    ),
    "nz-observability-incidents": (
        "Five-person company, fifty alerts — fix the alerts, not the headcount.",
        "Define MVP observability: metrics, logs, one dashboard, two alerts.",
    ),
    "nz-security-basics": (
        "Privacy Act 2020 — DevOps enables encryption; legal owns interpretation.",
        "List five security controls for your first 90 days at a NZ SaaS.",
    ),
    "nz-behavioral-culture": (
        "Kiwi humility: 'we shipped' beats 'I rescued' every time.",
        "Three STAR stories emphasizing team outcomes and practical fixes.",
    ),
    "nz-relocation-practical": (
        "IRD, KiwiSaver, Auckland rent — plan before you pack.",
        "Draft timeline: offer → visa → arrival → first month checklist.",
    ),
    "nz-mock-drills-final": (
        "Kia kaha — generalists who automate toil get sponsored.",
        "Mock: lean platform for 3 services + solo on-call first 10 minutes.",
    ),
    "nz-complete-resources": (
        "Small market, sharp prep — this page is your NZ interview bible.",
        "Verify accredited employer list + pass checklist before any verbal offer.",
    ),
    "us-devops-battle-plan": (
        "H-1B lottery is a plot twist — plan O-1 evidence and Tier-1 sponsors in parallel.",
        "Mark H-1B calendar dates and start Tier-1 applications timeline.",
    ),
    "us-visa-sponsor-landscape": (
        "USCIS history is signal, not guarantee — still beats guessing.",
        "Tier your target list: Tier 1 frequent sponsors vs risky startups.",
    ),
    "us-employers-and-stacks": (
        "L5 vs E5 vs SDE III — level before comp or you'll negotiate blind.",
        "Rewrite resume bullets with metrics: MTTR, deploy freq, cost saved.",
    ),
    "us-foundations-interview": (
        "Light scripting rounds separate tourists from operators who automate.",
        "Solve one log-parsing script in 20 minutes. Explain complexity aloud.",
    ),
    "us-aws-eks-deep": (
        "Design round: VPC, EKS, IRSA, GitOps — draw before they ask depth.",
        "Whiteboard multi-AZ EKS platform. Name one failure mode per component.",
    ),
    "us-cicd-at-scale": (
        "A thousand microservices need blast radius limits, not hope.",
        "Explain canary analysis + auto-rollback in 3 minutes.",
    ),
    "us-terraform-iac": (
        "Platform teams sell paved roads — Terraform modules are the asphalt.",
        "Describe self-service namespace module with guardrails in five bullets.",
    ),
    "us-sre-observability": (
        "Error budget meeting — Google exported the meeting, US interviews import it.",
        "Narrate an error budget dispute: launch or freeze? Show judgment.",
    ),
    "us-security-compliance": (
        "SOC2 auditors love immutable artifacts and hate shared prod passwords.",
        "Map three SOC2 trust principles to pipeline controls you own.",
    ),
    "us-behavioral-negotiation": (
        "Leadership Principles at Amazon — two stories each or don't claim Ownership.",
        "Prepare 10 STAR stories + comp anchors from levels.fyi for your target level.",
    ),
    "us-system-design-infra": (
        "Infra design is system design with sharper failure modes.",
        "45-min mock aloud: design CI at GitHub Actions scale. Record it.",
    ),
    "us-mock-drills-final": (
        "Full loop mock beats reading Hacker News the night before.",
        "Run scripting + infra design + behavioral in one mock day.",
    ),
    "us-complete-resources": (
        "H-1B lottery is random; your checklist is the part you control.",
        "Clear every gate. Book the lawyer consult if H-1B is your path.",
    ),
    "uk-devops-battle-plan": (
        "Skilled Worker + CoS — know the acronym soup before the technical soup.",
        "Align four-week study with sponsor register research time.",
    ),
    "uk-visa-sponsor-landscape": (
        "Not on the sponsor register? Next tab. Life's too short.",
        "Verify three target employers on UK licensed sponsor register.",
    ),
    "uk-employers-and-stacks": (
        "Revolut velocity, Barclays caution — same K8s, different change advisory.",
        "Shortlist 15 licensed sponsors: fintech vs bank vs scale-up.",
    ),
    "uk-foundations-interview": (
        "Take-home Terraform tasks are auditions — treat README like a cover letter.",
        "Pass linux-shell, git, networking quizzes. Prep one take-home outline.",
    ),
    "uk-kubernetes-gitops": (
        "GitOps rollback = revert commit. kubectl apply prod is the villain.",
        "Explain Argo CD sync vs kubectl rollback in 2 minutes.",
    ),
    "uk-aws-gcp-cloud": (
        "eu-west-2 London — data residency answers impress FCA-adjacent interviewers.",
        "Compare EKS vs GKE for fintech microservices — trade-offs, not fanboy picks.",
    ),
    "uk-cicd-regulated": (
        "Auditor asks who deployed v1.2.3 at 03:14 — your pipeline better know.",
        "Design deploy audit chain: Git SHA → pipeline → CloudTrail in five steps.",
    ),
    "uk-terraform-iac": (
        "FinOps tags aren't boring — they're how London CFOs sleep.",
        "Review a fictional Terraform PR: plan output, blast radius, Checkov gate.",
    ),
    "uk-observability-incidents": (
        "Datadog dashboards don't page themselves — burn rate alerts do.",
        "Define SLOs for a UK payments API. One alert, one runbook link.",
    ),
    "uk-security-gdpr": (
        "Prod DB in staging is a GDPR horror story — interviewers listen for that reflex.",
        "Explain masked non-prod data strategy without hand-waving 'we're careful'.",
    ),
    "uk-behavioral-culture": (
        "Professional politeness + solid STAR — the London panel combo meal.",
        "Five STAR stories. Ask them three questions about CoS and on-call.",
    ),
    "uk-relocation-practical": (
        "NI number, GP, council tax — adulting speedrun after visa stamp.",
        "Draft UK relocation checklist from CoS to first day hybrid policy.",
    ),
    "uk-mock-drills-final": (
        "GitOps + FCA awareness — the London platform interview duet.",
        "Mock: GitOps platform + regulated emergency deploy. Cheat sheet after.",
    ),
    "uk-complete-resources": (
        "Sponsor register or scroll past — this checklist saves months of dead ends.",
        "Verify sponsor licence + Skilled Worker gates before celebrating the offer.",
    ),
    "devops-sre-complete-resources": (
        "Production craft is never 'done' — this page is your ops bookmark bar.",
        "Audit the pass checklist. Pick one regional sprint if you're visa hunting.",
    ),
}


def _register_career_flavor(slug: str, title: str) -> tuple[str, str]:
    if slug.startswith("sp-"):
        if slug.endswith("-intro"):
            return (
                "Volvo, IFS, and peers — one employer path per target country.",
                "Link core sprint + regional elective + this sponsor path in your notes.",
            )
        if "volvo" in slug:
            return (
                "Automotive Azure platforms reward safety and traceability — not heroics.",
                "Whiteboard AKS pipeline + rollback in 15 minutes. Say safety aloud.",
            )
        if "ifs" in slug:
            return (
                "Enterprise SaaS ops — tenant isolation beats buzzword bingo.",
                "Prepare one SaaS incident STAR with customer-impact metrics.",
            )
        if slug.endswith("-checklist"):
            return (
                "Sponsor path checklist — visa + employer gates before you sign.",
                "Walk every box. Stop only when sponsor and visa route are verified.",
            )
    if slug.startswith("reloc-"):
        if slug.endswith("-intro"):
            return (
                "One elective, every discipline — visa culture without repeating five copies.",
                "Pick the core sprint you're running. Link this elective in your notes.",
            )
        if slug.endswith("-visa"):
            return (
                "Official immigration links beat forum rumors every time.",
                "Read the visa reference section. List three red flags from real job posts.",
            )
        if slug.endswith("-checklist"):
            return (
                "The checklist page — tick every box before you sign or relocate.",
                "Walk the pass checklist. Stop only when all gates are green.",
            )
    if "battle-plan" in slug:
        return (
            "Thirty days beats thirty tabs — this questline is your interview calendar.",
            "Block four weeks on your calendar. Screenshot it.",
        )
    if "visa-landscape" in slug:
        return (
            "Official immigration links beat forum rumors every time.",
            "Read the visa reference section. List three red flags from real job posts.",
        )
    if "complete-resources" in slug:
        return (
            "The checklist page — tick every box before you book interviews.",
            "Walk the pass checklist. Stop only when all gates are green.",
        )
    if "mock-final" in slug:
        return (
            "Mocks are dress rehearsal; rambling is the villain.",
            "Record one 20-minute technical mock. Listen once. Fix one thing.",
        )
    return (
        f"{title} — ship proof, not buzzwords.",
        "Write one interview answer you'll reuse. Say it aloud.",
    )


try:
    from .content.career_path_builder import all_career_roadmaps as _career_roadmaps
    from .content.sponsor_employer_paths import SPONSOR_ROADMAPS as _sponsor_roadmaps

    for _roadmap in (*_career_roadmaps(), *_sponsor_roadmaps):
        for _lesson in _roadmap["lessons"]:
            _slug = _lesson["slug"]
            if _slug not in FLAVOR:
                FLAVOR[_slug] = _register_career_flavor(_slug, _lesson["title"])
except Exception:  # noqa: BLE001 — keep static FLAVOR usable if generated packs fail
    pass


def flavor_for(lesson_slug: str) -> tuple[str, str]:
    return FLAVOR.get(
        lesson_slug,
        (
            "Clear this quest. Future-you on-call will send a thank-you PR.",
            "Write one sentence you'll remember in an interview. Say it out loud.",
        ),
    )
