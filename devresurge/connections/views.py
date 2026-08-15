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

from .context_processors import invalidate_unread_count
from .emails import send_notification_email
from .graph import build_explore_graph
from .graph import build_network_graph
from .models import Connection
from .models import ConnectionRelation
from .models import ConnectionStatus
from .models import Notification
from .models import NotificationKind
from .share import build_explore_share_links
from .share import build_map_invite_share_links
from .share import build_map_share_links

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
    invalidate_unread_count(recipient.pk)
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
    allowed = {c.value for c in ConnectionRelation}
    value = (raw or ConnectionRelation.PEER).strip().lower()
    return value if value in allowed else ConnectionRelation.PEER


def _connect_context(viewer, profile_user) -> dict[str, Any]:
    """Return connect UI state for ``viewer`` toward ``profile_user``."""
    can_connect = viewer.is_authenticated and viewer.pk != profile_user.pk
    connection = None
    state = "none"
    if can_connect:
        connection = Connection.between(viewer, profile_user)
        if connection is not None:
            if connection.is_blocked:
                if connection.requester_id == viewer.pk:
                    state = "blocked"
                else:
                    can_connect = False
                    connection = None
                    state = "none"
            elif connection.is_accepted:
                state = "connected"
            elif connection.is_pending:
                state = (
                    "outgoing"
                    if connection.requester_id == viewer.pk
                    else "incoming"
                )
            elif connection.status == ConnectionStatus.DECLINED:
                state = "none"
    return {
        "can_connect": can_connect,
        "connection": connection,
        "connect_state": state,
    }


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
        ctx["profile"] = getattr(me, "profile", None)
        return ctx


class NetworkMapView(LoginRequiredMixin, TemplateView):
    """Owner map of public connections.

    When the profile is publicly listed, redirect to the canonical shareable
    URL ``/u/<handle>/map/`` so there is one map product — not two.
    Private profiles keep a login-only preview here until they publish.
    """

    template_name = "connections/network_map.html"

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        profile = getattr(request.user, "profile", None)
        if profile is not None and profile.is_public and profile.handle:
            target = reverse(
                "profiles:network_map",
                kwargs={"handle": profile.handle},
            )
            qs = request.META.get("QUERY_STRING", "")
            if qs:
                target = f"{target}?{qs}"
            return redirect(target)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        include_mutual = self.request.GET.get("mutual", "1") != "0"
        graph = build_network_graph(
            self.request.user,
            include_mutual=include_mutual,
            public_only=True,
        )
        ctx["graph"] = graph
        ctx["include_mutual"] = include_mutual
        ctx["relations"] = ConnectionRelation.choices
        ctx["graph_json_url"] = reverse("connections:map_data")
        ctx["is_public_map"] = False
        ctx["is_explore_map"] = False
        ctx["map_profile"] = getattr(self.request.user, "profile", None)
        ctx["map_share"] = None
        ctx["map_invite"] = None
        ctx["invite_landing"] = False
        ctx["is_map_owner"] = True
        return ctx


@login_required
@require_GET
def network_map_data_view(request: HttpRequest) -> JsonResponse:
    """JSON graph payload for the owner's map (public accounts only)."""
    include_mutual = request.GET.get("mutual", "1") != "0"
    graph = build_network_graph(
        request.user,
        include_mutual=include_mutual,
        public_only=True,
    )
    response = JsonResponse(graph)
    response["Cache-Control"] = "private, no-store"
    return response


class PublicNetworkMapView(TemplateView):
    """Public ego-network map for a listed profile (public accounts only)."""

    template_name = "connections/network_map.html"

    def get_profile(self):
        from devresurge.profiles.models import Profile

        return get_object_or_404(
            Profile.objects.filter(is_public=True).select_related("user"),
            handle=Profile.normalize_handle(self.kwargs["handle"]),
        )

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        self.profile = self.get_profile()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        include_mutual = self.request.GET.get("mutual", "1") != "0"
        profile = self.profile
        graph = build_network_graph(
            profile.user,
            include_mutual=include_mutual,
            public_only=True,
            viewer=self.request.user if self.request.user.is_authenticated else None,
        )
        ctx["graph"] = graph
        ctx["include_mutual"] = include_mutual
        ctx["relations"] = ConnectionRelation.choices
        ctx["graph_json_url"] = reverse(
            "profiles:network_map_data",
            kwargs={"handle": profile.handle},
        )
        ctx["is_public_map"] = True
        ctx["is_explore_map"] = False
        ctx["map_profile"] = profile
        map_path = reverse("profiles:network_map", kwargs={"handle": profile.handle})
        map_url = self.request.build_absolute_uri(map_path)
        ctx["map_share"] = build_map_share_links(
            page_url=map_url,
            handle=profile.handle,
        )
        invite_url = f"{map_url}?invite=1"
        ctx["map_invite"] = build_map_invite_share_links(
            page_url=invite_url,
            handle=profile.handle,
            name=profile.public_name,
        )
        invite_flag = (self.request.GET.get("invite") or "").strip() in {
            "1",
            "true",
            "yes",
            "connect",
        }
        viewer = self.request.user
        is_owner = viewer.is_authenticated and viewer.pk == profile.user_id
        ctx["is_map_owner"] = is_owner
        ctx["invite_landing"] = invite_flag and not is_owner
        connect = _connect_context(viewer, profile.user)
        ctx.update(connect)
        ctx["relations"] = ConnectionRelation.choices
        profile_path = reverse("profiles:public", kwargs={"handle": profile.handle})
        ctx["connect_profile_url"] = f"{profile_path}?connect=1"
        return ctx


@require_GET
def public_network_map_data_view(request: HttpRequest, handle: str) -> JsonResponse:
    """Public JSON graph for a listed profile — never includes private accounts."""
    from devresurge.profiles.models import Profile

    profile = get_object_or_404(
        Profile.objects.filter(is_public=True).select_related("user"),
        handle=Profile.normalize_handle(handle),
    )
    include_mutual = request.GET.get("mutual", "1") != "0"
    graph = build_network_graph(
        profile.user,
        include_mutual=include_mutual,
        public_only=True,
        viewer=request.user if request.user.is_authenticated else None,
    )
    response = JsonResponse(graph)
    response["Cache-Control"] = "public, max-age=60, must-revalidate"
    return response


class ExploreMapView(TemplateView):
    """Anonymous-friendly public map of connected DevResurge profiles."""

    template_name = "connections/network_map.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        graph = build_explore_graph()
        ctx["graph"] = graph
        ctx["include_mutual"] = False
        ctx["relations"] = ConnectionRelation.choices
        ctx["graph_json_url"] = reverse("profiles:explore_map_data")
        ctx["is_public_map"] = True
        ctx["is_explore_map"] = True
        ctx["map_profile"] = None
        map_url = self.request.build_absolute_uri(reverse("profiles:explore_map"))
        ctx["map_share"] = build_explore_share_links(page_url=map_url)
        ctx["map_invite"] = None
        ctx["invite_landing"] = False
        ctx["is_map_owner"] = False
        viewer = self.request.user
        if viewer.is_authenticated:
            profile = getattr(viewer, "profile", None)
            if profile is not None and profile.is_public and profile.handle:
                invite_path = reverse(
                    "profiles:network_map",
                    kwargs={"handle": profile.handle},
                )
                invite_url = f"{self.request.build_absolute_uri(invite_path)}?invite=1"
                ctx["map_invite"] = build_map_invite_share_links(
                    page_url=invite_url,
                    handle=profile.handle,
                    name=profile.public_name,
                )
                ctx["is_map_owner"] = True
        return ctx


@require_GET
def explore_map_data_view(request: HttpRequest) -> JsonResponse:
    """JSON payload for the public community explore map."""
    graph = build_explore_graph()
    response = JsonResponse(graph)
    response["Cache-Control"] = "public, max-age=60, must-revalidate"
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
            invalidate_unread_count(request.user.pk)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        ctx["unread_ids"] = getattr(self, "unread_ids", set())
        ctx["NotificationKind"] = NotificationKind
        return ctx


connection_list_view = ConnectionListView.as_view()
notification_list_view = NotificationListView.as_view()
network_map_view = NetworkMapView.as_view()
public_network_map_view = PublicNetworkMapView.as_view()
explore_map_view = ExploreMapView.as_view()
