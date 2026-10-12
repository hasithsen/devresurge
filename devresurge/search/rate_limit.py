"""Soft IP rate limiting via the Django cache (Redis in production)."""

from __future__ import annotations

from django.core.cache import cache
from django.http import HttpRequest


def client_ip(request: HttpRequest) -> str:
    forwarded = (request.META.get("HTTP_X_FORWARDED_FOR") or "").split(",")[0].strip()
    return forwarded or (request.META.get("REMOTE_ADDR") or "unknown")


def is_rate_limited(
    request: HttpRequest,
    *,
    prefix: str,
    limit: int,
    window_seconds: int,
) -> bool:
    """Return True when the caller exceeded ``limit`` hits in ``window_seconds``."""
    if limit <= 0:
        return False
    key = f"{prefix}:{client_ip(request)}"
    try:
        count = cache.incr(key)
    except ValueError:
        cache.set(key, 1, window_seconds)
        return False
    return count > limit
