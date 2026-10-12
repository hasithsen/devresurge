"""Universal search pages, JSON API, and course markdown viewer."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from django.conf import settings
from django.http import Http404
from django.http import HttpRequest
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.decorators.http import require_GET

from devresurge.profiles.markdown import render_markdown

from .courses import build_course_index
from .courses import list_course_slugs
from .courses import resolve_course_file
from .rate_limit import is_rate_limited
from .services import ALL_TYPES
from .services import normalize_query
from .services import parse_types
from .services import search


def _rate_limited_response() -> JsonResponse:
    response = JsonResponse(
        {"error": "rate_limited", "detail": "Too many search requests. Try again shortly."},
        status=429,
    )
    response["Retry-After"] = str(int(getattr(settings, "SEARCH_RATE_WINDOW", 60)))
    response["Cache-Control"] = "no-store"
    return response


@require_GET
def search_page(request: HttpRequest) -> HttpResponse:
    q = normalize_query(request.GET.get("q"))
    types = parse_types(request.GET.get("type"))
    per_type = int(getattr(settings, "SEARCH_PAGE_PER_TYPE", 12))
    payload = search(q, types=types, per_type=per_type) if q else {
        "query": "",
        "types": list(types),
        "groups": {t: [] for t in types},
        "results": [],
        "total": 0,
    }
    return render(
        request,
        "search/results.html",
        {
            "q": q,
            "active_types": types,
            "all_types": ALL_TYPES,
            "payload": payload,
            "min_len": int(getattr(settings, "SEARCH_QUERY_MIN_LEN", 2)),
        },
    )


@require_GET
def search_api(request: HttpRequest) -> HttpResponse:
    if is_rate_limited(
        request,
        prefix="search_rl",
        limit=int(getattr(settings, "SEARCH_RATE_LIMIT", 60)),
        window_seconds=int(getattr(settings, "SEARCH_RATE_WINDOW", 60)),
    ):
        return _rate_limited_response()

    q = normalize_query(request.GET.get("q"))
    types = parse_types(request.GET.get("type"))
    try:
        per_type = int(request.GET.get("limit") or getattr(settings, "SEARCH_SUGGEST_PER_TYPE", 5))
    except (TypeError, ValueError):
        per_type = int(getattr(settings, "SEARCH_SUGGEST_PER_TYPE", 5))

    payload = search(q, types=types, per_type=per_type)
    response = JsonResponse(payload)
    response["Cache-Control"] = "private, max-age=15"
    return response


@require_GET
def course_list(request: HttpRequest) -> HttpResponse:
    slugs = list_course_slugs()
    courses: list[dict[str, Any]] = []
    index = build_course_index()
    for slug in slugs:
        chapters = [d for d in index if d.course_slug == slug]
        readme = next((c for c in chapters if c.chapter_slug.startswith("00") or c.chapter_slug == "README"), None)
        courses.append(
            {
                "slug": slug,
                "title": readme.title if readme else slug,
                "summary": readme.summary if readme else "",
                "chapter_count": len(chapters),
                "url": reverse("courses:detail", kwargs={"course_slug": slug}),
            },
        )
    return render(request, "search/course_list.html", {"courses": courses})


def _chapter_nav(course_slug: str, current: str) -> list[dict[str, str]]:
    items = []
    for doc in build_course_index():
        if doc.course_slug != course_slug:
            continue
        items.append(
            {
                "slug": doc.chapter_slug,
                "title": doc.title,
                "url": reverse(
                    "courses:chapter",
                    kwargs={"course_slug": course_slug, "chapter_slug": doc.chapter_slug},
                ),
                "current": doc.chapter_slug == current,
            },
        )
    return items


@require_GET
def course_detail(request: HttpRequest, course_slug: str) -> HttpResponse:
    path = resolve_course_file(course_slug)
    if path is None:
        raise Http404(_("Course not found."))
    return _render_course(request, course_slug, path)


@require_GET
def course_chapter(request: HttpRequest, course_slug: str, chapter_slug: str) -> HttpResponse:
    # Canonicalize README aliases to course home
    if chapter_slug.lower() in {"readme", "00-readme"}:
        return redirect("courses:detail", course_slug=course_slug, permanent=False)
    path = resolve_course_file(course_slug, chapter_slug)
    if path is None:
        raise Http404(_("Chapter not found."))
    # Redirect to canonical stem if matched via bare slug
    if path.stem != chapter_slug:
        return redirect(
            "courses:chapter",
            course_slug=course_slug,
            chapter_slug=path.stem,
            permanent=True,
        )
    return _render_course(request, course_slug, path)


def _render_course(request: HttpRequest, course_slug: str, path: Path) -> HttpResponse:
    try:
        source = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise Http404(_("Chapter not found.")) from exc

    # Rewrite relative .md links to course viewer URLs
    body_html = render_markdown(_rewrite_course_links(source, course_slug), heading_ids=True)
    nav = _chapter_nav(course_slug, path.stem)
    title = next((item["title"] for item in nav if item["current"]), path.stem)
    return render(
        request,
        "search/course_chapter.html",
        {
            "course_slug": course_slug,
            "chapter_slug": path.stem,
            "title": title,
            "body_html": body_html,
            "nav": nav,
            "courses_home": reverse("courses:list"),
            "course_home": reverse("courses:detail", kwargs={"course_slug": course_slug}),
        },
    )


def _rewrite_course_links(source: str, course_slug: str) -> str:
    """Map relative markdown links like 02-namespaces.md to /courses/... URLs."""
    import re

    def repl(match: re.Match[str]) -> str:
        label, target = match.group(1), match.group(2)
        if target.startswith(("#", "http://", "https://", "mailto:", "/")):
            return match.group(0)
        if target.startswith("./"):
            target = target[2:]
        if "/" in target or ".." in target:
            return match.group(0)
        if target.endswith(".md"):
            stem = target[:-3]
            url = reverse(
                "courses:chapter",
                kwargs={"course_slug": course_slug, "chapter_slug": stem},
            )
            return f"[{label}]({url})"
        if target.startswith("labs/"):
            return f"[{label}]({target})"  # leave as-is; not served
        return match.group(0)

    return re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", repl, source)
