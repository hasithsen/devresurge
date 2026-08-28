from __future__ import annotations

from typing import Any

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.decorators.http import require_POST

from devresurge.profiles.markdown import render_markdown
from devresurge.quizzes.models import Quiz

from .catalog import TRACK_LABELS
from .catalog import TRACK_ORDER
from .catalog import all_roadmaps
from .catalog import get_roadmap
from .catalog import related_roadmaps
from .catalog import relocation_electives
from .catalog import resolve_roadmap_slug
from .progress import annotate_roadmaps
from .progress import completed_keys
from .progress import continue_target
from .progress import global_stats
from .progress import mark_completed
from .progress import mark_started
from .progress import roadmap_stats
from .toc import lesson_headings


def roadmap_list_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST" and "learn_region" in request.POST:
        region = request.POST.get("learn_region", "").strip()
        if region in ("", "sweden", "australia", "new-zealand", "usa", "uk"):
            request.session["learn_region"] = region

    roadmaps = all_roadmaps()
    track_sections: list[dict[str, Any]] = []
    for track in TRACK_ORDER:
        rows = [row for row in annotate_roadmaps(request.user) if row["roadmap"].track == track]
        if rows:
            track_sections.append(
                {
                    "track": track,
                    "label": TRACK_LABELS[track],
                    "rows": rows,
                }
            )

    craft_by_domain: dict[str, list] = {}
    for row in annotate_roadmaps(request.user):
        if row["roadmap"].track == "craft":
            craft_by_domain.setdefault(row["roadmap"].domain, []).append(row)

    preferred_region = request.session.get("learn_region", "")
    preferred_elective = get_roadmap(f"relocation-{preferred_region}") if preferred_region else None

    resume = continue_target(request.user) if request.user.is_authenticated else None
    stats = global_stats(request.user) if request.user.is_authenticated else None
    return render(
        request,
        "learning/roadmap_list.html",
        {
            "roadmaps": roadmaps,
            "track_sections": track_sections,
            "craft_domains": craft_by_domain,
            "roadmap_count": len(roadmaps),
            "lesson_count": sum(r.lesson_count for r in roadmaps),
            "resume": resume,
            "learn_stats": stats,
            "preferred_region": preferred_region,
            "preferred_elective": preferred_elective,
            "relocation_electives": relocation_electives(),
        },
    )


def roadmap_detail_view(request: HttpRequest, roadmap_slug: str) -> HttpResponse:
    canonical = resolve_roadmap_slug(roadmap_slug)
    if canonical != roadmap_slug:
        return redirect("learning:roadmap", canonical)

    roadmap = get_roadmap(roadmap_slug)
    if roadmap is None:
        raise Http404("Roadmap not found")

    quizzes = []
    if roadmap.related_quiz_slugs:
        quiz_map = {
            q.slug: q
            for q in Quiz.objects.filter(
                slug__in=roadmap.related_quiz_slugs,
                is_published=True,
            )
        }
        quizzes = [quiz_map[slug] for slug in roadmap.related_quiz_slugs if slug in quiz_map]

    stats = None
    completed: set[str] = set()
    if request.user.is_authenticated:
        stats = roadmap_stats(request.user, roadmap)
        completed = {
            slug
            for rm, slug in completed_keys(request.user)
            if rm == roadmap.slug
        }

    start_lesson = stats["next_lesson"] if stats and stats["next_lesson"] else roadmap.lessons[0]
    paired_roadmaps = related_roadmaps(roadmap.related_roadmap_slugs)
    preferred_region = request.session.get("learn_region", "")
    highlighted_elective = (
        get_roadmap(f"relocation-{preferred_region}") if preferred_region else None
    )
    return render(
        request,
        "learning/roadmap_detail.html",
        {
            "roadmap": roadmap,
            "description_html": render_markdown(roadmap.description),
            "related_quizzes": quizzes,
            "learn_stats": stats,
            "completed_lessons": completed,
            "start_lesson": start_lesson,
            "paired_roadmaps": paired_roadmaps,
            "highlighted_elective": highlighted_elective,
        },
    )


@login_required
def lesson_detail_view(
    request: HttpRequest,
    roadmap_slug: str,
    lesson_slug: str,
) -> HttpResponse:
    canonical = resolve_roadmap_slug(roadmap_slug)
    if canonical != roadmap_slug:
        return redirect("learning:lesson", canonical, lesson_slug)

    roadmap = get_roadmap(roadmap_slug)
    if roadmap is None:
        raise Http404("Roadmap not found")
    lesson = roadmap.get_lesson(lesson_slug)
    if lesson is None:
        raise Http404("Lesson not found")

    progress = mark_started(request.user, roadmap.slug, lesson.slug)

    idx = roadmap.lesson_index(lesson_slug)
    prev_lesson = roadmap.lessons[idx - 1] if idx > 0 else None
    next_lesson = roadmap.lessons[idx + 1] if idx < len(roadmap.lessons) - 1 else None

    related_quiz = None
    if lesson.quiz_slug:
        related_quiz = Quiz.objects.filter(slug=lesson.quiz_slug, is_published=True).first()

    stats = roadmap_stats(request.user, roadmap)
    headings = lesson_headings(lesson.body)
    return render(
        request,
        "learning/lesson_detail.html",
        {
            "roadmap": roadmap,
            "lesson": lesson,
            "body_html": render_markdown(lesson.body, heading_ids=True),
            "lesson_headings": headings,
            "prev_lesson": prev_lesson,
            "next_lesson": next_lesson,
            "lesson_number": idx + 1,
            "related_quiz": related_quiz,
            "progress": progress,
            "learn_stats": stats,
        },
    )


@login_required
@require_POST
def lesson_complete_view(
    request: HttpRequest,
    roadmap_slug: str,
    lesson_slug: str,
) -> HttpResponse:
    roadmap = get_roadmap(roadmap_slug)
    if roadmap is None:
        raise Http404("Roadmap not found")
    lesson = roadmap.get_lesson(lesson_slug)
    if lesson is None:
        raise Http404("Lesson not found")

    progress = mark_completed(request.user, roadmap.slug, lesson.slug)
    if progress.is_completed:
        messages.success(
            request,
            f"Quest cleared. +{lesson.xp} XP — {lesson.title}.",
        )

    idx = roadmap.lesson_index(lesson_slug)
    if idx >= 0 and idx < len(roadmap.lessons) - 1:
        nxt = roadmap.lessons[idx + 1]
        return redirect("learning:lesson", roadmap.slug, nxt.slug)
    return redirect("learning:roadmap", roadmap.slug)
