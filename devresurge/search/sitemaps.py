"""Sitemap entries for courses and the search landing page."""

from __future__ import annotations

from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .courses import build_course_index
from .courses import list_course_slugs


class SearchStaticSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return ["search:page", "learning:course_list"]

    def location(self, item: str) -> str:
        return reverse(item)


class CourseSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.65

    def items(self):
        items: list[tuple[str, str | None]] = []
        for slug in list_course_slugs():
            items.append((slug, None))
        for doc in build_course_index():
            if doc.chapter_slug.lower() in {"readme", "00-readme"}:
                continue
            items.append((doc.course_slug, doc.chapter_slug))
        return items

    def location(self, item: tuple[str, str | None]) -> str:
        course_slug, chapter_slug = item
        if chapter_slug is None:
            return reverse("learning:course_detail", kwargs={"course_slug": course_slug})
        return reverse(
            "learning:course_chapter",
            kwargs={"course_slug": course_slug, "chapter_slug": chapter_slug},
        )
