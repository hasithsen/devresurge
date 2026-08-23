# DevResurge

Terminal-styled developer profiles — the technical README that complements LinkedIn.
Spin up a public profile, list your stack, attach projects, verify skills, link your career network.

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

License: MIT

## Features

- **Public profile** at `/u/<handle>/` — avatar, headline, bio, tech stack, **experience &
  education timeline**, projects, social links, peer recommendations, and quiz badges.
  Includes canonical link, `Person` JSON-LD, OpenGraph + Twitter cards (with avatar fallback).
  Handles are **case-insensitive**: they're stored lowercase, uniqueness is enforced at the DB
  with a `Lower("handle")` constraint, and `/u/Ada/` 301-redirects to the canonical `/u/ada/`.
  Bios render a **safe Markdown subset** (headings, lists, bold/italic, code, http(s)/mailto links).
  Link LinkedIn on your profile for a one-click bridge — DevResurge = signal, LinkedIn = network.
- **Open-to intents** — open to work, collaborate, mentor, or seeking mentorship, plus an optional
  note. Directory filters by intent so hiring managers and collaborators find the right people.
- **Peer skill endorsements** — accepted connections can vouch for skills on your stack (counts
  show publicly). Written **recommendations** from connections appear on your profile.
- **Owner dashboard** at `/me/` with self-service editors for profile, experience, education,
  projects, and links, a one-click copy-share-URL chip, a **profile readiness checklist**
  (`setup.sh`) that tracks what's still missing (including LinkedIn bridge), **README.md export**,
  and an embeddable **SVG badge** for GitHub READMEs.
- **Privacy-first analytics** at `/me/analytics/` — daily views, unique visitors, busiest day,
  referrer breakdown and **outbound link clicks** over a 7/30/90-day window, rendered as a
  dependency-free CSS bar chart. Visitors are tracked via a salted, irreversible fingerprint
  (never a raw IP); owner/bot hits are excluded. Link clicks are captured by a lightweight
  `navigator.sendBeacon` POST to `/c/`; the server derives the label/destination from its own
  records so payloads can't be spoofed. Events auto-expire after a **90-day retention window**
  (see `prune_analytics`).
- **Connections & notifications** — logged-in users send connection requests from any profile with a
  **relation label** (peer, collaborator, mentor, hiring, …) and optional note; the recipient
  accepts/declines from an in-app inbox at `/connections/notifications/` (unread badge in the
  navbar). Accepted links show editable relation status; either party can **block**. Accepting
  links both users, notifies the requester, and can unlock network badges. Emails are opt-out
  under `/users/~settings/`. An interactive **network map** at `/connections/map/` renders your
  ego graph (drag, zoom, relation filter, mutual edges between peers) with a JSON data endpoint
  for the canvas client.
- **Quizzes & achievement badges** — skill quizzes at `/quizzes/` (Python, Git, Django, SQL,
  JavaScript, HTTP/APIs, security basics — seeded via `seed_quizzes`). Pass at 80% to earn
  badges. Each badge has a **public linkable page** at `/quizzes/badges/<slug>/` with
  **LinkedIn / X / Reddit / email share buttons**, plus embeddable SVGs
  (`/quizzes/badges/<slug>.svg`, and a personal variant with your handle). Profile milestones
  (ready, shipper, open to work), network milestones (first link, networker), and quiz milestones
  (core streak, polyglot) award automatically.
- **Profile directory** at `/u/` with search, role filter, **open-to-work filter**, lazy-loaded
  avatars, pagination. Hireable profiles float to the top of the default listing.
- **SEO** — `/sitemap.xml` indexes public profiles + key static pages; `/robots.txt` points crawlers
  at it and blocks private surfaces (`/me/`, `/accounts/`, `/admin/`, …).
- **Mobile-first terminal UI** — JetBrains Mono, scanline overlay, prompt headers, blinking cursor.
- **Dark / light theme toggle** that respects `prefers-color-scheme` and persists in `localStorage`.
  Theme is applied **before first paint** to avoid the flash-of-wrong-theme. Toggle always visible
  in the navbar (no need to open the mobile menu first).
- **Auth out of the box** — email login, email verification, MFA via `django-allauth`, rate limits
  on signup / login / password reset, enumeration protection.
- **Hardened avatar uploads** — 2 MB cap, allowed-extension + MIME allowlist, live client-side
  preview and validation, fallback server-side `validate_avatar_size` + `FileExtensionValidator`.
- **Production-ready scaffolding** — Postgres, Redis, Whitenoise, Argon2, Docker compose for local + prod.

## Settings

Moved to [settings](https://cookiecutter-django.readthedocs.io/en/latest/1-getting-started/settings.html).

## Quickstart

```bash
docker compose -f docker-compose.local.yml up --build
docker compose -f docker-compose.local.yml run --rm django python manage.py migrate
docker compose -f docker-compose.local.yml run --rm django python manage.py createsuperuser
```

Then visit <http://localhost:8000>.

Local Compose runs migrations then `runserver_plus` on port 8000.

## Routes

| Path                                | What it does                       |
| ----------------------------------- | ---------------------------------- |
| `/`                                 | Terminal landing page              |
| `/health/`                          | Liveness probe (DB + cache)        |
| `/u/`                               | Public profile directory + search  |
| `/u/<handle>/`                      | A user's public profile            |
| `/u/<handle>/badge.svg`             | Embeddable SVG profile badge       |
| `/c/`                               | Link-click beacon (POST)           |
| `/connections/`                     | Your network + pending requests    |
| `/connections/map/`                 | Interactive network map            |
| `/connections/notifications/`       | In-app notification inbox          |
| `/quizzes/`                         | Skill quizzes                      |
| `/quizzes/badges/`                  | Badge catalog (public)             |
| `/quizzes/badges/<slug>/`           | Linkable badge detail + holders    |
| `/quizzes/badges/<slug>.svg`        | Embeddable achievement SVG         |
| `/quizzes/badges/<slug>/@<h>.svg`   | Personal earned-badge SVG          |
| `/quizzes/<slug>/` (+ take)         | Quiz detail + attempt              |
| `/users/~settings/`                 | Notification (email) preferences   |
| `/me/`                              | Owner dashboard                    |
| `/me/edit/`                         | Edit your profile                  |
| `/me/analytics/`                    | Views + link-click analytics (90d) |
| `/me/export/readme.md`              | Download profile as README.md      |
| `/me/experience/` (+ new/edit/delete) | Career timeline                    |
| `/me/education/` (+ new/edit/delete)  | Education entries                  |
| `/me/projects/` (+ new/edit/delete) | Manage project links               |
| `/me/links/` (+ new/edit/delete)    | Manage social / website links      |
| `/admin/`                           | Django admin                       |
| `/robots.txt`                       | Crawler rules                      |
| `/sitemap.xml`                      | Public profile + static sitemap    |

## Basic Commands

### Setting Up Your Users

- To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

- To create a **superuser account**, use this command:

      uv run python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

### Analytics retention

Analytics events — both profile views and outbound link clicks — are kept for 90
days. Production Compose runs an `analytics-prune` sidecar that calls
`prune_analytics` daily. For non-Compose hosts, schedule the same command
(cron, systemd timer, or Celery beat), e.g.:

    uv run python manage.py prune_analytics

Use `--days N` to override the window or `--dry-run` to preview what would be
deleted. The command prunes every analytics model and reports a per-model and
total count.

### Production env templates

Copy the checked-in examples and fill in real secrets (never commit them):

    mkdir -p .envs/.production
    cp .envs/.production/.django.example .envs/.production/.django
    cp .envs/.production/.postgres.example .envs/.production/.postgres

After HTTPS is confirmed through Traefik/your proxy, raise
`DJANGO_SECURE_HSTS_SECONDS` to `518400`. Enable
`DJANGO_SECURE_HSTS_PRELOAD=True` only when you intend to submit for browser
preload.

Production Compose runs `migrate` on Django boot, plus sidecars for analytics
pruning and daily Postgres backups. See [deployment/README.md](deployment/README.md)
for Traefik vs multi-host nginx-proxy setup.

### Quizzes & badges

After migrate, starter quizzes and achievement badges are seeded by the quizzes
migration. To re-seed or refresh question banks:

    uv run python manage.py seed_quizzes


### Type checks

Running type checks with mypy:

    uv run mypy devresurge

### Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report:

    uv run coverage run -m pytest
    uv run coverage html
    uv run open htmlcov/index.html

#### Running tests with pytest

    uv run pytest

### Live reloading and Sass CSS compilation

Moved to [Live reloading and SASS compilation](https://cookiecutter-django.readthedocs.io/en/latest/2-local-development/developing-locally.html#using-webpack-or-gulp).

## Deployment

The following details how to deploy this application.

### Docker

See [deployment/README.md](deployment/README.md) for production Compose, backups,
and multi-host nginx-proxy setup. General Cookiecutter Django Docker notes:
[deployment with Docker](https://cookiecutter-django.readthedocs.io/en/latest/3-deployment/deployment-with-docker.html).
