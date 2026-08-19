"""Catalog of FAANG-oriented roadmaps and lessons (code-as-CMS)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .content import backend
from .content import databases
from .content import devops
from .content import distributed
from .content import dsa
from .content import elite_path
from .content import foundations
from .content import system_design
from .flavor import flavor_for


@dataclass(frozen=True)
class Lesson:
    slug: str
    title: str
    summary: str
    body: str
    minutes: int = 12
    quiz_slug: str | None = None
    outcomes: tuple[str, ...] = ()
    hook: str = ""
    boss_fight: str = ""
    xp: int = 0


@dataclass(frozen=True)
class Roadmap:
    slug: str
    title: str
    tagline: str
    description: str
    domain: str
    level: str
    icon: str
    order: int
    audience: str
    outcomes: tuple[str, ...]
    lessons: tuple[Lesson, ...]
    related_quiz_slugs: tuple[str, ...] = ()

    @property
    def lesson_count(self) -> int:
        return len(self.lessons)

    @property
    def total_minutes(self) -> int:
        return sum(lesson.minutes for lesson in self.lessons)

    def get_lesson(self, slug: str) -> Lesson | None:
        for lesson in self.lessons:
            if lesson.slug == slug:
                return lesson
        return None

    def lesson_index(self, slug: str) -> int:
        for idx, lesson in enumerate(self.lessons):
            if lesson.slug == slug:
                return idx
        return -1


def _lesson(data: dict[str, Any]) -> Lesson:
    minutes = int(data.get("minutes", 12))
    hook, boss_fight = flavor_for(data["slug"])
    return Lesson(
        slug=data["slug"],
        title=data["title"],
        summary=data["summary"],
        body=data["body"].strip(),
        minutes=minutes,
        quiz_slug=data.get("quiz_slug"),
        outcomes=tuple(data.get("outcomes") or ()),
        hook=data.get("hook") or hook,
        boss_fight=data.get("boss_fight") or boss_fight,
        xp=int(data.get("xp") or minutes * 10),
    )


def _roadmap(data: dict[str, Any]) -> Roadmap:
    return Roadmap(
        slug=data["slug"],
        title=data["title"],
        tagline=data["tagline"],
        description=data["description"],
        domain=data["domain"],
        level=data["level"],
        icon=data["icon"],
        order=int(data["order"]),
        audience=data["audience"],
        outcomes=tuple(data.get("outcomes") or ()),
        lessons=tuple(_lesson(item) for item in data["lessons"]),
        related_quiz_slugs=tuple(data.get("related_quiz_slugs") or ()),
    )


ROADMAP_SOURCES: tuple[dict[str, Any], ...] = (
    foundations.ROADMAP,
    dsa.ROADMAP,
    system_design.ROADMAP,
    backend.ROADMAP,
    devops.ROADMAP,
    databases.ROADMAP,
    distributed.ROADMAP,
    elite_path.ROADMAP,
)

ROADMAPS: tuple[Roadmap, ...] = tuple(
    sorted((_roadmap(src) for src in ROADMAP_SOURCES), key=lambda r: (r.order, r.title)),
)

_BY_SLUG: dict[str, Roadmap] = {roadmap.slug: roadmap for roadmap in ROADMAPS}


def all_roadmaps() -> tuple[Roadmap, ...]:
    return ROADMAPS


def get_roadmap(slug: str) -> Roadmap | None:
    return _BY_SLUG.get(slug)


def roadmap_count() -> int:
    return len(ROADMAPS)


def lesson_count() -> int:
    return sum(r.lesson_count for r in ROADMAPS)
