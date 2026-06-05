from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse

from .models import NotificationKind

if TYPE_CHECKING:
    from django.http import HttpRequest

    from .models import Notification

logger = logging.getLogger(__name__)

# Maps a notification kind to its e-mail template bundle (subject/text/html).
_TEMPLATES = {
    NotificationKind.CONNECTION_REQUEST: "connections/email/connection_request",
    NotificationKind.CONNECTION_ACCEPTED: "connections/email/connection_accepted",
}


def _absolute(request: HttpRequest | None, path: str) -> str:
    if request is not None:
        return request.build_absolute_uri(path)
    # Fallback when no request is available (e.g. management commands).
    base = getattr(settings, "DEFAULT_SITE_URL", "").rstrip("/")
    return f"{base}{path}" if base else path


def send_notification_email(
    notification: Notification,
    request: HttpRequest | None = None,
) -> bool:
    """Email the recipient about a notification, respecting their preference.

    Returns True if an email was handed to the backend, False if it was skipped
    (opted out, no address, or unknown kind). Never raises — delivery failures
    are logged so they can't break the triggering request.
    """
    recipient = notification.recipient
    if not getattr(recipient, "email_notifications", True):
        return False
    if not recipient.email:
        return False

    template_base = _TEMPLATES.get(notification.kind)
    if template_base is None:
        return False

    actor = notification.actor
    actor_name = ""
    if actor is not None:
        actor_profile = getattr(actor, "profile", None)
        actor_name = (
            (actor_profile.display_name if actor_profile else "")
            or actor.name
            or actor.email
        )

    context = {
        "recipient": recipient,
        "recipient_name": recipient.name or recipient.email,
        "actor": actor,
        "actor_name": actor_name,
        "notification": notification,
        "connections_url": _absolute(request, reverse("connections:notifications")),
        "settings_url": _absolute(request, reverse("users:settings")),
        "site_name": "DevResurge",
    }

    subject = render_to_string(f"{template_base}_subject.txt", context).strip()
    text_body = render_to_string(f"{template_base}_body.txt", context)
    html_body = render_to_string(f"{template_base}_body.html", context)

    message = EmailMultiAlternatives(
        subject=subject,
        body=text_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[recipient.email],
    )
    message.attach_alternative(html_body, "text/html")

    try:
        message.send()
    except Exception:  # noqa: BLE001 — never let email break the request
        logger.warning(
            "Failed to send %s notification email to user %s",
            notification.kind,
            recipient.pk,
            exc_info=True,
        )
        return False
    return True
