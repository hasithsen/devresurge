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
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext as _
from django.views.decorators.http import require_GET
from django.views.decorators.http import require_POST
from django.views.generic import ListView
from django.views.generic import TemplateView

from .emails import send_notification_email
from .graph import build_network_graph
from .models import Connection
from .models import ConnectionRelation
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
    connection: Connection | None = None,
    payload: str = "",
) -> None:
    """Create an in-app notification and best-effort email the recipient."""
    notification = Notification.objects.create(
        recipient=recipient,
        actor=actor,
        kind=kind,
        connection=connection,
        payload=payload[:120],
    )
    if connection is not None and kind in {
        NotificationKind.CONNECTION_REQUEST,
        NotificationKind.CONNECTION_ACCEPTED,
    }:
        send_notification_email(notification, request=request)


def _safe_redirect_back(request: HttpRequest, default: str) -> HttpResponse:
    """Redirect to the `next` param if it's a safe local path, else `default`."""
    nxt = request.POST.get("next") or request.GET.get("next")
    if nxt and nxt.startswith("/") and not nxt.startswith("//"):
        return redirect(nxt)
    return redirect(default)


def _parse_relation(raw: str | None) -> str:
    value = (raw or "").strip()
    if value in ConnectionRelation.values:
        return value
    return ConnectionRelation.PEER


def _parse_message(raw: str | None) -> str:
    return (raw or "").strip()[:280]


@require_POST
@login_required
def connection_request_view(request: HttpRequest, user_id: int) -> HttpResponse:
    me = request.user
    target = get_object_or_404(User, pk=user_id)
    relation = _parse_relation(request.POST.get("relation"))
    message = _parse_message(request.POST.get("message"))

    fallback = reverse("connections:list")
    if target.pk == me.pk:
        messages.error(request, _("You can't connect with yourself."))
        return _safe_redirect_back(request, fallback)

    existing = Connection.between(me, target)
    if existing is not None:
        if existing.is_blocked:
            messages.error(request, _("You can't connect with this member."))
            return _safe_redirect_back(request, fallback)
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
        existing.relation = relation
        existing.message = message
        existing.responded_at = None
        try:
            with transaction.atomic():
                existing.save(
                    update_fields=[
                        "requester",
                        "addressee",
                        "status",
                        "relation",
                        "message",
                        "responded_at",
                    ],
                )
        except IntegrityError:
            messages.error(request, _("Could not send the request. Please try again."))
            return _safe_redirect_back(request, fallback)
        connection = existing
    else:
        try:
            with transaction.atomic():
                connection = Connection.objects.create(
                    requester=me,
                    addressee=target,
                    relation=relation,
                    message=message,
                )
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
    # Engagement hook — first / network badges.
    try:
        from devresurge.quizzes.awards import evaluate_connection_badges

        evaluate_connection_badges(me)
        evaluate_connection_badges(connection.requester)
    except Exception:  # noqa: BLE001 — badges must never break accept
        pass

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


@require_POST
@login_required
def connection_relation_view(request: HttpRequest, pk: int) -> HttpResponse:
    """Update the relation label on an accepted connection."""
    me = request.user
    connection = get_object_or_404(
        Connection.objects.involving(me).filter(status=ConnectionStatus.ACCEPTED),
        pk=pk,
    )
    connection.relation = _parse_relation(request.POST.get("relation"))
    connection.save(update_fields=["relation"])
    messages.success(request, _("Connection status updated."))
    return _safe_redirect_back(request, reverse("connections:list"))


@require_POST
@login_required
def connection_block_view(request: HttpRequest, user_id: int) -> HttpResponse:
    """Block a user — prevents future connection requests either way."""
    me = request.user
    target = get_object_or_404(User, pk=user_id)
    fallback = reverse("connections:list")
    if target.pk == me.pk:
        messages.error(request, _("You can't block yourself."))
        return _safe_redirect_back(request, fallback)

    existing = Connection.between(me, target)
    if existing is not None:
        if existing.is_blocked and existing.requester_id == me.pk:
            messages.info(request, _("Already blocked."))
            return _safe_redirect_back(request, fallback)
        existing.block(me)
    else:
        Connection.objects.create(
            requester=me,
            addressee=target,
            status=ConnectionStatus.BLOCKED,
            responded_at=timezone.now(),
        )
    messages.info(
        request,
        _("Blocked %(name)s.") % {"name": _display(target)},
    )
    return _safe_redirect_back(request, fallback)


@require_POST
@login_required
def connection_unblock_view(request: HttpRequest, pk: int) -> HttpResponse:
    me = request.user
    connection = get_object_or_404(
        Connection,
        pk=pk,
        requester=me,
        status=ConnectionStatus.BLOCKED,
    )
    connection.delete()
    messages.info(request, _("Unblocked."))
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
    """Public label for a user — never exposes their email address."""
    profile = getattr(user, "profile", None)
    if profile is not None:
        return profile.public_name
    return _("a member")


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
        ctx["blocked"] = (
            Connection.objects.filter(requester=me, status=ConnectionStatus.BLOCKED)
            .select_related("addressee__profile")
        )
        ctx["relations"] = ConnectionRelation.choices
        return ctx


class NetworkMapView(LoginRequiredMixin, TemplateView):
    """Interactive force-directed map of the signed-in user's network."""

    template_name = "connections/network_map.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        include_mutual = self.request.GET.get("mutual", "1") != "0"
        graph = build_network_graph(self.request.user, include_mutual=include_mutual)
        ctx["graph"] = graph
        ctx["include_mutual"] = include_mutual
        ctx["relations"] = ConnectionRelation.choices
        ctx["graph_json_url"] = reverse("connections:map_data")
        return ctx


@login_required
@require_GET
def network_map_data_view(request: HttpRequest) -> JsonResponse:
    """JSON graph payload for the map (and future clients)."""
    include_mutual = request.GET.get("mutual", "1") != "0"
    graph = build_network_graph(request.user, include_mutual=include_mutual)
    response = JsonResponse(graph)
    response["Cache-Control"] = "private, no-store"
    return response


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
network_map_view = NetworkMapView.as_view()
