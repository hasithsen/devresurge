"""Lightweight readiness probes for load balancers and Compose healthchecks."""

from __future__ import annotations

import logging

from django.core.cache import cache
from django.db import connection
from django.http import HttpRequest
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.http import require_GET

logger = logging.getLogger(__name__)


@require_GET
def health_view(_request: HttpRequest) -> HttpResponse:
    """Return 200 when the process can reach Postgres (and cache when configured).

    Intentionally unauthenticated and side-effect free aside from a tiny cache
    touch so orchestrators can probe without credentials.
    """
    checks: dict[str, str] = {}
    try:
        connection.ensure_connection()
        checks["database"] = "ok"
    except Exception:  # noqa: BLE001 — log internally; never leak probe details
        logger.exception("Health check: database probe failed")
        return JsonResponse(
            {"status": "error", "checks": {"database": "unavailable"}},
            status=503,
        )

    try:
        cache.set("healthcheck", "1", 5)
        if cache.get("healthcheck") != "1":
            raise RuntimeError("cache round-trip failed")
        checks["cache"] = "ok"
    except Exception:  # noqa: BLE001
        # Cache is optional for process liveness; report degraded but stay up.
        logger.exception("Health check: cache probe failed")
        checks["cache"] = "degraded"

    return JsonResponse({"status": "ok", "checks": checks})
