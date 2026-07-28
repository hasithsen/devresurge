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
        "slug": "quiz_typescript",
        "title": "Typed Edge",
        "description": "Passed the TypeScript essentials quiz.",
        "icon": "TS",
        "category": BadgeCategory.QUIZ,
        "order": 89,
    },
    {
        "slug": "quiz_css",
        "title": "Layout Solid",
        "description": "Passed the CSS & layout quiz.",
        "icon": "▤",
        "category": BadgeCategory.QUIZ,
        "order": 90,
    },
    {
        "slug": "quiz_linux",
        "title": "Shell Steady",
        "description": "Passed the Linux shell essentials quiz.",
        "icon": "$",
        "category": BadgeCategory.QUIZ,
        "order": 91,
    },
    {
        "slug": "quiz_docker",
        "title": "Container Cleared",
        "description": "Passed the containers & Docker quiz.",
        "icon": "⬡",
        "category": BadgeCategory.QUIZ,
        "order": 92,
    },
    {
        "slug": "quiz_testing",
        "title": "Test Proven",
        "description": "Passed the testing fundamentals quiz.",
        "icon": "✓",
        "category": BadgeCategory.QUIZ,
        "order": 93,
    },
    {
        "slug": "quiz_streak",
        "title": "Core Streak",
        "description": "Passed Python, Git, and Django quizzes.",
        "icon": "⚡",
        "category": BadgeCategory.MILESTONE,
        "order": 100,
    },
    {
        "slug": "quiz_frontend",
        "title": "Frontend Track",
        "description": "Passed JavaScript, CSS, and TypeScript quizzes.",
        "icon": "◈",
        "category": BadgeCategory.MILESTONE,
        "order": 105,
    },
    {
        "slug": "quiz_ops",
        "title": "Ops Track",
        "description": "Passed Linux, Docker, and testing quizzes.",
        "icon": "⚙",
        "category": BadgeCategory.MILESTONE,
        "order": 110,
    },
    {
        "slug": "quiz_polyglot",
        "title": "Polyglot",
        "description": "Passed five or more skill quizzes.",
        "icon": "◆",
        "category": BadgeCategory.MILESTONE,
        "order": 120,
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
    {
        "slug": "typescript-essentials",
        "title": "TypeScript essentials",
        "tagline": "Types that catch bugs before runtime.",
        "description": "Practical TypeScript for everyday app work. Pass to earn Typed Edge.",
        "topic": "typescript",
        "badge_slug": "quiz_typescript",
        "order": 80,
        "questions": [
            {
                "prompt": "What does `strictNullChecks` mainly prevent?",
                "explanation": "`null`/`undefined` are not assignable to other types unless declared.",
                "choices": [
                    ("All async code", False),
                    ("Silent null/undefined mistakes", True),
                    ("CSS imports", False),
                    ("Git merges", False),
                ],
            },
            {
                "prompt": "`interface User { id: number }` vs `type User = { id: number }` — key difference?",
                "explanation": "Interfaces can be declaration-merged; type aliases generally cannot.",
                "choices": [
                    ("Types are faster at runtime", False),
                    ("Interfaces can merge declarations", True),
                    ("Interfaces erase at compile time only for classes", False),
                    ("Types cannot describe objects", False),
                ],
            },
            {
                "prompt": "Best fit for `unknown` over `any`?",
                "explanation": "`unknown` forces narrowing before use; `any` disables checking.",
                "choices": [
                    ("Disable all type checks", False),
                    ("Accept a value, then narrow before using it", True),
                    ("Mark private fields", False),
                    ("Speed up the compiler", False),
                ],
            },
            {
                "prompt": "What does `Readonly<T>` do?",
                "explanation": "It makes all properties of `T` readonly in the type system.",
                "choices": [
                    ("Freezes the object at runtime always", False),
                    ("Makes properties readonly for type-checking", True),
                    ("Converts T to a Promise", False),
                    ("Removes optional keys", False),
                ],
            },
            {
                "prompt": "A discriminated union is useful when…",
                "explanation": "A shared literal field (discriminant) lets TypeScript narrow variants safely.",
                "choices": [
                    ("Every object is identical", False),
                    ("Variants share a literal tag field", True),
                    ("You only use `any`", False),
                    ("You avoid switch/if entirely", False),
                ],
            },
        ],
    },
    {
        "slug": "css-layout",
        "title": "CSS & layout",
        "tagline": "Flex, grid, cascade, and responsive basics.",
        "description": "Layout fluency for modern UI. Pass to earn Layout Solid.",
        "topic": "css",
        "badge_slug": "quiz_css",
        "order": 90,
        "questions": [
            {
                "prompt": "In flexbox, `justify-content` mainly controls…",
                "explanation": "Main-axis alignment of flex items (row → horizontal by default).",
                "choices": [
                    ("Stacking context only", False),
                    ("Alignment along the main axis", True),
                    ("Font smoothing", False),
                    ("Z-index automatically", False),
                ],
            },
            {
                "prompt": "`display: grid` with `grid-template-columns: 1fr 2fr` means…",
                "explanation": "Two columns; the second gets twice the free space of the first.",
                "choices": [
                    ("Fixed 1px and 2px columns", False),
                    ("Two columns, second twice as wide (fractional)", True),
                    ("Always 100% width each", False),
                    ("Columns collapse on mobile only", False),
                ],
            },
            {
                "prompt": "Which unit scales with the viewport width?",
                "explanation": "`vw` is 1% of the viewport width.",
                "choices": [
                    ("em", False),
                    ("vw", True),
                    ("ch", False),
                    ("lh", False),
                ],
            },
            {
                "prompt": "Cascade: all else equal, which wins?",
                "explanation": "More specific selectors beat less specific ones (then source order).",
                "choices": [
                    ("The stylesheet loaded first always", False),
                    ("Higher specificity (then later source order)", True),
                    ("Inline styles never win", False),
                    ("IDs are ignored", False),
                ],
            },
            {
                "prompt": "A mobile-first breakpoint typically uses…",
                "explanation": "Base styles for small screens; `min-width` media queries enhance upward.",
                "choices": [
                    ("Only `max-width` with desktop defaults", False),
                    ("Base mobile styles + `min-width` queries", True),
                    ("No media queries ever", False),
                    ("`orientation` only", False),
                ],
            },
        ],
    },
    {
        "slug": "linux-shell",
        "title": "Linux shell essentials",
        "tagline": "Paths, pipes, permissions, and processes.",
        "description": "CLI fluency for debugging and deploys. Pass to earn Shell Steady.",
        "topic": "linux",
        "badge_slug": "quiz_linux",
        "order": 100,
        "questions": [
            {
                "prompt": "`chmod 644 file` sets permissions to…",
                "explanation": "Owner rw, group r, others r (no execute).",
                "choices": [
                    ("rwx for everyone", False),
                    ("rw-r--r--", True),
                    ("r-x--x--x", False),
                    ("Only owner execute", False),
                ],
            },
            {
                "prompt": "What does `cmd1 | cmd2` do?",
                "explanation": "stdout of cmd1 becomes stdin of cmd2.",
                "choices": [
                    ("Runs cmd2 only on failure", False),
                    ("Pipes stdout of cmd1 into cmd2", True),
                    ("Backgrounds both", False),
                    ("Compares the two binaries", False),
                ],
            },
            {
                "prompt": "`grep -R \"TODO\" .` is best described as…",
                "explanation": "Recursive search for the pattern under the current directory.",
                "choices": [
                    ("Delete matching files", False),
                    ("Recursively search for a pattern", True),
                    ("Replace TODO in git history", False),
                    ("Compile TypeScript", False),
                ],
            },
            {
                "prompt": "Which signal is commonly used for graceful shutdown?",
                "explanation": "SIGTERM asks a process to terminate cleanly; SIGKILL cannot be caught.",
                "choices": [
                    ("SIGKILL only", False),
                    ("SIGTERM", True),
                    ("SIGSTOP forever", False),
                    ("SIGHUP always reboots the host", False),
                ],
            },
            {
                "prompt": "`2>` redirects…",
                "explanation": "File descriptor 2 is stderr.",
                "choices": [
                    ("stdout", False),
                    ("stderr", True),
                    ("stdin", False),
                    ("the exit code", False),
                ],
            },
        ],
    },
    {
        "slug": "containers-docker",
        "title": "Containers & Docker",
        "tagline": "Images, layers, and runtime hygiene.",
        "description": "Ship the same artifact everywhere. Pass to earn Container Cleared.",
        "topic": "docker",
        "badge_slug": "quiz_docker",
        "order": 110,
        "questions": [
            {
                "prompt": "An image vs a container — which is true?",
                "explanation": "Images are immutable templates; containers are running (or stopped) instances.",
                "choices": [
                    ("They are identical terms", False),
                    ("Image is the template; container is a running instance", True),
                    ("Containers cannot be stopped", False),
                    ("Images include the live process table", False),
                ],
            },
            {
                "prompt": "Why prefer a non-root user in production containers?",
                "explanation": "Least privilege reduces blast radius if the process is compromised.",
                "choices": [
                    ("Faster builds only", False),
                    ("Limits privilege if the app is compromised", True),
                    ("Required by the Docker daemon always", False),
                    ("Disables networking", False),
                ],
            },
            {
                "prompt": "A multi-stage Dockerfile mainly helps you…",
                "explanation": "Build with a fat toolchain image, then copy artifacts into a slim runtime image.",
                "choices": [
                    ("Run two OS kernels", False),
                    ("Keep build tools out of the final image", True),
                    ("Skip layer caching forever", False),
                    ("Avoid tagging images", False),
                ],
            },
            {
                "prompt": "`COPY` vs `ADD` in Dockerfiles — prefer COPY when…",
                "explanation": "COPY is explicit for local files; ADD has extra magic (URLs, auto-extract).",
                "choices": [
                    ("You always need remote URL fetching", False),
                    ("You just need local files without archive magic", True),
                    ("You want automatic `chmod +x`", False),
                    ("COPY cannot use build context", False),
                ],
            },
            {
                "prompt": "Bind-mounting a host directory into a container means…",
                "explanation": "Changes are shared with the host path — useful for dev, risky for secrets.",
                "choices": [
                    ("The directory is copied once at build time only", False),
                    ("Host and container share that path live", True),
                    ("Networking is disabled", False),
                    ("The image becomes read-only forever", False),
                ],
            },
        ],
    },
    {
        "slug": "testing-fundamentals",
        "title": "Testing fundamentals",
        "tagline": "What to test, how to isolate, when to stop.",
        "description": "Practical testing judgment for shipping with confidence. Pass to earn Test Proven.",
        "topic": "testing",
        "badge_slug": "quiz_testing",
        "order": 120,
        "questions": [
            {
                "prompt": "A unit test should ideally…",
                "explanation": "Fast, focused, and isolated from flaky I/O when possible.",
                "choices": [
                    ("Hit production databases always", False),
                    ("Exercise a small unit with controlled inputs", True),
                    ("Only run yearly", False),
                    ("Replace code review entirely", False),
                ],
            },
            {
                "prompt": "What is a test double (mock/stub/fake) for?",
                "explanation": "Replace a dependency so you can control behavior and keep tests fast/deterministic.",
                "choices": [
                    ("Encrypt fixtures", False),
                    ("Stand in for a dependency under test control", True),
                    ("Generate CSS", False),
                    ("Bump semver automatically", False),
                ],
            },
            {
                "prompt": "Flaky tests usually hurt most because they…",
                "explanation": "Erode trust — teams ignore failures, then miss real regressions.",
                "choices": [
                    ("Make CI faster", False),
                    ("Train teams to ignore red builds", True),
                    ("Improve coverage metrics only", False),
                    ("Prove eventual consistency", False),
                ],
            },
            {
                "prompt": "Arrange–Act–Assert structure means…",
                "explanation": "Set up, perform the behavior, then verify outcomes — keeps tests readable.",
                "choices": [
                    ("Deploy, monitor, rollback", False),
                    ("Setup, exercise, verify", True),
                    ("Lint, format, commit", False),
                    ("Build, ship, celebrate", False),
                ],
            },
            {
                "prompt": "Prefer testing behavior over implementation details so that…",
                "explanation": "Refactors that preserve behavior should not force mass test rewrites.",
                "choices": [
                    ("Tests break on every rename of a private helper", False),
                    ("Refactors keep tests green when behavior is unchanged", True),
                    ("You never write assertions", False),
                    ("Coverage must be 100% of lines always", False),
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
