from __future__ import annotations

import json
from typing import TYPE_CHECKING
from typing import Any

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.db.models import Case
from django.db.models import IntegerField
from django.db.models import Q
from django.db.models import Value
from django.db.models import When
from django.http import Http404
from django.http import HttpRequest
from django.http import HttpResponse
from django.http import JsonResponse
from django.urls import reverse
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_POST
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.views.generic import UpdateView

from .forms import ProfileForm
from .forms import ProjectLinkForm
from .forms import SocialLinkForm
from .models import PrimaryRole
from .models import Profile
from .models import ProjectLink
from .models import SocialLink

if TYPE_CHECKING:
    from django.db.models import QuerySet


def _get_or_create_profile(user) -> Profile:
    profile, _created = Profile.objects.get_or_create(user=user)
    return profile


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
        return ctx


class ProfileBrowseView(ListView):
    """Public directory of profiles with simple search + role filter."""

    model = Profile
    template_name = "profiles/profile_list.html"
    context_object_name = "profiles"
    paginate_by = 24

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
        return qs

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        ctx["q"] = self.request.GET.get("q", "")
        ctx["role"] = self.request.GET.get("role", "")
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
            .prefetch_related("social_links", "projects")
        )

    def get_object(self, queryset: QuerySet[Profile] | None = None) -> Profile:
        obj = super().get_object(queryset=queryset)
        owner_viewing = self.request.user.is_authenticated and obj.user_id == self.request.user.pk
        if not obj.is_public and not owner_viewing:
            err = _("This profile is private.")
            raise Http404(err)
        return obj


class ProfileDashboardView(LoginRequiredMixin, DetailView):
    """Owner's dashboard — links to edit profile, projects, links."""

    model = Profile
    template_name = "profiles/dashboard.html"
    context_object_name = "profile"

    def get_object(self, queryset: QuerySet[Profile] | None = None) -> Profile:
        return _get_or_create_profile(self.request.user)


class ProfileEditView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = "profiles/profile_form.html"
    success_message = _("Profile updated.")

    def get_object(self, queryset: QuerySet[Profile] | None = None) -> Profile:
        return _get_or_create_profile(self.request.user)

    def get_success_url(self) -> str:
        return reverse("profiles:dashboard")


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
        return super().form_valid(form)


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


# Function aliases (cookiecutter convention)
home_view = HomeView.as_view()
profile_browse_view = ProfileBrowseView.as_view()
profile_public_view = ProfilePublicView.as_view()
profile_dashboard_view = ProfileDashboardView.as_view()
profile_edit_view = ProfileEditView.as_view()
project_list_view = ProjectLinkListView.as_view()
project_create_view = ProjectLinkCreateView.as_view()
project_update_view = ProjectLinkUpdateView.as_view()
project_delete_view = ProjectLinkDeleteView.as_view()
link_list_view = SocialLinkListView.as_view()
link_create_view = SocialLinkCreateView.as_view()
link_update_view = SocialLinkUpdateView.as_view()
link_delete_view = SocialLinkDeleteView.as_view()
# `project_reorder_view` and `link_reorder_view` are already module-level functions.
