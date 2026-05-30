from django.contrib import admin

from .models import Profile
from .models import ProjectLink
from .models import SocialLink


class ProjectLinkInline(admin.TabularInline):
    model = ProjectLink
    extra = 0
    fields = ("title", "url", "repo_url", "is_featured", "order")


class SocialLinkInline(admin.TabularInline):
    model = SocialLink
    extra = 0
    fields = ("platform", "label", "url", "order")


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "handle",
        "display_name",
        "primary_role",
        "location",
        "available_for_hire",
        "is_public",
        "updated_at",
    )
    list_filter = ("primary_role", "is_public", "available_for_hire")
    search_fields = ("handle", "display_name", "headline", "user__email", "tech_stack", "location")
    autocomplete_fields = ("user",)
    inlines = (SocialLinkInline, ProjectLinkInline)
    readonly_fields = ("created_at", "updated_at")


@admin.register(ProjectLink)
class ProjectLinkAdmin(admin.ModelAdmin):
    list_display = ("title", "profile", "is_featured", "order", "created_at")
    list_filter = ("is_featured",)
    search_fields = ("title", "description", "profile__handle")


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ("profile", "platform", "label", "url")
    list_filter = ("platform",)
    search_fields = ("profile__handle", "label", "url")
