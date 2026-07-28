from __future__ import annotations

import hashlib
import json
import logging
from datetime import timedelta
from typing import TYPE_CHECKING
from typing import Any
from urllib.parse import urlparse

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db import DatabaseError
from django.db import IntegrityError
from django.db import transaction
from django.db.models import Case
from django.db.models import Count
from django.db.models import IntegerField
from django.db.models import Prefetch
from django.db.models import Q
from django.db.models import Value
from django.db.models import When
from django.db.models.functions import TruncDate
from django.http import Http404
from django.http import HttpRequest
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.urls import reverse
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import cache_control
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from django.views.decorators.http import require_POST
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.views.generic import UpdateView

from devresurge.connections.models import Connection
from devresurge.connections.models import ConnectionStatus
from devresurge.connections.models import Notification
from devresurge.connections.models import NotificationKind

from .badges import render_profile_badge_svg
from .forms import EducationForm
from .forms import ProfileForm
from .forms import ProjectLinkForm
from .forms import RecommendationForm
from .forms import SocialLinkForm
from .forms import WorkExperienceForm
from .models import Education
from .models import LinkClick
from .models import LinkKind
from .models import PrimaryRole
from .models import Profile
from .models import ProfileView as ProfileViewEvent
from .models import ProjectLink
from .models import Recommendation
from .models import SkillEndorsement
from .models import SocialLink
from .models import WorkExperience

if TYPE_CHECKING:
    from django.db.models import QuerySet

logger = logging.getLogger(__name__)


def _get_or_create_profile(user) -> Profile:
    profile, _created = Profile.objects.get_or_create(user=user)
    return profile


# ---------------------------------------------------------------------------
# Analytics recording (privacy-preserving)
# ---------------------------------------------------------------------------

_BOT_UA_MARKERS = (
    "bot",
    "crawl",
    "spider",
    "slurp",
    "bingpreview",
    "facebookexternalhit",
    "embedly",
    "preview",
    "headless",
    "monitor",
    "uptime",
    "curl",
    "wget",
    "python-requests",
)


def _client_ip(request: HttpRequest) -> str:
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR", "")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "") or ""


def _looks_like_bot(user_agent: str) -> bool:
    ua = (user_agent or "").lower()
    if not ua:
        return False
    return any(marker in ua for marker in _BOT_UA_MARKERS)


def _referrer_host(request: HttpRequest) -> str:
    referrer = request.META.get("HTTP_REFERER", "") or ""
    if not referrer:
        return ""
    host = urlparse(referrer).netloc.lower()
    # Internal navigation shouldn't show up as an external referrer.
    if not host or host == request.get_host().lower():
        return ""
    return host[:255]


def _visitor_hash(request: HttpRequest, profile: Profile, user_agent: str) -> str:
    """Salted, irreversible visitor fingerprint — never stores the raw IP."""
    raw = "|".join(
        [
            settings.SECRET_KEY,
            str(profile.pk),
            _client_ip(request),
            user_agent or "",
        ],
    )
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def _host_or_value(url: str) -> str:
    """Reduce a URL to its host for grouping (or a scheme label like 'mailto')."""
    url = (url or "").strip()
    if not url:
        return ""
    parsed = urlparse(url)
    if parsed.netloc:
        return parsed.netloc.lower()[:255]
    if parsed.scheme:
        return parsed.scheme.lower()[:255]
    return url[:255]


def record_profile_view(request: HttpRequest, profile: Profile) -> None:
    """Log a profile page view, skipping owners, bots and non-GET requests.

    Failures are swallowed (logged) so analytics can never break page render.
    The insert runs in its own savepoint to stay safe under ATOMIC_REQUESTS.
    """
    if request.method != "GET":
        return

    user = getattr(request, "user", None)
    if user is not None and user.is_authenticated and user.pk == profile.user_id:
        return

    user_agent = request.META.get("HTTP_USER_AGENT", "")
    if _looks_like_bot(user_agent):
        return

    visitor = _visitor_hash(request, profile, user_agent)
    seen_today = ProfileViewEvent.objects.filter(
        profile=profile,
        visitor_hash=visitor,
        created_at__date=timezone.localdate(),
    ).exists()

    try:
        with transaction.atomic():
            ProfileViewEvent.objects.create(
                profile=profile,
                visitor_hash=visitor,
                referrer=_referrer_host(request),
                is_unique=not seen_today,
            )
    except DatabaseError:
        logger.warning("Failed to record profile view for %s", profile.pk, exc_info=True)


# Suppress duplicate beacons from a single interaction (e.g. click + auxclick).
_CLICK_DEDUPE_SECONDS = 2


def record_link_click(
    request: HttpRequest,
    profile: Profile,
    kind: str,
    *,
    target_id: int | None = None,
    label: str = "",
    destination: str = "",
) -> None:
    """Log an outbound link click, skipping owners, bots and rapid duplicates."""
    user = getattr(request, "user", None)
    if user is not None and user.is_authenticated and user.pk == profile.user_id:
        return

    user_agent = request.META.get("HTTP_USER_AGENT", "")
    if _looks_like_bot(user_agent):
        return

    visitor = _visitor_hash(request, profile, user_agent)
    recent = timezone.now() - timedelta(seconds=_CLICK_DEDUPE_SECONDS)
    is_duplicate = LinkClick.objects.filter(
        profile=profile,
        visitor_hash=visitor,
        kind=kind,
        target_id=target_id,
        created_at__gte=recent,
    ).exists()
    if is_duplicate:
        return

    try:
        with transaction.atomic():
            LinkClick.objects.create(
                profile=profile,
                kind=kind,
                target_id=target_id,
                label=label[:160],
                destination=destination[:255],
                visitor_hash=visitor,
            )
    except DatabaseError:
        logger.warning("Failed to record link click for %s", profile.pk, exc_info=True)


@csrf_exempt
@require_POST
def link_click_view(request: HttpRequest) -> HttpResponse:
    """Beacon endpoint for outbound link clicks on public profiles.

    CSRF-exempt because `navigator.sendBeacon` cannot attach a CSRF header.
    This only ever increments anonymous analytics counters for *public*
    profiles, and the server derives the label/destination from its own DB
    records (the client only supplies a handle, kind and id), so a spoofed
    payload cannot inject arbitrary content.
    """
    try:
        payload = json.loads(request.body or b"{}")
    except (json.JSONDecodeError, UnicodeDecodeError):
        return HttpResponseBadRequest("invalid json")
    if not isinstance(payload, dict):
        return HttpResponseBadRequest("invalid payload")

    handle = Profile.normalize_handle(payload.get("handle"))
    kind = (payload.get("kind") or "").strip()
    if not handle or kind not in LinkKind.values:
        return HttpResponseBadRequest("missing or invalid fields")

    profile = (
        Profile.objects.filter(handle=handle, is_public=True)
        .only("id", "user_id", "website_url")
        .first()
    )
    # Silently ignore unknown/private profiles so the beacon can't enumerate them.
    if profile is None:
        return HttpResponse(status=204)

    label = ""
    destination = ""
    target_id: int | None = None

    if kind in {LinkKind.PROJECT, LinkKind.SOCIAL}:
        try:
            target_id = int(payload.get("id"))
        except (TypeError, ValueError):
            return HttpResponse(status=204)

        if kind == LinkKind.PROJECT:
            project = profile.projects.filter(pk=target_id).first()
            if project is None:
                return HttpResponse(status=204)
            chosen = project.repo_url if payload.get("field") == "repo" else (project.url or project.repo_url)
            label = project.title
            destination = _host_or_value(chosen)
        else:
            link = profile.social_links.filter(pk=target_id).first()
            if link is None:
                return HttpResponse(status=204)
            label = link.display_label
            destination = "email" if link.platform == "email" else _host_or_value(link.url)
    elif kind == LinkKind.WEBSITE:
        if not profile.website_url:
            return HttpResponse(status=204)
        label = "website"
        destination = _host_or_value(profile.website_url)
    elif kind == LinkKind.EMAIL:
        label = "email"
        destination = "email"

    record_link_click(
        request,
        profile,
        kind,
        target_id=target_id,
        label=label,
        destination=destination,
    )
    return HttpResponse(status=204)


class HomeView(TemplateView):
    template_name = "pages/home.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        ctx["featured_profiles"] = (
            Profile.objects.filter(is_public=True)
            .select_related("user")
            .order_by("-updated_at")[:6]
        )
        ctx["profile_count"] = Profile.objects.filter(is_public=True).count()
        ctx["project_count"] = ProjectLink.objects.count()

        # Showcase public maps that actually have connections (LinkedIn complement).
        from devresurge.connections.graph import build_network_graph

        featured_maps: list[dict[str, Any]] = []
        for profile in (
            Profile.objects.filter(is_public=True)
            .select_related("user")
            .order_by("-updated_at")[:24]
        ):
            graph = build_network_graph(profile.user, public_only=True)
            if graph["stats"]["connections"] < 1:
                continue
            featured_maps.append({"profile": profile, "stats": graph["stats"]})
            if len(featured_maps) >= 3:
                break
        ctx["featured_maps"] = featured_maps
        return ctx


class ProfileBrowseView(ListView):
    """Public directory of profiles with search, role, and hire filters."""

    model = Profile
    template_name = "profiles/profile_list.html"
    context_object_name = "profiles"
    paginate_by = 24

    def hire_only(self) -> bool:
        return (self.request.GET.get("hire") or "").strip() in {"1", "true", "yes", "on"}

    def intent(self) -> str:
        raw = (self.request.GET.get("intent") or "").strip()
        allowed = {"hire", "collaborate", "mentor", "learning"}
        return raw if raw in allowed else ""

    def get_queryset(self) -> QuerySet[Profile]:
        qs = (
            Profile.objects.filter(is_public=True)
            .select_related("user")
            .prefetch_related("social_links", "projects")
        )
        q = (self.request.GET.get("q") or "").strip()
        role = (self.request.GET.get("role") or "").strip()
        if q:
            qs = qs.filter(
                Q(display_name__icontains=q)
                | Q(handle__icontains=q)
                | Q(headline__icontains=q)
                | Q(tech_stack__icontains=q)
                | Q(location__icontains=q),
            )
        if role and role in PrimaryRole.values:
            qs = qs.filter(primary_role=role)
        intent = self.intent()
        if intent == "hire" or self.hire_only():
            qs = qs.filter(available_for_hire=True)
        elif intent == "collaborate":
            qs = qs.filter(open_to_collaborate=True)
        elif intent == "mentor":
            qs = qs.filter(open_to_mentor=True)
        elif intent == "learning":
            qs = qs.filter(open_to_learning=True)
        if intent or self.hire_only():
            return qs.order_by("-updated_at")
        return qs.order_by("-available_for_hire", "-open_to_collaborate", "-updated_at")

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        ctx["q"] = self.request.GET.get("q", "")
        ctx["role"] = self.request.GET.get("role", "")
        ctx["hire"] = self.hire_only() or self.intent() == "hire"
        ctx["intent"] = self.intent() or ("hire" if self.hire_only() else "")
        ctx["roles"] = PrimaryRole.choices
        return ctx


class ProfilePublicView(DetailView):
    """Public, handle-addressable profile page."""

    model = Profile
    template_name = "profiles/profile_detail.html"
    context_object_name = "profile"
    slug_field = "handle"
    slug_url_kwarg = "handle"

    def get_queryset(self) -> QuerySet[Profile]:
        return (
            Profile.objects.select_related("user")
            .prefetch_related(
                "social_links",
                "projects",
                "experiences",
                "education",
                Prefetch(
                    "recommendations_received",
                    queryset=Recommendation.objects.filter(is_public=True).select_related(
                        "author__profile",
                    ),
                ),
            )
        )

    def get_object(self, queryset: QuerySet[Profile] | None = None) -> Profile:
        # Handles are case-insensitive: match on the canonical lowercase form,
        # which uses the SlugField's btree index (no per-row UPPER()).
        if queryset is None:
            queryset = self.get_queryset()
        handle = Profile.normalize_handle(self.kwargs.get(self.slug_url_kwarg, ""))
        try:
            obj = queryset.get(handle=handle)
        except Profile.DoesNotExist as exc:
            err = _("No profile found for this handle.")
            raise Http404(err) from exc
        owner_viewing = self.request.user.is_authenticated and obj.user_id == self.request.user.pk
        if not obj.is_public and not owner_viewing:
            err = _("This profile is private.")
            raise Http404(err)
        return obj

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        self.object = self.get_object()
        # Redirect non-canonical (e.g. mixed-case) URLs to the lowercase form
        # so each profile has a single canonical address.
        requested = kwargs.get(self.slug_url_kwarg, "")
        if requested != self.object.handle:
            return redirect("profiles:public", handle=self.object.handle, permanent=True)
        context = self.get_context_data(object=self.object)
        # Only public, non-owner GET hits reach here (private → 404 above).
        record_profile_view(request, self.object)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        viewer = self.request.user
        profile = self.object
        can_connect = viewer.is_authenticated and viewer.pk != profile.user_id
        connection = None
        state = "none"
        if can_connect:
            connection = Connection.between(viewer, profile.user)
            if connection is not None:
                if connection.is_blocked:
                    # Only the blocker sees a blocked state; blocked party sees none.
                    if connection.requester_id == viewer.pk:
                        state = "blocked"
                    else:
                        can_connect = False
                        state = "none"
                        connection = None
                elif connection.is_accepted:
                    state = "connected"
                elif connection.is_pending:
                    state = "outgoing" if connection.requester_id == viewer.pk else "incoming"
                elif connection.status == "declined":
                    state = "none"
        ctx["can_connect"] = can_connect
        ctx["connection"] = connection
        ctx["connect_state"] = state
        from devresurge.connections.models import ConnectionRelation

        ctx["relations"] = ConnectionRelation.choices
        from devresurge.quizzes.models import UserBadge

        ctx["user_badges"] = (
            UserBadge.objects.filter(user=profile.user, badge__is_active=True)
            .select_related("badge")
            .order_by("badge__order", "-earned_at")
        )

        # Endorsement counts per skill + which the viewer already gave.
        endorsement_counts = {
            row["skill"]: row["c"]
            for row in (
                SkillEndorsement.objects.filter(profile=profile)
                .values("skill")
                .annotate(c=Count("id"))
            )
        }
        ctx["skill_endorsements"] = [
            {"skill": skill, "count": endorsement_counts.get(skill, 0)}
            for skill in profile.tech_stack_list
        ]
        ctx["my_endorsed_skills"] = set()
        ctx["is_connected"] = state == "connected"
        ctx["recommendation_form"] = None
        ctx["existing_recommendation"] = None
        ctx["mutual_connections"] = []
        ctx["linkedin_url"] = profile.linkedin_url()
        ctx["map_peer_count"] = 0
        ctx["map_share"] = None
        ctx["map_invite"] = None
        ctx["is_owner"] = viewer.is_authenticated and viewer.pk == profile.user_id
        ctx["open_connect"] = (self.request.GET.get("connect") or "").strip() in {
            "1",
            "true",
            "yes",
        }
        if profile.is_public and profile.handle:
            from devresurge.connections.share import build_map_invite_share_links
            from devresurge.connections.share import build_map_share_links

            ctx["map_peer_count"] = (
                Connection.objects.accepted()
                .filter(
                    Q(
                        requester_id=profile.user_id,
                        addressee__profile__is_public=True,
                    )
                    | Q(
                        addressee_id=profile.user_id,
                        requester__profile__is_public=True,
                    ),
                )
                .count()
            )
            map_path = reverse("profiles:network_map", kwargs={"handle": profile.handle})
            map_url = self.request.build_absolute_uri(map_path)
            ctx["map_share"] = build_map_share_links(
                page_url=map_url,
                handle=profile.handle,
            )
            ctx["map_invite"] = build_map_invite_share_links(
                page_url=f"{map_url}?invite=1",
                handle=profile.handle,
                name=profile.public_name,
            )

        if viewer.is_authenticated and viewer.pk != profile.user_id:
            ctx["my_endorsed_skills"] = set(
                SkillEndorsement.objects.filter(
                    profile=profile,
                    endorser=viewer,
                ).values_list("skill", flat=True),
            )
            if state == "connected":
                ctx["recommendation_form"] = RecommendationForm()
                ctx["existing_recommendation"] = Recommendation.objects.filter(
                    profile=profile,
                    author=viewer,
                ).first()
                # Mutual accepted connections (shared network).
                my_peers = set(
                    Connection.objects.involving(viewer)
                    .accepted()
                    .values_list("requester_id", "addressee_id"),
                )
                my_ids: set[int] = set()
                for a, b in my_peers:
                    my_ids.add(b if a == viewer.pk else a)
                their_peers = set(
                    Connection.objects.involving(profile.user)
                    .accepted()
                    .values_list("requester_id", "addressee_id"),
                )
                their_ids: set[int] = set()
                for a, b in their_peers:
                    their_ids.add(b if a == profile.user_id else a)
                mutual_ids = (my_ids & their_ids) - {viewer.pk, profile.user_id}
                if mutual_ids:
                    ctx["mutual_connections"] = list(
                        Profile.objects.filter(user_id__in=mutual_ids, is_public=True)
                        .select_related("user")[:8],
                    )
        return ctx


class ProfileDashboardView(LoginRequiredMixin, DetailView):
    """Owner's dashboard — links to edit profile, projects, links."""

    model = Profile
    template_name = "profiles/dashboard.html"
    context_object_name = "profile"

    def get_object(self, queryset: QuerySet[Profile] | None = None) -> Profile:
        return _get_or_create_profile(self.request.user)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        ctx["views_30d"] = (
            ProfileViewEvent.objects.for_profile(self.object).within_days(30).count()
        )
        ctx["readiness"] = self.object.readiness()
        badge_path = reverse("profiles:badge", kwargs={"handle": self.object.handle})
        ctx["badge_url"] = self.request.build_absolute_uri(badge_path)
        from devresurge.quizzes.models import Quiz
        from devresurge.quizzes.models import UserBadge

        ctx["earned_badges"] = (
            UserBadge.objects.filter(user=self.request.user, badge__is_active=True)
            .select_related("badge")
            .order_by("badge__order")[:8]
        )
        ctx["quiz_count"] = Quiz.objects.filter(is_published=True).count()
        return ctx


@login_required
@require_GET
def profile_export_readme_view(request: HttpRequest) -> HttpResponse:
    """Download the owner's profile as a README.md file."""
    profile = _get_or_create_profile(request.user)
    base = f"{request.scheme}://{request.get_host()}"
    body = profile.to_readme_markdown(base_url=base)
    response = HttpResponse(body, content_type="text/markdown; charset=utf-8")
    response["Content-Disposition"] = f'attachment; filename="{profile.handle}-README.md"'
    return response


@cache_control(public=True, max_age=60 * 10)
@require_GET
def profile_badge_view(request: HttpRequest, handle: str) -> HttpResponse:
    """Public SVG badge for embedding in GitHub READMEs and personal sites."""
    profile = get_object_or_404(
        Profile.objects.filter(is_public=True),
        handle=Profile.normalize_handle(handle),
    )
    svg = render_profile_badge_svg(profile)
    response = HttpResponse(svg, content_type="image/svg+xml; charset=utf-8")
    response["Cache-Control"] = "public, max-age=60, must-revalidate"
    return response


class ProfileEditView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = "profiles/profile_form.html"
    success_message = _("Profile updated.")

    def get_object(self, queryset: QuerySet[Profile] | None = None) -> Profile:
        return _get_or_create_profile(self.request.user)

    def form_valid(self, form):
        response = super().form_valid(form)
        try:
            from devresurge.quizzes.awards import evaluate_profile_badges

            evaluate_profile_badges(self.request.user)
        except Exception:  # noqa: BLE001
            pass
        return response

    def get_success_url(self) -> str:
        return reverse("profiles:dashboard")


# ---------------------------------------------------------------------------
# Analytics dashboard
# ---------------------------------------------------------------------------


class ProfileAnalyticsView(LoginRequiredMixin, TemplateView):
    """Owner-only analytics for their own profile, over a selectable window."""

    template_name = "profiles/analytics.html"
    RANGE_CHOICES = (7, 30, 90)
    DEFAULT_RANGE = 30

    def get_range(self) -> int:
        try:
            days = int(self.request.GET.get("days", self.DEFAULT_RANGE))
        except (TypeError, ValueError):
            return self.DEFAULT_RANGE
        return days if days in self.RANGE_CHOICES else self.DEFAULT_RANGE

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        profile = _get_or_create_profile(self.request.user)
        days = self.get_range()
        today = timezone.localdate()
        start = today - timedelta(days=days - 1)
        prev_start = start - timedelta(days=days)
        prev_end = start - timedelta(days=1)

        events = ProfileViewEvent.objects.filter(profile=profile, created_at__date__gte=start)

        total_views = events.count()
        unique_visitors = events.values("visitor_hash").distinct().count()

        prev_views = ProfileViewEvent.objects.filter(
            profile=profile,
            created_at__date__gte=prev_start,
            created_at__date__lte=prev_end,
        ).count()
        views_delta = total_views - prev_views
        if prev_views > 0:
            views_delta_pct = round((views_delta / prev_views) * 100)
        elif total_views > 0:
            views_delta_pct = 100
        else:
            views_delta_pct = 0

        daily = (
            events.annotate(day=TruncDate("created_at"))
            .values("day")
            .annotate(
                views=Count("id"),
                uniques=Count("visitor_hash", distinct=True),
            )
        )
        by_day = {row["day"]: row for row in daily}

        series: list[dict[str, Any]] = []
        peak = 0
        for offset in range(days):
            day = start + timedelta(days=offset)
            row = by_day.get(day)
            view_count = row["views"] if row else 0
            unique_count = row["uniques"] if row else 0
            peak = max(peak, view_count)
            series.append(
                {
                    "date": day,
                    "views": view_count,
                    "uniques": unique_count,
                    "is_today": day == today,
                    "weekday": day.strftime("%a"),
                },
            )

        # X-axis tick cadence: every day (7), ~weekly (30), ~biweekly (90).
        if days <= 7:
            tick_every = 1
        elif days <= 30:
            tick_every = 5
        else:
            tick_every = 14

        for idx, point in enumerate(series):
            point["pct"] = round((point["views"] / peak) * 100, 1) if peak else 0
            point["unique_pct"] = (
                round((point["uniques"] / peak) * 100, 1) if peak else 0
            )
            point["share"] = (
                round((point["views"] / total_views) * 100) if total_views else 0
            )
            point["is_peak"] = bool(peak and point["views"] == peak)
            point["show_tick"] = (
                idx == 0
                or idx == days - 1
                or point["is_today"]
                or (idx % tick_every == 0)
            )
            if days <= 7:
                point["tick_label"] = point["weekday"][:2]
            else:
                point["tick_label"] = f"{point['date'].month}/{point['date'].day}"

        peak_mid = peak // 2
        avg_per_day = round(total_views / days, 1) if days else 0
        avg_pct = round((avg_per_day / peak) * 100, 1) if peak and avg_per_day else 0
        if peak <= 1:
            y_ticks = [
                {"value": peak, "pct": 100},
                {"value": 0, "pct": 0},
            ]
        else:
            y_ticks = [
                {"value": peak, "pct": 100},
                {"value": peak_mid, "pct": round((peak_mid / peak) * 100, 1)},
                {"value": 0, "pct": 0},
            ]

        busiest = max(series, key=lambda p: p["views"], default=None)
        if busiest and busiest["views"] == 0:
            busiest = None

        # Active days table (newest first) — actual per-day numbers.
        daily_rows = [p for p in reversed(series) if p["views"] > 0]
        active_days = len(daily_rows)

        # Referrer breakdown (external hosts only) + a synthetic "direct" row.
        referrers = list(
            events.exclude(referrer="")
            .values("referrer")
            .annotate(count=Count("id"))
            .order_by("-count")[:8],
        )
        direct_views = total_views - events.exclude(referrer="").count()
        ref_max = max([r["count"] for r in referrers] + [direct_views] + [0])
        for ref in referrers:
            ref["pct"] = round((ref["count"] / ref_max) * 100) if ref_max else 0
            ref["share"] = (
                round((ref["count"] / total_views) * 100) if total_views else 0
            )
        direct_share = (
            round((direct_views / total_views) * 100) if total_views else 0
        )
        direct_pct = round((direct_views / ref_max) * 100) if ref_max else 0

        last_view = (
            events.order_by("-created_at").values_list("created_at", flat=True).first()
        )

        # Outbound link clicks over the same window.
        clicks = LinkClick.objects.filter(profile=profile, created_at__date__gte=start)
        total_clicks = clicks.count()
        top_links = list(
            clicks.values("kind", "label", "destination")
            .annotate(count=Count("id"))
            .order_by("-count")[:8],
        )
        click_max = top_links[0]["count"] if top_links else 0
        for link in top_links:
            link["pct"] = round((link["count"] / click_max) * 100) if click_max else 0
            link["share"] = (
                round((link["count"] / total_clicks) * 100) if total_clicks else 0
            )

        ctr = (
            round((total_clicks / total_views) * 100, 1) if total_views else 0
        )

        ctx.update(
            {
                "profile": profile,
                "days": days,
                "range_choices": self.RANGE_CHOICES,
                "retention_days": ProfileViewEvent.RETENTION_DAYS,
                "window_start": start,
                "window_end": today,
                "total_views": total_views,
                "unique_visitors": unique_visitors,
                "avg_per_day": avg_per_day,
                "avg_pct": avg_pct,
                "y_ticks": y_ticks,
                "prev_views": prev_views,
                "views_delta": views_delta,
                "views_delta_pct": views_delta_pct,
                "ctr": ctr,
                "busiest": busiest,
                "series": series,
                "daily_rows": daily_rows,
                "active_days": active_days,
                "peak": peak,
                "peak_mid": peak_mid,
                "referrers": referrers,
                "direct_views": direct_views,
                "direct_share": direct_share,
                "direct_pct": direct_pct,
                "last_view": last_view,
                "unique_share": (
                    round((unique_visitors / total_views) * 100) if total_views else 0
                ),
                "total_clicks": total_clicks,
                "top_links": top_links,
                "has_views": total_views > 0,
                "has_clicks": total_clicks > 0,
                "has_data": total_views > 0 or total_clicks > 0,
            },
        )
        return ctx


# ---------------------------------------------------------------------------
# Project link CRUD
# ---------------------------------------------------------------------------


class _OwnerScopedMixin(LoginRequiredMixin):
    """Restrict the queryset to objects owned by the current user."""

    owner_field = "profile__user"

    def get_queryset(self):  # type: ignore[override]
        qs = super().get_queryset()  # type: ignore[misc]
        return qs.filter(**{self.owner_field: self.request.user})


class ProjectLinkListView(LoginRequiredMixin, ListView):
    model = ProjectLink
    template_name = "profiles/projectlink_list.html"
    context_object_name = "projects"

    def get_queryset(self) -> QuerySet[ProjectLink]:
        profile = _get_or_create_profile(self.request.user)
        return profile.projects.all()

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        ctx["profile"] = _get_or_create_profile(self.request.user)
        return ctx


class ProjectLinkCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = ProjectLink
    form_class = ProjectLinkForm
    template_name = "profiles/projectlink_form.html"
    success_url = reverse_lazy("profiles:project_list")
    success_message = _("Project added.")

    def form_valid(self, form: ProjectLinkForm):
        form.instance.profile = _get_or_create_profile(self.request.user)
        response = super().form_valid(form)
        try:
            from devresurge.quizzes.awards import evaluate_profile_badges

            evaluate_profile_badges(self.request.user)
        except Exception:  # noqa: BLE001
            pass
        return response


class ProjectLinkUpdateView(_OwnerScopedMixin, SuccessMessageMixin, UpdateView):
    model = ProjectLink
    form_class = ProjectLinkForm
    template_name = "profiles/projectlink_form.html"
    success_url = reverse_lazy("profiles:project_list")
    success_message = _("Project updated.")


class ProjectLinkDeleteView(_OwnerScopedMixin, DeleteView):
    model = ProjectLink
    template_name = "profiles/projectlink_confirm_delete.html"
    success_url = reverse_lazy("profiles:project_list")


# ---------------------------------------------------------------------------
# Social link CRUD
# ---------------------------------------------------------------------------


class SocialLinkListView(LoginRequiredMixin, ListView):
    model = SocialLink
    template_name = "profiles/sociallink_list.html"
    context_object_name = "links"

    def get_queryset(self) -> QuerySet[SocialLink]:
        profile = _get_or_create_profile(self.request.user)
        return profile.social_links.all()

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        ctx["profile"] = _get_or_create_profile(self.request.user)
        return ctx


class SocialLinkCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = SocialLink
    form_class = SocialLinkForm
    template_name = "profiles/sociallink_form.html"
    success_url = reverse_lazy("profiles:link_list")
    success_message = _("Link added.")

    def form_valid(self, form: SocialLinkForm):
        form.instance.profile = _get_or_create_profile(self.request.user)
        return super().form_valid(form)


class SocialLinkUpdateView(_OwnerScopedMixin, SuccessMessageMixin, UpdateView):
    model = SocialLink
    form_class = SocialLinkForm
    template_name = "profiles/sociallink_form.html"
    success_url = reverse_lazy("profiles:link_list")
    success_message = _("Link updated.")


class SocialLinkDeleteView(_OwnerScopedMixin, DeleteView):
    model = SocialLink
    template_name = "profiles/sociallink_confirm_delete.html"
    success_url = reverse_lazy("profiles:link_list")


# ---------------------------------------------------------------------------
# Reorder endpoints (used by drag-and-drop in the list templates)
# ---------------------------------------------------------------------------


def _reorder(request: HttpRequest, model: Any) -> HttpResponse:
    """Apply a new `order` to caller-owned `model` rows.

    Body: ``{"ids": [3, 1, 2]}`` — the new order, top → bottom.
    Only ids actually owned by the requester's profile are touched, which both
    enforces authorization and silently drops stale ids the client may submit.
    """
    try:
        payload = json.loads(request.body or b"{}")
    except json.JSONDecodeError:
        return JsonResponse({"ok": False, "error": "invalid json"}, status=400)

    raw_ids = payload.get("ids")
    if not isinstance(raw_ids, list):
        return JsonResponse({"ok": False, "error": "ids must be a list"}, status=400)

    ids: list[int] = []
    for value in raw_ids:
        try:
            ids.append(int(value))
        except (TypeError, ValueError):
            return JsonResponse({"ok": False, "error": "ids must be integers"}, status=400)

    profile = _get_or_create_profile(request.user)
    owned_qs = model.objects.filter(profile=profile, pk__in=ids)
    owned_ids = set(owned_qs.values_list("pk", flat=True))
    ordered = [pk for pk in ids if pk in owned_ids]

    if not ordered:
        return JsonResponse({"ok": True, "updated": 0})

    whens = [When(pk=pk, then=Value(idx)) for idx, pk in enumerate(ordered)]
    with transaction.atomic():
        model.objects.filter(pk__in=ordered).update(
            order=Case(*whens, default=Value(0), output_field=IntegerField()),
        )
    return JsonResponse({"ok": True, "updated": len(ordered)})


@login_required
@require_POST
def project_reorder_view(request: HttpRequest) -> HttpResponse:
    return _reorder(request, ProjectLink)


@login_required
@require_POST
def link_reorder_view(request: HttpRequest) -> HttpResponse:
    return _reorder(request, SocialLink)


# ---------------------------------------------------------------------------
# Experience + education CRUD
# ---------------------------------------------------------------------------


class ExperienceListView(LoginRequiredMixin, ListView):
    model = WorkExperience
    template_name = "profiles/experience_list.html"
    context_object_name = "experiences"

    def get_queryset(self):
        return _get_or_create_profile(self.request.user).experiences.all()

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        ctx["profile"] = _get_or_create_profile(self.request.user)
        return ctx


class ExperienceCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = WorkExperience
    form_class = WorkExperienceForm
    template_name = "profiles/experience_form.html"
    success_url = reverse_lazy("profiles:experience_list")
    success_message = _("Experience added.")

    def form_valid(self, form):
        form.instance.profile = _get_or_create_profile(self.request.user)
        return super().form_valid(form)


class ExperienceUpdateView(_OwnerScopedMixin, SuccessMessageMixin, UpdateView):
    model = WorkExperience
    form_class = WorkExperienceForm
    template_name = "profiles/experience_form.html"
    success_url = reverse_lazy("profiles:experience_list")
    success_message = _("Experience updated.")


class ExperienceDeleteView(_OwnerScopedMixin, DeleteView):
    model = WorkExperience
    template_name = "profiles/experience_confirm_delete.html"
    success_url = reverse_lazy("profiles:experience_list")


class EducationListView(LoginRequiredMixin, ListView):
    model = Education
    template_name = "profiles/education_list.html"
    context_object_name = "education_list"

    def get_queryset(self):
        return _get_or_create_profile(self.request.user).education.all()

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        ctx["profile"] = _get_or_create_profile(self.request.user)
        return ctx


class EducationCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Education
    form_class = EducationForm
    template_name = "profiles/education_form.html"
    success_url = reverse_lazy("profiles:education_list")
    success_message = _("Education added.")

    def form_valid(self, form):
        form.instance.profile = _get_or_create_profile(self.request.user)
        return super().form_valid(form)


class EducationUpdateView(_OwnerScopedMixin, SuccessMessageMixin, UpdateView):
    model = Education
    form_class = EducationForm
    template_name = "profiles/education_form.html"
    success_url = reverse_lazy("profiles:education_list")
    success_message = _("Education updated.")


class EducationDeleteView(_OwnerScopedMixin, DeleteView):
    model = Education
    template_name = "profiles/education_confirm_delete.html"
    success_url = reverse_lazy("profiles:education_list")


# ---------------------------------------------------------------------------
# Endorsements + recommendations (connection-gated)
# ---------------------------------------------------------------------------


def _require_accepted_connection(viewer, profile_user) -> Connection | None:
    conn = Connection.between(viewer, profile_user)
    if conn is None or not conn.is_accepted:
        return None
    return conn


@login_required
@require_POST
def skill_endorse_view(request: HttpRequest, handle: str) -> HttpResponse:
    profile = get_object_or_404(
        Profile.objects.filter(is_public=True),
        handle=Profile.normalize_handle(handle),
    )
    fallback = profile.get_absolute_url()
    if profile.user_id == request.user.pk:
        messages.error(request, _("You can't endorse yourself."))
        return redirect(fallback)
    if _require_accepted_connection(request.user, profile.user) is None:
        messages.error(request, _("Connect first to endorse skills."))
        return redirect(fallback)

    skill = (request.POST.get("skill") or "").strip().lower()
    if skill not in profile.tech_stack_list:
        messages.error(request, _("That skill isn't on their stack."))
        return redirect(fallback)

    try:
        with transaction.atomic():
            _, created = SkillEndorsement.objects.get_or_create(
                profile=profile,
                endorser=request.user,
                skill=skill,
            )
    except IntegrityError:
        created = False

    if created:
        Notification.objects.create(
            recipient=profile.user,
            actor=request.user,
            kind=NotificationKind.SKILL_ENDORSED,
            payload=skill,
        )
        messages.success(request, _("Endorsed %(skill)s.") % {"skill": skill})
    else:
        messages.info(request, _("You already endorsed that skill."))
    return redirect(fallback)


@login_required
@require_POST
def skill_unendorse_view(request: HttpRequest, handle: str) -> HttpResponse:
    profile = get_object_or_404(
        Profile,
        handle=Profile.normalize_handle(handle),
    )
    skill = (request.POST.get("skill") or "").strip().lower()
    SkillEndorsement.objects.filter(
        profile=profile,
        endorser=request.user,
        skill=skill,
    ).delete()
    messages.info(request, _("Endorsement removed."))
    return redirect(profile.get_absolute_url())


@login_required
@require_POST
def recommendation_create_view(request: HttpRequest, handle: str) -> HttpResponse:
    profile = get_object_or_404(
        Profile.objects.filter(is_public=True),
        handle=Profile.normalize_handle(handle),
    )
    fallback = profile.get_absolute_url()
    if profile.user_id == request.user.pk:
        messages.error(request, _("You can't recommend yourself."))
        return redirect(fallback)
    if _require_accepted_connection(request.user, profile.user) is None:
        messages.error(request, _("Connect first to write a recommendation."))
        return redirect(fallback)

    existing = Recommendation.objects.filter(profile=profile, author=request.user).first()
    form = RecommendationForm(request.POST, instance=existing)
    if not form.is_valid():
        messages.error(request, form.errors.as_text())
        return redirect(fallback)

    rec = form.save(commit=False)
    rec.profile = profile
    rec.author = request.user
    rec.is_public = True
    rec.save()
    if existing is None:
        Notification.objects.create(
            recipient=profile.user,
            actor=request.user,
            kind=NotificationKind.RECOMMENDATION,
            payload=profile.handle,
        )
        messages.success(request, _("Recommendation published."))
    else:
        messages.success(request, _("Recommendation updated."))
    return redirect(fallback)


# Function aliases (cookiecutter convention)
home_view = HomeView.as_view()
profile_browse_view = ProfileBrowseView.as_view()
profile_public_view = ProfilePublicView.as_view()
profile_dashboard_view = ProfileDashboardView.as_view()
profile_edit_view = ProfileEditView.as_view()
profile_analytics_view = ProfileAnalyticsView.as_view()
project_list_view = ProjectLinkListView.as_view()
project_create_view = ProjectLinkCreateView.as_view()
project_update_view = ProjectLinkUpdateView.as_view()
project_delete_view = ProjectLinkDeleteView.as_view()
link_list_view = SocialLinkListView.as_view()
link_create_view = SocialLinkCreateView.as_view()
link_update_view = SocialLinkUpdateView.as_view()
link_delete_view = SocialLinkDeleteView.as_view()
experience_list_view = ExperienceListView.as_view()
experience_create_view = ExperienceCreateView.as_view()
experience_update_view = ExperienceUpdateView.as_view()
experience_delete_view = ExperienceDeleteView.as_view()
education_list_view = EducationListView.as_view()
education_create_view = EducationCreateView.as_view()
education_update_view = EducationUpdateView.as_view()
education_delete_view = EducationDeleteView.as_view()
# `project_reorder_view`, `link_reorder_view`, `link_click_view`,
# `profile_export_readme_view`, `profile_badge_view`, endorse/recommend
# helpers are already module-level functions.
