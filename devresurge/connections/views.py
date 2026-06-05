from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Any

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.db import transaction
from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST
from django.views.generic import ListView

from .emails import send_notification_email
from .models import Connection
from .models import ConnectionStatus
from .models import Notification
from .models import NotificationKind

if TYPE_CHECKING:
    from django.db.models import QuerySet

User = get_user_model()


def _notify(
    request: HttpRequest,
    *,
    recipient,
    actor,
    kind: str,
    connection: Connection,
) -> None:
    """Create an in-app notification and best-effort email the recipient."""
    notification = Notification.objects.create(
        recipient=recipient,
        actor=actor,
        kind=kind,
        connection=connection,
    )
    send_notification_email(notification, request=request)


def _safe_redirect_back(request: HttpRequest, default: str) -> HttpResponse:
    """Redirect to the `next` param if it's a safe local path, else `default`."""
    nxt = request.POST.get("next") or request.GET.get("next")
    if nxt and nxt.startswith("/") and not nxt.startswith("//"):
        return redirect(nxt)
    return redirect(default)


@require_POST
@login_required
def connection_request_view(request: HttpRequest, user_id: int) -> HttpResponse:
    me = request.user
    target = get_object_or_404(User, pk=user_id)

    fallback = reverse("connections:list")
    if target.pk == me.pk:
        messages.error(request, _("You can't connect with yourself."))
        return _safe_redirect_back(request, fallback)

    existing = Connection.between(me, target)
    if existing is not None:
        if existing.is_accepted:
            messages.info(request, _("You're already connected."))
            return _safe_redirect_back(request, fallback)
        if existing.is_pending:
            if existing.requester_id == me.pk:
                messages.info(request, _("Your request is already pending."))
            else:
                messages.info(
                    request,
                    _("%(name)s already sent you a request — check your inbox.")
                    % {"name": _display(target)},
                )
            return _safe_redirect_back(request, fallback)
        # Previously declined: revive the row as a fresh request from `me`.
        existing.requester = me
        existing.addressee = target
        existing.status = ConnectionStatus.PENDING
        existing.responded_at = None
        try:
            with transaction.atomic():
                existing.save(update_fields=["requester", "addressee", "status", "responded_at"])
        except IntegrityError:
            messages.error(request, _("Could not send the request. Please try again."))
            return _safe_redirect_back(request, fallback)
        connection = existing
    else:
        try:
            with transaction.atomic():
                connection = Connection.objects.create(requester=me, addressee=target)
        except IntegrityError:
            messages.info(request, _("A connection already exists."))
            return _safe_redirect_back(request, fallback)

    _notify(
        request,
        recipient=target,
        actor=me,
        kind=NotificationKind.CONNECTION_REQUEST,
        connection=connection,
    )
    messages.success(
        request,
        _("Connection request sent to %(name)s.") % {"name": _display(target)},
    )
    return _safe_redirect_back(request, fallback)


@require_POST
@login_required
def connection_accept_view(request: HttpRequest, pk: int) -> HttpResponse:
    me = request.user
    connection = get_object_or_404(
        Connection,
        pk=pk,
        addressee=me,
        status=ConnectionStatus.PENDING,
    )
    connection.accept()
    _mark_request_notifications_read(me, connection)
    _notify(
        request,
        recipient=connection.requester,
        actor=me,
        kind=NotificationKind.CONNECTION_ACCEPTED,
        connection=connection,
    )
    messages.success(
        request,
        _("You're now connected with %(name)s.") % {"name": _display(connection.requester)},
    )
    return _safe_redirect_back(request, reverse("connections:list"))


@require_POST
@login_required
def connection_decline_view(request: HttpRequest, pk: int) -> HttpResponse:
    me = request.user
    connection = get_object_or_404(
        Connection,
        pk=pk,
        addressee=me,
        status=ConnectionStatus.PENDING,
    )
    connection.decline()
    _mark_request_notifications_read(me, connection)
    messages.info(request, _("Request declined."))
    return _safe_redirect_back(request, reverse("connections:notifications"))


@require_POST
@login_required
def connection_cancel_view(request: HttpRequest, pk: int) -> HttpResponse:
    me = request.user
    connection = get_object_or_404(
        Connection,
        pk=pk,
        requester=me,
        status=ConnectionStatus.PENDING,
    )
    # Deleting cascades to the addressee's pending request notification.
    connection.delete()
    messages.info(request, _("Request withdrawn."))
    return _safe_redirect_back(request, reverse("connections:list"))


@require_POST
@login_required
def connection_remove_view(request: HttpRequest, pk: int) -> HttpResponse:
    me = request.user
    connection = get_object_or_404(
        Connection.objects.involving(me).filter(status=ConnectionStatus.ACCEPTED),
        pk=pk,
    )
    other = connection.other_user(me)
    connection.delete()
    messages.info(
        request,
        _("Removed your connection with %(name)s.") % {"name": _display(other)},
    )
    return _safe_redirect_back(request, reverse("connections:list"))


def _mark_request_notifications_read(user, connection: Connection) -> None:
    """Clear the recipient's request notification once they respond to it."""
    (
        Notification.objects.for_user(user)
        .unread()
        .filter(connection=connection, kind=NotificationKind.CONNECTION_REQUEST)
        .update(read_at=timezone.now())
    )


def _display(user) -> str:
    profile = getattr(user, "profile", None)
    if profile and profile.display_name:
        return profile.display_name
    return user.name or user.email


class ConnectionListView(LoginRequiredMixin, ListView):
    """The signed-in user's network: accepted connections + pending requests."""

    template_name = "connections/connection_list.html"
    context_object_name = "connections"

    def get_queryset(self) -> QuerySet[Connection]:
        return (
            Connection.objects.involving(self.request.user)
            .accepted()
            .select_related(
                "requester__profile",
                "addressee__profile",
            )
        )

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        me = self.request.user
        ctx["accepted"] = [
            {"connection": c, "user": c.other_user(me)} for c in ctx["connections"]
        ]
        ctx["incoming"] = (
            Connection.objects.incoming(me).select_related("requester__profile")
        )
        ctx["outgoing"] = (
            Connection.objects.outgoing(me).select_related("addressee__profile")
        )
        return ctx


class NotificationListView(LoginRequiredMixin, ListView):
    """Inbox of in-app notifications; marks them read on view."""

    template_name = "connections/notification_list.html"
    context_object_name = "notifications"
    paginate_by = 25

    def get_queryset(self) -> QuerySet[Notification]:
        return (
            Notification.objects.for_user(self.request.user)
            .select_related("actor__profile", "connection")
        )

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        # Capture which were unread so we can still highlight them this load,
        # then clear them immediately so the navbar badge resets.
        self.unread_ids = set(
            Notification.objects.for_user(request.user)
            .unread()
            .values_list("id", flat=True),
        )
        if self.unread_ids:
            Notification.objects.filter(id__in=self.unread_ids).update(
                read_at=timezone.now(),
            )
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        ctx["unread_ids"] = getattr(self, "unread_ids", set())
        ctx["NotificationKind"] = NotificationKind
        return ctx


connection_list_view = ConnectionListView.as_view()
notification_list_view = NotificationListView.as_view()
