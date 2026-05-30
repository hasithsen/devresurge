# DevResurge

Terminal-styled developer profiles for the IT crowd. Spin up a public profile, list
your stack, attach projects, link your socials.

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

License: MIT

## Features

- **Public profile** at `/p/<handle>/` — avatar, headline, bio, tech stack, projects, social links.
  Includes canonical link, `Person` JSON-LD, OpenGraph + Twitter cards (with avatar fallback).
- **Owner dashboard** at `/me/` with self-service editors for profile, projects, and links and a
  one-click copy-share-URL chip.
- **Profile directory** at `/p/` with search + role filter, lazy-loaded avatars, pagination.
- **Mobile-first terminal UI** — JetBrains Mono, scanline overlay, prompt headers, blinking cursor.
- **Dark / light theme toggle** that respects `prefers-color-scheme` and persists in `localStorage`.
  Theme is applied **before first paint** to avoid the flash-of-wrong-theme. Toggle always visible
  in the navbar (no need to open the mobile menu first).
- **Auth out of the box** — email login, email verification, MFA via `django-allauth`, rate limits
  on signup / login / password reset, enumeration protection.
- **Hardened avatar uploads** — 2 MB cap, allowed-extension + MIME allowlist, live client-side
  preview and validation, fallback server-side `validate_avatar_size` + `FileExtensionValidator`.
- **`/robots.txt`** auto-served with sensible defaults (allows `/p/...` indexing, blocks `/me/`,
  `/accounts/` and `/admin/`).
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

## Routes

| Path                                | What it does                       |
| ----------------------------------- | ---------------------------------- |
| `/`                                 | Terminal landing page              |
| `/p/`                               | Public profile directory + search  |
| `/p/<handle>/`                      | A user's public profile            |
| `/me/`                              | Owner dashboard                    |
| `/me/edit/`                         | Edit your profile                  |
| `/me/projects/` (+ new/edit/delete) | Manage project links               |
| `/me/links/` (+ new/edit/delete)    | Manage social / website links      |
| `/admin/`                           | Django admin                       |
| `/robots.txt`                       | Crawler rules                      |

## Basic Commands

### Setting Up Your Users

- To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

- To create a **superuser account**, use this command:

      uv run python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

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

See detailed [cookiecutter-django Docker documentation](https://cookiecutter-django.readthedocs.io/en/latest/3-deployment/deployment-with-docker.html).
