from __future__ import annotations

from .models import Notification


def notifications(request):
    """Expose the unread notification count to all templates (navbar badge)."""
    user = getattr(request, "user", None)
    if user is None or not user.is_authenticated:
        return {}
    return {
        "unread_notification_count": (
            Notification.objects.for_user(user).unread().count()
        ),
    }
