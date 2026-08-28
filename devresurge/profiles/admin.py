from django.contrib import admin

from .models import Education
from .models import LinkClick
from .models import Profile
from .models import ProfileView
from .models import ProjectLink
from .models import Recommendation
from .models import ShowcaseItem
from .models import SkillEndorsement
from .models import SocialLink
from .models import WorkExperience


class ProjectLinkInline(admin.TabularInline):
    model = ProjectLink
    extra = 0
    fields = ("title", "url", "repo_url", "is_featured", "order")


class ShowcaseItemInline(admin.TabularInline):
    model = ShowcaseItem
    extra = 0
    fields = ("title", "kind", "slug", "is_featured", "is_published", "order")
    readonly_fields = ("slug",)


class SocialLinkInline(admin.TabularInline):
    model = SocialLink
    extra = 0
    fields = ("platform", "label", "url", "order")


class WorkExperienceInline(admin.TabularInline):
    model = WorkExperience
    extra = 0
    fields = ("title", "company", "start_year", "is_current", "order")


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "handle",
        "display_name",
        "primary_role",
        "location",
        "available_for_hire",
        "open_to_collaborate",
        "is_public",
        "updated_at",
    )
    list_filter = (
        "primary_role",
        "is_public",
        "available_for_hire",
        "open_to_collaborate",
        "open_to_mentor",
    )
    search_fields = ("handle", "display_name", "headline", "user__email", "tech_stack", "location")
    autocomplete_fields = ("user",)
    inlines = (SocialLinkInline, ProjectLinkInline, ShowcaseItemInline, WorkExperienceInline)
    readonly_fields = ("created_at", "updated_at")


@admin.register(ProjectLink)
class ProjectLinkAdmin(admin.ModelAdmin):
    list_display = ("title", "profile", "is_featured", "order", "created_at")
    list_filter = ("is_featured",)
    search_fields = ("title", "description", "profile__handle")


@admin.register(ShowcaseItem)
class ShowcaseItemAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "profile",
        "kind",
        "is_published",
        "is_featured",
        "fetched_at",
        "order",
    )
    list_filter = ("kind", "is_published", "is_featured")
    search_fields = ("title", "summary", "github_url", "profile__handle")
    readonly_fields = (
        "slug",
        "github_owner",
        "github_repo",
        "github_path",
        "github_ref",
        "content_sha",
        "fetched_at",
        "fetch_error",
        "created_at",
        "updated_at",
    )


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ("profile", "platform", "label", "url")
    list_filter = ("platform",)
    search_fields = ("profile__handle", "label", "url")


@admin.register(WorkExperience)
class WorkExperienceAdmin(admin.ModelAdmin):
    list_display = ("title", "company", "profile", "start_year", "is_current")
    search_fields = ("title", "company", "profile__handle")


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ("school", "degree", "profile", "end_year")
    search_fields = ("school", "profile__handle")


@admin.register(SkillEndorsement)
class SkillEndorsementAdmin(admin.ModelAdmin):
    list_display = ("skill", "profile", "endorser", "created_at")
    search_fields = ("skill", "profile__handle", "endorser__email")
    raw_id_fields = ("profile", "endorser")


@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    list_display = ("profile", "author", "is_public", "created_at")
    search_fields = ("profile__handle", "author__email", "body")
    raw_id_fields = ("profile", "author")


@admin.register(ProfileView)
class ProfileViewAdmin(admin.ModelAdmin):
    list_display = ("profile", "created_at", "is_unique", "referrer")
    list_filter = ("is_unique", "created_at")
    search_fields = ("profile__handle", "referrer")
    readonly_fields = ("profile", "visitor_hash", "referrer", "is_unique", "created_at")
    date_hierarchy = "created_at"

    def has_add_permission(self, request) -> bool:  # noqa: ARG002
        return False


@admin.register(LinkClick)
class LinkClickAdmin(admin.ModelAdmin):
    list_display = ("profile", "kind", "label", "destination", "created_at")
    list_filter = ("kind", "created_at")
    search_fields = ("profile__handle", "label", "destination")
    readonly_fields = (
        "profile",
        "kind",
        "target_id",
        "label",
        "destination",
        "visitor_hash",
        "created_at",
    )
    date_hierarchy = "created_at"

    def has_add_permission(self, request) -> bool:  # noqa: ARG002
        return False
