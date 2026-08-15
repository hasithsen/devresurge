from __future__ import annotations

from django.core.cache import cache

from .models import Notification

_UNREAD_CACHE_TTL = 45


def unread_count_cache_key(user_id: int) -> str:
    return f"notif:unread:{user_id}"


def invalidate_unread_count(user_id: int | None) -> None:
    if user_id is None:
        return
    cache.delete(unread_count_cache_key(user_id))


def notifications(request):
    """Expose the unread notification count to all templates (navbar badge)."""
    user = getattr(request, "user", None)
    if user is None or not user.is_authenticated:
        return {}
    cache_key = unread_count_cache_key(user.pk)
    count = cache.get(cache_key)
    if count is None:
        count = Notification.objects.for_user(user).unread().count()
        cache.set(cache_key, count, _UNREAD_CACHE_TTL)
    return {"unread_notification_count": count}
