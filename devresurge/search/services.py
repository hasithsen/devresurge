"""Efficient multi-source search with scoring, limits, and short-lived cache."""

from __future__ import annotations

import hashlib
import re
from dataclasses import asdict
from dataclasses import dataclass
from typing import Any
from typing import Literal

from django.conf import settings
from django.core.cache import cache
from django.db.models import Q
from django.urls import reverse

from devresurge.learning.catalog import all_roadmaps
from devresurge.profiles.models import Profile
from devresurge.profiles.models import ProfileTool
from devresurge.quizzes.models import Quiz

from .courses import build_course_index

SearchType = Literal["people", "courses", "learn", "quizzes", "tools"]

ALL_TYPES: tuple[SearchType, ...] = ("people", "courses", "learn", "quizzes", "tools")

_WS_RE = re.compile(r"\s+")


@dataclass(frozen=True)
class SearchHit:
    type: SearchType
    title: str
    subtitle: str
    url: str
    score: float
    meta: dict[str, str]


def normalize_query(raw: str | None) -> str:
    text = _WS_RE.sub(" ", (raw or "").strip())
    max_len = int(getattr(settings, "SEARCH_QUERY_MAX_LEN", 80))
    return text[:max_len]


def parse_types(raw: str | None) -> tuple[SearchType, ...]:
    if not raw or raw.strip() in {"", "all", "*"}:
        return ALL_TYPES
    wanted: list[SearchType] = []
    for part in raw.split(","):
        key = part.strip().lower()
        if key in ALL_TYPES and key not in wanted:
            wanted.append(key)  # type: ignore[arg-type]
    return tuple(wanted) or ALL_TYPES


def _score(query: str, *fields: str) -> float:
    q = query.lower()
    best = 0.0
    for idx, field in enumerate(fields):
        if not field:
            continue
        value = field.lower()
        weight = 1.0 - (idx * 0.08)
        if value == q:
            best = max(best, 100 * weight)
        elif value.startswith(q):
            best = max(best, 80 * weight)
        elif f" {q}" in f" {value}":
            best = max(best, 60 * weight)
        elif q in value:
            best = max(best, 40 * weight)
    return best


def _search_people(query: str, limit: int) -> list[SearchHit]:
    qs = (
        Profile.objects.filter(is_public=True)
        .filter(
            Q(display_name__icontains=query)
            | Q(handle__icontains=query)
            | Q(headline__icontains=query)
            | Q(tech_stack__icontains=query)
            | Q(location__icontains=query)
            | Q(bio__icontains=query)
            | Q(primary_role__icontains=query),
        )
        .only(
            "handle",
            "display_name",
            "headline",
            "tech_stack",
            "location",
            "primary_role",
            "bio",
        )[: max(limit * 3, limit)]
    )
    hits: list[SearchHit] = []
    for profile in qs:
        score = _score(
            query,
            profile.handle,
            profile.display_name,
            profile.headline,
            profile.tech_stack,
            profile.location,
            profile.primary_role,
            (profile.bio or "")[:200],
        )
        if score <= 0:
            continue
        hits.append(
            SearchHit(
                type="people",
                title=profile.display_name or profile.handle,
                subtitle=profile.headline or f"@{profile.handle}",
                url=reverse("profiles:public", kwargs={"handle": profile.handle}),
                score=score,
                meta={"handle": profile.handle, "role": profile.primary_role or ""},
            ),
        )
    hits.sort(key=lambda h: (-h.score, h.title.lower()))
    return hits[:limit]


def _search_quizzes(query: str, limit: int) -> list[SearchHit]:
    qs = (
        Quiz.objects.filter(is_published=True)
        .filter(
            Q(title__icontains=query)
            | Q(tagline__icontains=query)
            | Q(description__icontains=query)
            | Q(topic__icontains=query)
            | Q(slug__icontains=query),
        )
        .only("slug", "title", "tagline", "description", "topic")[: max(limit * 3, limit)]
    )
    hits: list[SearchHit] = []
    for quiz in qs:
        score = _score(query, quiz.title, quiz.topic, quiz.tagline, quiz.slug, quiz.description)
        if score <= 0:
            continue
        hits.append(
            SearchHit(
                type="quizzes",
                title=quiz.title,
                subtitle=quiz.tagline or quiz.topic or "quiz",
                url=reverse("quizzes:detail", kwargs={"slug": quiz.slug}),
                score=score,
                meta={"topic": quiz.topic or "", "slug": quiz.slug},
            ),
        )
    hits.sort(key=lambda h: (-h.score, h.title.lower()))
    return hits[:limit]


def _search_learn(query: str, limit: int) -> list[SearchHit]:
    hits: list[SearchHit] = []
    for roadmap in all_roadmaps():
        score = _score(
            query,
            roadmap.title,
            roadmap.slug,
            roadmap.tagline,
            roadmap.domain,
            roadmap.description,
            roadmap.audience,
        )
        if score > 0:
            hits.append(
                SearchHit(
                    type="learn",
                    title=roadmap.title,
                    subtitle=roadmap.tagline or roadmap.domain,
                    url=reverse("learning:roadmap", kwargs={"roadmap_slug": roadmap.slug}),
                    score=score + 5,  # prefer roadmaps over lessons slightly
                    meta={"kind": "roadmap", "domain": roadmap.domain},
                ),
            )
        for lesson in roadmap.lessons:
            lscore = _score(query, lesson.title, lesson.slug, lesson.summary, lesson.hook)
            if lscore <= 0:
                continue
            hits.append(
                SearchHit(
                    type="learn",
                    title=lesson.title,
                    subtitle=f"{roadmap.title} · lesson",
                    url=reverse(
                        "learning:lesson",
                        kwargs={
                            "roadmap_slug": roadmap.slug,
                            "lesson_slug": lesson.slug,
                        },
                    ),
                    score=lscore,
                    meta={"kind": "lesson", "roadmap": roadmap.slug},
                ),
            )
    hits.sort(key=lambda h: (-h.score, h.title.lower()))
    return hits[:limit]


def _search_tools(query: str, limit: int) -> list[SearchHit]:
    catalog = ProfileTool.catalog(q=query)
    hits: list[SearchHit] = []
    for row in catalog[: max(limit * 2, limit)]:
        name = str(row.get("name") or "")
        category = str(row.get("category_label") or row.get("category") or "")
        slug = str(row.get("slug") or "")
        users = row.get("users") or 0
        score = _score(query, name, category, slug)
        if score <= 0:
            continue
        url = str(row.get("url") or reverse("profiles:tool_explore_detail", kwargs={"slug": slug}))
        hits.append(
            SearchHit(
                type="tools",
                title=name,
                subtitle=f"{category} · {users} profiles" if category else f"{users} profiles",
                url=url,
                score=score,
                meta={"category": str(row.get("category") or ""), "slug": slug},
            ),
        )
    hits.sort(key=lambda h: (-h.score, h.title.lower()))
    return hits[:limit]


def _search_courses(query: str, limit: int) -> list[SearchHit]:
    hits: list[SearchHit] = []
    for doc in build_course_index():
        score = _score(
            query,
            doc.title,
            doc.course_slug,
            doc.chapter_slug,
            doc.summary,
            doc.path,
        )
        if score <= 0:
            continue
        hits.append(
            SearchHit(
                type="courses",
                title=doc.title,
                subtitle=f"{doc.course_slug} · {doc.summary}"[:160],
                url=reverse(
                    "learning:course_chapter",
                    kwargs={
                        "course_slug": doc.course_slug,
                        "chapter_slug": doc.chapter_slug,
                    },
                ),
                score=score,
                meta={"course": doc.course_slug, "chapter": doc.chapter_slug},
            ),
        )
    hits.sort(key=lambda h: (-h.score, h.title.lower()))
    return hits[:limit]


_SEARCHERS = {
    "people": _search_people,
    "courses": _search_courses,
    "learn": _search_learn,
    "quizzes": _search_quizzes,
    "tools": _search_tools,
}


def search(
    query: str,
    *,
    types: tuple[SearchType, ...] | None = None,
    per_type: int | None = None,
    use_cache: bool = True,
) -> dict[str, Any]:
    """Run universal search. Returns groups + flat ranked hits."""
    q = normalize_query(query)
    min_len = int(getattr(settings, "SEARCH_QUERY_MIN_LEN", 2))
    types = types or ALL_TYPES
    per_type = per_type or int(getattr(settings, "SEARCH_PER_TYPE_LIMIT", 8))
    per_type = max(1, min(per_type, int(getattr(settings, "SEARCH_PER_TYPE_MAX", 25))))

    empty = {
        "query": q,
        "types": list(types),
        "groups": {t: [] for t in types},
        "results": [],
        "total": 0,
    }
    if len(q) < min_len:
        return empty

    cache_ttl = int(getattr(settings, "SEARCH_CACHE_TTL", 30))
    cache_key = ""
    if use_cache and cache_ttl > 0:
        digest = hashlib.sha256(f"{q}|{','.join(types)}|{per_type}".encode()).hexdigest()[:24]
        cache_key = f"search:v1:{digest}"
        cached = cache.get(cache_key)
        if cached is not None:
            return cached

    groups: dict[str, list[dict[str, Any]]] = {}
    flat: list[SearchHit] = []
    for stype in types:
        searcher = _SEARCHERS[stype]
        hits = searcher(q, per_type)
        groups[stype] = [asdict(h) for h in hits]
        flat.extend(hits)

    flat.sort(key=lambda h: (-h.score, h.type, h.title.lower()))
    payload = {
        "query": q,
        "types": list(types),
        "groups": groups,
        "results": [asdict(h) for h in flat],
        "total": len(flat),
    }
    if cache_key:
        cache.set(cache_key, payload, cache_ttl)
    return payload
