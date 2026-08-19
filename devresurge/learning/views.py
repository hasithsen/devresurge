from __future__ import annotations

from django.http import Http404
from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import render

from devresurge.profiles.markdown import render_markdown
from devresurge.quizzes.models import Quiz

from .catalog import all_roadmaps
from .catalog import get_roadmap


def roadmap_list_view(request: HttpRequest) -> HttpResponse:
    roadmaps = all_roadmaps()
    by_domain: dict[str, list] = {}
    for roadmap in roadmaps:
        by_domain.setdefault(roadmap.domain, []).append(roadmap)
    return render(
        request,
        "learning/roadmap_list.html",
        {
            "roadmaps": roadmaps,
            "domains": by_domain,
            "roadmap_count": len(roadmaps),
            "lesson_count": sum(r.lesson_count for r in roadmaps),
        },
    )


def roadmap_detail_view(request: HttpRequest, roadmap_slug: str) -> HttpResponse:
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

    return render(
        request,
        "learning/roadmap_detail.html",
        {
            "roadmap": roadmap,
            "related_quizzes": quizzes,
        },
    )


def lesson_detail_view(
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

    idx = roadmap.lesson_index(lesson_slug)
    prev_lesson = roadmap.lessons[idx - 1] if idx > 0 else None
    next_lesson = roadmap.lessons[idx + 1] if idx < len(roadmap.lessons) - 1 else None

    related_quiz = None
    if lesson.quiz_slug:
        related_quiz = Quiz.objects.filter(slug=lesson.quiz_slug, is_published=True).first()

    return render(
        request,
        "learning/lesson_detail.html",
        {
            "roadmap": roadmap,
            "lesson": lesson,
            "body_html": render_markdown(lesson.body),
            "prev_lesson": prev_lesson,
            "next_lesson": next_lesson,
            "lesson_number": idx + 1,
            "related_quiz": related_quiz,
        },
    )
