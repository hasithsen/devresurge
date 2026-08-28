"""Catalog of FAANG-oriented roadmaps and lessons (code-as-CMS)."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Any

from .content import backend
from .content import career_paths
from .content import databases
from .content import devops
from .content import distributed
from .content import dsa
from .content import elite_path
from .content import foundations
from .content import sponsor_employer_paths
from .content import system_design
from .content import volvo_devops_interview
from .content.career_references import CAREER_REF_BY_KEY
from .content.devops_references import REF_BY_KEY as DEVOPS_REF_BY_KEY
from .devops_lesson_refs import ref_keys_for_lesson
from .flavor import flavor_for

REF_BY_KEY: dict[str, str] = {**DEVOPS_REF_BY_KEY, **CAREER_REF_BY_KEY}

TRACK_LABELS: dict[str, str] = {
    "craft": "Core craft",
    "interview": "Interview sprints",
    "elective": "Shared electives",
    "relocation": "Regional electives",
    "sponsor": "Migration sponsor paths",
}

TRACK_ORDER: tuple[str, ...] = ("interview", "elective", "relocation", "sponsor", "craft")

# Backwards-compatible URLs → merged questlines
SLUG_ALIASES: dict[str, str] = {
    "devops-interview-30-day": "devops-interview",
    "data-eng-interview-30-day": "data-eng-interview",
    "volvo-sponsor-path": "sponsor-employers-sweden",
    "ifs-sponsor-sweden": "sponsor-employers-sweden",
    "ifs-sponsor-australia": "sponsor-employers-australia",
    "ifs-sponsor-usa": "sponsor-employers-usa",
}

_LEGACY_REGION_SUFFIXES: tuple[str, ...] = (
    "sweden",
    "australia",
    "new-zealand",
    "usa",
    "uk",
)

_LEGACY_ROLE_PREFIXES: tuple[str, ...] = (
    "devops-interview",
    "devsecops-interview",
    "data-eng-interview",
    "data-science-interview",
    "qa-interview",
    "backend-interview",
    "cloud-interview",
)

for _region in _LEGACY_REGION_SUFFIXES:
    _reloc = f"relocation-{_region}"
    for _role in _LEGACY_ROLE_PREFIXES:
        SLUG_ALIASES[f"{_role}-{_region}"] = _reloc


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
    track: str = "craft"
    related_roadmap_slugs: tuple[str, ...] = ()
    elective: bool = False

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


def _append_reference_blocks(body: str, ref_keys: tuple[str, ...]) -> str:
    if not ref_keys:
        return body
    blocks: list[str] = [body]
    seen: set[str] = set()
    for key in ref_keys:
        if key in seen:
            continue
        block = REF_BY_KEY.get(key)
        if block:
            blocks.append(block.strip())
            seen.add(key)
    return "\n\n".join(blocks)


def _as_text(value: Any) -> str:
    """Coerce roadmap string fields; join accidental tuple/list audiences."""
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, (tuple, list)):
        return " ".join(str(part) for part in value if part is not None)
    return str(value)


def _lesson(data: dict[str, Any]) -> Lesson:
    minutes = int(data.get("minutes", 12))
    hook, boss_fight = flavor_for(data["slug"])
    ref_keys = ref_keys_for_lesson(data["slug"], tuple(data.get("refs") or ()))
    return Lesson(
        slug=data["slug"],
        title=data["title"],
        summary=data["summary"],
        body=_append_reference_blocks(data["body"].strip(), ref_keys),
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
        tagline=_as_text(data["tagline"]),
        description=_as_text(data["description"]),
        domain=data["domain"],
        level=data["level"],
        icon=data["icon"],
        order=int(data["order"]),
        audience=_as_text(data["audience"]),
        outcomes=tuple(data.get("outcomes") or ()),
        lessons=tuple(_lesson(item) for item in data["lessons"]),
        related_quiz_slugs=tuple(data.get("related_quiz_slugs") or ()),
        track=str(data.get("track") or "craft"),
        related_roadmap_slugs=tuple(data.get("related_roadmap_slugs") or ()),
        elective=bool(data.get("elective")),
    )


ROADMAP_SOURCES: tuple[dict[str, Any], ...] = (
    foundations.ROADMAP,
    dsa.ROADMAP,
    system_design.ROADMAP,
    backend.ROADMAP,
    volvo_devops_interview.ROADMAP,
    *career_paths.ROADMAPS,
    *sponsor_employer_paths.SPONSOR_ROADMAPS,
    devops.ROADMAP,
    databases.ROADMAP,
    distributed.ROADMAP,
    elite_path.ROADMAP,
)

_built = tuple(
    sorted((_roadmap(src) for src in ROADMAP_SOURCES), key=lambda r: (r.order, r.title)),
)
_dupes = [slug for slug, n in Counter(r.slug for r in _built).items() if n > 1]
if _dupes:
    msg = f"Duplicate roadmap slug(s): {', '.join(sorted(_dupes))}"
    raise RuntimeError(msg)

ROADMAPS: tuple[Roadmap, ...] = _built

_BY_SLUG: dict[str, Roadmap] = {roadmap.slug: roadmap for roadmap in ROADMAPS}


def resolve_roadmap_slug(slug: str) -> str:
    return SLUG_ALIASES.get(slug, slug)


def all_roadmaps() -> tuple[Roadmap, ...]:
    return ROADMAPS


def get_roadmap(slug: str) -> Roadmap | None:
    return _BY_SLUG.get(resolve_roadmap_slug(slug))


def roadmaps_by_track() -> dict[str, tuple[Roadmap, ...]]:
    buckets: dict[str, list[Roadmap]] = {key: [] for key in TRACK_ORDER}
    buckets.setdefault("craft", [])
    for roadmap in ROADMAPS:
        track = roadmap.track if roadmap.track in buckets else "craft"
        buckets[track].append(roadmap)
    return {key: tuple(buckets.get(key, ())) for key in TRACK_ORDER if buckets.get(key)}


def relocation_electives() -> tuple[Roadmap, ...]:
    return tuple(r for r in ROADMAPS if r.track == "relocation")


def interview_sprints() -> tuple[Roadmap, ...]:
    return tuple(r for r in ROADMAPS if r.track == "interview")


def related_roadmaps(slugs: tuple[str, ...]) -> tuple[Roadmap, ...]:
    items: list[Roadmap] = []
    for slug in slugs:
        roadmap = get_roadmap(slug)
        if roadmap is not None:
            items.append(roadmap)
    return tuple(items)


def roadmap_count() -> int:
    return len(ROADMAPS)


def lesson_count() -> int:
    return sum(r.lesson_count for r in ROADMAPS)
