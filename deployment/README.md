# Production deployment

## Single-host (Traefik)

Use `docker-compose.production.yml` from the project root. Traefik terminates TLS and
routes traffic to Gunicorn; the bundled Nginx container serves `/media/` only.

```bash
mkdir -p .envs/.production
cp .envs/.production/.django.example .envs/.production/.django
cp .envs/.production/.postgres.example .envs/.production/.postgres
# Edit both files — replace every placeholder secret.

docker compose -f docker-compose.production.yml up -d --build
```

The Django start script runs `migrate` and `collectstatic` on boot. Sidecars:

- `analytics-prune` — daily `prune_analytics`
- `postgres-backup` — daily `pg_dump` into the `*_postgres_data_backups` volume

Manual backup: `docker compose -f docker-compose.production.yml exec postgres backup`

## Multi-host (external nginx-proxy)

Use `docker-compose.production.multi.yml` when Traefik runs elsewhere. Copy
`deployment/nginx-proxy/conf.d/devresurge.conf` into your host nginx `conf.d/` and
adjust certificate paths. Ensure the external network `nginx_proxy_network` exists:

```bash
docker network create nginx_proxy_network
```

## Post-deploy checklist

1. Confirm HTTPS end-to-end, then raise `DJANGO_SECURE_HSTS_SECONDS` to `518400`.
2. Set `DJANGO_SECURE_HSTS_PRELOAD=True` only if submitting for browser preload.
3. Use a non-guessable `DJANGO_ADMIN_URL`.
4. Verify `/health/` returns `200` with `database` and `cache` checks ok.
5. Restore-test a Postgres backup from the backups volume.
