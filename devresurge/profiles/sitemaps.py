from __future__ import annotations

from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from devresurge.profiles.models import Profile
from devresurge.profiles.models import ProfileTool


class ProfileSitemap(Sitemap):
    """Index public profiles for search engines."""

    changefreq = "weekly"
    priority = 0.8
    protocol = None  # inherit from request / settings

    def items(self):
        return Profile.objects.filter(is_public=True).only("handle", "updated_at")

    def lastmod(self, obj: Profile):
        return obj.updated_at

    def location(self, obj: Profile) -> str:
        return obj.get_absolute_url()


class ProfileNetworkMapSitemap(Sitemap):
    """Index public network maps (public accounts only)."""

    changefreq = "weekly"
    priority = 0.5
    protocol = None

    def items(self):
        return Profile.objects.filter(is_public=True).only("handle", "updated_at")

    def lastmod(self, obj: Profile):
        return obj.updated_at

    def location(self, obj: Profile) -> str:
        return reverse("profiles:network_map", kwargs={"handle": obj.handle})


class ProfileToolsSitemap(Sitemap):
    """Index per-profile public tools pages when the member listed any."""

    changefreq = "weekly"
    priority = 0.55
    protocol = None

    def items(self):
        return (
            Profile.objects.filter(is_public=True, tools__isnull=False)
            .distinct()
            .only("handle", "updated_at")
        )

    def lastmod(self, obj: Profile):
        return obj.updated_at

    def location(self, obj: Profile) -> str:
        return reverse("profiles:public_tools", kwargs={"handle": obj.handle})


class ToolExploreSitemap(Sitemap):
    """Index popular public tool detail pages."""

    changefreq = "weekly"
    priority = 0.45
    protocol = None

    def items(self):
        return ProfileTool.catalog()[:200]

    def location(self, obj: dict) -> str:
        return obj["url"]


class StaticViewSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return [
            "home",
            "about",
            "profiles:browse",
            "profiles:explore_map",
            "profiles:tool_explore",
            "learning:list",
            "quizzes:list",
        ]

    def location(self, item: str) -> str:
        return reverse(item)
