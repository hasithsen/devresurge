"""Seed catalog: quizzes, questions, choices, and achievement badges."""

from __future__ import annotations

from django.db import transaction

from .models import Badge
from .models import BadgeCategory
from .models import Choice
from .models import Question
from .models import Quiz

BADGE_CATALOG: list[dict] = [
    {
        "slug": "profile_ready",
        "title": "Profile Ready",
        "description": "Completed every item on the setup.sh checklist.",
        "icon": "▣",
        "category": BadgeCategory.PROFILE,
        "order": 10,
    },
    {
        "slug": "open_to_work",
        "title": "Open to Work",
        "description": "Marked available for hire on a public profile.",
        "icon": "◉",
        "category": BadgeCategory.PROFILE,
        "order": 20,
    },
    {
        "slug": "shipper",
        "title": "Shipper",
        "description": "Listed three or more projects.",
        "icon": "▲",
        "category": BadgeCategory.PROFILE,
        "order": 30,
    },
    {
        "slug": "first_link",
        "title": "First Link",
        "description": "Accepted your first connection.",
        "icon": "⇄",
        "category": BadgeCategory.NETWORK,
        "order": 40,
    },
    {
        "slug": "networker",
        "title": "Networker",
        "description": "Grew your network to five accepted connections.",
        "icon": "▦",
        "category": BadgeCategory.NETWORK,
        "order": 50,
    },
    {
        "slug": "quiz_python",
        "title": "Python Pulse",
        "description": "Passed the Python fundamentals quiz.",
        "icon": "π",
        "category": BadgeCategory.QUIZ,
        "order": 60,
    },
    {
        "slug": "quiz_git",
        "title": "Git Fluent",
        "description": "Passed the Git & collaboration quiz.",
        "icon": "⎇",
        "category": BadgeCategory.QUIZ,
        "order": 70,
    },
    {
        "slug": "quiz_django",
        "title": "Django Drift",
        "description": "Passed the Django basics quiz.",
        "icon": "◈",
        "category": BadgeCategory.QUIZ,
        "order": 80,
    },
    {
        "slug": "quiz_sql",
        "title": "SQL Solid",
        "description": "Passed the SQL fundamentals quiz.",
        "icon": "⊆",
        "category": BadgeCategory.QUIZ,
        "order": 85,
    },
    {
        "slug": "quiz_js",
        "title": "JS Current",
        "description": "Passed the JavaScript essentials quiz.",
        "icon": "{}",
        "category": BadgeCategory.QUIZ,
        "order": 86,
    },
    {
        "slug": "quiz_http",
        "title": "HTTP Fluent",
        "description": "Passed the HTTP & APIs quiz.",
        "icon": "⇄",
        "category": BadgeCategory.QUIZ,
        "order": 87,
    },
    {
        "slug": "quiz_security",
        "title": "Secure Baseline",
        "description": "Passed the web security basics quiz.",
        "icon": "⛨",
        "category": BadgeCategory.QUIZ,
        "order": 88,
    },
    {
        "slug": "quiz_streak",
        "title": "Core Streak",
        "description": "Passed Python, Git, and Django quizzes.",
        "icon": "⚡",
        "category": BadgeCategory.MILESTONE,
        "order": 90,
    },
    {
        "slug": "quiz_polyglot",
        "title": "Polyglot",
        "description": "Passed five or more skill quizzes.",
        "icon": "◆",
        "category": BadgeCategory.MILESTONE,
        "order": 95,
    },
]

QUIZ_CATALOG: list[dict] = [
    {
        "slug": "python-fundamentals",
        "title": "Python fundamentals",
        "tagline": "Lists, dicts, and the stuff you use every day.",
        "description": "A quick pulse check on core Python. Pass at 80% to earn Python Pulse.",
        "topic": "python",
        "badge_slug": "quiz_python",
        "order": 10,
        "questions": [
            {
                "prompt": "What does `len({1, 2, 2, 3})` return?",
                "explanation": "Sets de-duplicate; `{1, 2, 2, 3}` has three unique values.",
                "choices": [
                    ("2", False),
                    ("3", True),
                    ("4", False),
                    ("TypeError", False),
                ],
            },
            {
                "prompt": "Which creates a new list with squares of 1..3?",
                "explanation": "`[x * x for x in range(1, 4)]` is a list comprehension.",
                "choices": [
                    ("{x*x for x in range(1,4)}", False),
                    ("[x*x for x in range(1,4)]", True),
                    ("(x*x for x in range(1,4))", False),
                    ("map(square, 1..3)", False),
                ],
            },
            {
                "prompt": "What is the output of `bool([])`?",
                "explanation": "Empty containers are falsy in Python.",
                "choices": [
                    ("True", False),
                    ("False", True),
                    ("None", False),
                    ("[]", False),
                ],
            },
            {
                "prompt": "Which keyword defines a generator function?",
                "explanation": "Using `yield` makes a function a generator.",
                "choices": [
                    ("async", False),
                    ("yield", True),
                    ("defer", False),
                    ("gen", False),
                ],
            },
            {
                "prompt": "`dict.get('x', 0)` when key is missing returns…",
                "explanation": "`.get` returns the default instead of raising KeyError.",
                "choices": [
                    ("KeyError", False),
                    ("None", False),
                    ("0", True),
                    ("'x'", False),
                ],
            },
        ],
    },
    {
        "slug": "git-collaboration",
        "title": "Git & collaboration",
        "tagline": "Branching, history, and not rewriting shared main.",
        "description": "Everyday Git hygiene for working with a team.",
        "topic": "git",
        "badge_slug": "quiz_git",
        "order": 20,
        "questions": [
            {
                "prompt": "Which command stages all tracked modifications?",
                "explanation": "`git add -u` stages updates to tracked files.",
                "choices": [
                    ("git commit -a", False),
                    ("git add -u", True),
                    ("git stage --all", False),
                    ("git update", False),
                ],
            },
            {
                "prompt": "A safe way to update a feature branch with main is…",
                "explanation": "Rebase (or merge) locally; avoid force-pushing shared main.",
                "choices": [
                    ("git push --force origin main", False),
                    ("git rebase main", True),
                    ("git reset --hard origin/main", False),
                    ("git clean -fdx", False),
                ],
            },
            {
                "prompt": "`git status` shows a file as untracked. First step?",
                "explanation": "Untracked files must be added before commit.",
                "choices": [
                    ("git commit -m '…'", False),
                    ("git add <file>", True),
                    ("git push", False),
                    ("git stash drop", False),
                ],
            },
            {
                "prompt": "What does a pull request (MR) primarily enable?",
                "explanation": "Code review and discussion before merging.",
                "choices": [
                    ("Automatic production deploys only", False),
                    ("Peer review before merge", True),
                    ("Deleting the remote", False),
                    ("Rewriting author history", False),
                ],
            },
            {
                "prompt": "Which history is generally considered immutable on shared main?",
                "explanation": "Don't force-push rewritten commits to protected shared branches.",
                "choices": [
                    ("Your private scratch branch", False),
                    ("Protected main/master", True),
                    ("A local WIP commit", False),
                    ("Stash entries", False),
                ],
            },
        ],
    },
    {
        "slug": "django-basics",
        "title": "Django basics",
        "tagline": "Models, views, and the request/response loop.",
        "description": "Core Django concepts for profile-platform builders.",
        "topic": "django",
        "badge_slug": "quiz_django",
        "order": 30,
        "questions": [
            {
                "prompt": "Which layer maps URLs to callables?",
                "explanation": "URLconf / path() routes requests to views.",
                "choices": [
                    ("Middleware", False),
                    ("URLconf", True),
                    ("Template tags", False),
                    ("Migrations", False),
                ],
            },
            {
                "prompt": "A ModelForm primarily helps you…",
                "explanation": "ModelForms generate and validate forms from models.",
                "choices": [
                    ("Serve static files", False),
                    ("Build forms from models", True),
                    ("Run Celery tasks", False),
                    ("Compile Sass", False),
                ],
            },
            {
                "prompt": "`migrate` applies…",
                "explanation": "Migrations change the database schema.",
                "choices": [
                    ("Template caches", False),
                    ("Database schema changes", True),
                    ("CSS bundles", False),
                    ("Email outbox", False),
                ],
            },
            {
                "prompt": "Which is the correct place for per-request auth user?",
                "explanation": "`request.user` is set by AuthenticationMiddleware.",
                "choices": [
                    ("request.session['user'] only", False),
                    ("request.user", True),
                    ("settings.AUTH_USER", False),
                    ("os.environ['USER']", False),
                ],
            },
            {
                "prompt": "CSRF protection is most relevant for…",
                "explanation": "State-changing POST/PUT/DELETE from browsers need CSRF tokens.",
                "choices": [
                    ("GET asset downloads", False),
                    ("Browser form POSTs", True),
                    ("Static file MIME types", False),
                    ("Database indexes", False),
                ],
            },
        ],
    },
    {
        "slug": "sql-fundamentals",
        "title": "SQL fundamentals",
        "tagline": "SELECT with intent — joins, nulls, and indexes.",
        "description": "Everyday SQL for backend and data work. Pass to earn SQL Solid.",
        "topic": "sql",
        "badge_slug": "quiz_sql",
        "order": 40,
        "questions": [
            {
                "prompt": "Which clause filters rows before aggregation?",
                "explanation": "WHERE filters rows; HAVING filters groups after GROUP BY.",
                "choices": [
                    ("HAVING", False),
                    ("WHERE", True),
                    ("ORDER BY", False),
                    ("LIMIT", False),
                ],
            },
            {
                "prompt": "`NULL = NULL` evaluates to…",
                "explanation": "Comparisons with NULL yield UNKNOWN; use IS NULL.",
                "choices": [
                    ("TRUE", False),
                    ("FALSE", False),
                    ("UNKNOWN / NULL", True),
                    ("1", False),
                ],
            },
            {
                "prompt": "An INNER JOIN returns…",
                "explanation": "Only rows with matches in both tables.",
                "choices": [
                    ("All rows from the left table", False),
                    ("Only matching rows from both tables", True),
                    ("A Cartesian product always", False),
                    ("Duplicates removed automatically", False),
                ],
            },
            {
                "prompt": "A good reason to add an index is…",
                "explanation": "Indexes speed selective lookups; they cost write overhead.",
                "choices": [
                    ("Every column should be indexed", False),
                    ("Frequent equality/range filters on large tables", True),
                    ("To store JSON faster", False),
                    ("To replace primary keys", False),
                ],
            },
            {
                "prompt": "`COUNT(*)` vs `COUNT(col)` — what's different?",
                "explanation": "COUNT(col) skips NULLs in that column; COUNT(*) counts rows.",
                "choices": [
                    ("They are identical always", False),
                    ("COUNT(col) ignores NULL values in col", True),
                    ("COUNT(*) ignores NULL rows", False),
                    ("COUNT(col) is slower by definition", False),
                ],
            },
        ],
    },
    {
        "slug": "javascript-essentials",
        "title": "JavaScript essentials",
        "tagline": "Types, async, and the DOM-adjacent mental model.",
        "description": "Core JS for full-stack folks. Pass to earn JS Current.",
        "topic": "javascript",
        "badge_slug": "quiz_js",
        "order": 50,
        "questions": [
            {
                "prompt": "`typeof null` returns…",
                "explanation": "Historical quirk: typeof null === 'object'.",
                "choices": [
                    ("'null'", False),
                    ("'object'", True),
                    ("'undefined'", False),
                    ("'nil'", False),
                ],
            },
            {
                "prompt": "Which compares without type coercion?",
                "explanation": "=== is strict equality.",
                "choices": [
                    ("==", False),
                    ("===", True),
                    ("=", False),
                    ("!=", False),
                ],
            },
            {
                "prompt": "`const` means…",
                "explanation": "Binding can't be reassigned; object contents can still mutate.",
                "choices": [
                    ("Value is deeply immutable", False),
                    ("Binding cannot be reassigned", True),
                    ("Variable is function-scoped only", False),
                    ("Hoisted as undefined", False),
                ],
            },
            {
                "prompt": "A Promise rejected without .catch…",
                "explanation": "Unhandled rejections surface as errors/warnings.",
                "choices": [
                    ("Is silently ignored forever", False),
                    ("Becomes an unhandled rejection", True),
                    ("Retries automatically", False),
                    ("Converts to null", False),
                ],
            },
            {
                "prompt": "`Array.prototype.map` returns…",
                "explanation": "map builds a new array from transformed elements.",
                "choices": [
                    ("The same array mutated", False),
                    ("A new array", True),
                    ("A single reduced value", False),
                    ("An iterator only", False),
                ],
            },
        ],
    },
    {
        "slug": "http-apis",
        "title": "HTTP & APIs",
        "tagline": "Status codes, methods, and idempotency.",
        "description": "How the web talks. Pass to earn HTTP Fluent.",
        "topic": "http",
        "badge_slug": "quiz_http",
        "order": 60,
        "questions": [
            {
                "prompt": "Which status means created successfully?",
                "explanation": "201 Created is typical after a successful POST that makes a resource.",
                "choices": [
                    ("200", False),
                    ("201", True),
                    ("204", False),
                    ("304", False),
                ],
            },
            {
                "prompt": "Idempotent HTTP methods include…",
                "explanation": "GET, PUT, DELETE are idempotent; POST generally is not.",
                "choices": [
                    ("POST only", False),
                    ("GET and PUT", True),
                    ("PATCH only", False),
                    ("CONNECT", False),
                ],
            },
            {
                "prompt": "401 vs 403 — which is which?",
                "explanation": "401 unauthenticated; 403 authenticated but not allowed.",
                "choices": [
                    ("401 forbidden, 403 unauthorized", False),
                    ("401 unauthenticated, 403 forbidden", True),
                    ("Both mean not found", False),
                    ("403 means redirect", False),
                ],
            },
            {
                "prompt": "Cache-Control: no-store means…",
                "explanation": "Caches must not store the response.",
                "choices": [
                    ("Revalidate every time only", False),
                    ("Do not store the response", True),
                    ("Store forever", False),
                    ("Compress the body", False),
                ],
            },
            {
                "prompt": "REST-ish APIs usually identify resources via…",
                "explanation": "Nouns in the path; verbs via HTTP methods.",
                "choices": [
                    ("RPC method names in every path", False),
                    ("Resource URLs + HTTP methods", True),
                    ("Only query strings", False),
                    ("WebSockets exclusively", False),
                ],
            },
        ],
    },
    {
        "slug": "security-basics",
        "title": "Web security basics",
        "tagline": "XSS, CSRF, secrets, and least privilege.",
        "description": "Baseline defenses every builder should know. Pass to earn Secure Baseline.",
        "topic": "security",
        "badge_slug": "quiz_security",
        "order": 70,
        "questions": [
            {
                "prompt": "Primary defense against stored XSS in HTML pages?",
                "explanation": "Escape/encode untrusted output (and use CSP as defense in depth).",
                "choices": [
                    ("Disable HTTPS", False),
                    ("Context-aware output encoding", True),
                    ("Longer passwords only", False),
                    ("Open CORS to *", False),
                ],
            },
            {
                "prompt": "CSRF tokens matter most for…",
                "explanation": "Cookie-authenticated state-changing browser requests.",
                "choices": [
                    ("Public CDN GETs", False),
                    ("Cookie-auth form POSTs", True),
                    ("Static image loads", False),
                    ("DNS lookups", False),
                ],
            },
            {
                "prompt": "Where should production secrets live?",
                "explanation": "Env / secret manager — never commit to git.",
                "choices": [
                    ("Committed .env in git", False),
                    ("Environment / secret manager", True),
                    ("Public README", False),
                    ("Client-side JS", False),
                ],
            },
            {
                "prompt": "Principle of least privilege means…",
                "explanation": "Grant only the access needed to do the job.",
                "choices": [
                    ("Everyone is admin for speed", False),
                    ("Minimal necessary permissions", True),
                    ("Disable logging", False),
                    ("Share one DB user everywhere", False),
                ],
            },
            {
                "prompt": "Password storage should use…",
                "explanation": "Slow adaptive hashes (Argon2, bcrypt, scrypt) — not plain SHA.",
                "choices": [
                    ("Plaintext with TLS only", False),
                    ("Adaptive password hashing (e.g. Argon2)", True),
                    ("MD5", False),
                    ("Base64", False),
                ],
            },
        ],
    },
]


@transaction.atomic
def seed_catalog(*, refresh_questions: bool = True) -> dict[str, int]:
    """Upsert badges + quizzes. Returns counts of created/updated rows."""
    created = {"badges": 0, "quizzes": 0, "questions": 0}

    for entry in BADGE_CATALOG:
        _, was_created = Badge.objects.update_or_create(
            slug=entry["slug"],
            defaults={
                "title": entry["title"],
                "description": entry["description"],
                "icon": entry["icon"],
                "category": entry["category"],
                "order": entry["order"],
                "is_active": True,
            },
        )
        if was_created:
            created["badges"] += 1

    for quiz_data in QUIZ_CATALOG:
        questions = quiz_data["questions"]
        quiz, was_created = Quiz.objects.update_or_create(
            slug=quiz_data["slug"],
            defaults={
                "title": quiz_data["title"],
                "tagline": quiz_data["tagline"],
                "description": quiz_data["description"],
                "topic": quiz_data["topic"],
                "badge_slug": quiz_data["badge_slug"],
                "order": quiz_data["order"],
                "pass_percent": 80,
                "is_published": True,
            },
        )
        if was_created:
            created["quizzes"] += 1

        if refresh_questions:
            quiz.questions.all().delete()
            for q_idx, q in enumerate(questions):
                question = Question.objects.create(
                    quiz=quiz,
                    prompt=q["prompt"],
                    explanation=q.get("explanation", ""),
                    order=q_idx,
                )
                created["questions"] += 1
                for c_idx, (label, is_correct) in enumerate(q["choices"]):
                    Choice.objects.create(
                        question=question,
                        label=label,
                        is_correct=is_correct,
                        order=c_idx,
                    )

    return created
