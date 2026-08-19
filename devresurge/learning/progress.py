"""Helpers for lesson quest progress."""

from __future__ import annotations

from django.db import transaction
from django.utils import timezone

from .catalog import Lesson
from .catalog import Roadmap
from .catalog import all_roadmaps
from .models import LessonProgress


def mark_started(user, roadmap_slug: str, lesson_slug: str) -> LessonProgress:
    progress, _created = LessonProgress.objects.get_or_create(
        user=user,
        roadmap_slug=roadmap_slug,
        lesson_slug=lesson_slug,
        defaults={"status": LessonProgress.Status.STARTED},
    )
    return progress


def mark_completed(user, roadmap_slug: str, lesson_slug: str) -> LessonProgress:
    now = timezone.now()
    with transaction.atomic():
        progress, created = LessonProgress.objects.get_or_create(
            user=user,
            roadmap_slug=roadmap_slug,
            lesson_slug=lesson_slug,
            defaults={
                "status": LessonProgress.Status.COMPLETED,
                "completed_at": now,
            },
        )
        if not created and progress.status != LessonProgress.Status.COMPLETED:
            progress.status = LessonProgress.Status.COMPLETED
            progress.completed_at = now
            progress.save(update_fields=["status", "completed_at", "updated_at"])
    return progress


def completed_keys(user) -> set[tuple[str, str]]:
    return set(
        LessonProgress.objects.filter(
            user=user,
            status=LessonProgress.Status.COMPLETED,
        ).values_list("roadmap_slug", "lesson_slug"),
    )


def roadmap_stats(user, roadmap: Roadmap) -> dict:
    done_keys = completed_keys(user)
    done = sum(1 for lesson in roadmap.lessons if (roadmap.slug, lesson.slug) in done_keys)
    total = roadmap.lesson_count
    xp = sum(
        lesson.xp
        for lesson in roadmap.lessons
        if (roadmap.slug, lesson.slug) in done_keys
    )
    pct = round((done / total) * 100) if total else 0
    next_lesson = None
    for lesson in roadmap.lessons:
        if (roadmap.slug, lesson.slug) not in done_keys:
            next_lesson = lesson
            break
    return {
        "done": done,
        "total": total,
        "xp": xp,
        "pct": pct,
        "complete": done >= total and total > 0,
        "next_lesson": next_lesson,
    }


def global_stats(user) -> dict:
    done_keys = completed_keys(user)
    total = sum(r.lesson_count for r in all_roadmaps())
    done = 0
    xp = 0
    for roadmap in all_roadmaps():
        for lesson in roadmap.lessons:
            if (roadmap.slug, lesson.slug) in done_keys:
                done += 1
                xp += lesson.xp
    pct = round((done / total) * 100) if total else 0
    return {"done": done, "total": total, "xp": xp, "pct": pct}


def continue_target(user) -> tuple[Roadmap, Lesson] | None:
    """Resume the first incomplete lesson in a started roadmap, else the elite path."""
    done_keys = completed_keys(user)
    started_roadmaps = set(
        LessonProgress.objects.filter(user=user).values_list("roadmap_slug", flat=True),
    )
    ordered = list(all_roadmaps())
    started = [r for r in ordered if r.slug in started_roadmaps]
    rest = [r for r in ordered if r.slug not in started_roadmaps]
    for roadmap in started + rest:
        for lesson in roadmap.lessons:
            if (roadmap.slug, lesson.slug) not in done_keys:
                return roadmap, lesson
    return None


def annotate_roadmaps(user) -> list[dict]:
    done_keys = completed_keys(user) if user.is_authenticated else set()
    rows = []
    for roadmap in all_roadmaps():
        done = sum(1 for lesson in roadmap.lessons if (roadmap.slug, lesson.slug) in done_keys)
        rows.append(
            {
                "roadmap": roadmap,
                "done": done,
                "pct": round((done / roadmap.lesson_count) * 100) if roadmap.lesson_count else 0,
            },
        )
    return rows
