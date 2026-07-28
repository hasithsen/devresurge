from __future__ import annotations

from typing import Any

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import DetailView
from django.views.generic import ListView

from .awards import evaluate_quiz_badges
from .badge_svg import render_achievement_badge_svg
from .models import Badge
from .models import Choice
from .models import Quiz
from .models import QuizAttempt
from .models import UserBadge
from .share import build_badge_share_links


class QuizListView(ListView):
    model = Quiz
    template_name = "quizzes/quiz_list.html"
    context_object_name = "quizzes"

    def get_queryset(self):
        return (
            Quiz.objects.filter(is_published=True)
            .prefetch_related("questions")
        )

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        user = self.request.user
        best: dict[int, QuizAttempt] = {}
        if user.is_authenticated:
            for attempt in (
                QuizAttempt.objects.filter(user=user)
                .order_by("quiz_id", "-percent", "-created_at")
            ):
                best.setdefault(attempt.quiz_id, attempt)
        rows = []
        earned = set()
        if user.is_authenticated:
            earned = set(
                UserBadge.objects.filter(user=user).values_list("badge__slug", flat=True),
            )
        for quiz in ctx["quizzes"]:
            rows.append(
                {
                    "quiz": quiz,
                    "best": best.get(quiz.pk),
                    "earned": quiz.badge_slug in earned if quiz.badge_slug else False,
                },
            )
        ctx["quiz_rows"] = rows
        return ctx


class QuizDetailView(DetailView):
    model = Quiz
    template_name = "quizzes/quiz_detail.html"
    context_object_name = "quiz"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return Quiz.objects.filter(is_published=True).prefetch_related(
            "questions__choices",
        )

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        user = self.request.user
        ctx["prior_pass"] = False
        ctx["best_attempt"] = None
        if user.is_authenticated:
            attempts = QuizAttempt.objects.filter(user=user, quiz=self.object)
            ctx["prior_pass"] = attempts.filter(passed=True).exists()
            ctx["best_attempt"] = attempts.order_by("-percent", "-created_at").first()
        return ctx


@login_required
def quiz_take_view(request: HttpRequest, slug: str) -> HttpResponse:
    quiz = get_object_or_404(
        Quiz.objects.filter(is_published=True).prefetch_related("questions__choices"),
        slug=slug,
    )
    questions = list(quiz.questions.all())
    if not questions:
        messages.error(request, "This quiz has no questions yet.")
        return redirect(quiz.get_absolute_url())

    if request.method == "POST":
        return _grade_attempt(request, quiz, questions)

    return render(
        request,
        "quizzes/quiz_take.html",
        {"quiz": quiz, "questions": questions},
    )


def _grade_attempt(request: HttpRequest, quiz: Quiz, questions: list) -> HttpResponse:
    score = 0
    total = len(questions)
    review: list[dict] = []

    for question in questions:
        field = f"q_{question.pk}"
        raw = request.POST.get(field)
        try:
            choice_id = int(raw) if raw is not None else None
        except (TypeError, ValueError):
            choice_id = None

        selected = None
        correct = question.choices.filter(is_correct=True).first()
        is_right = False
        if choice_id is not None:
            selected = Choice.objects.filter(pk=choice_id, question=question).first()
            if selected is not None and selected.is_correct:
                is_right = True
                score += 1

        review.append(
            {
                "question": question,
                "selected": selected,
                "correct": correct,
                "is_right": is_right,
            },
        )

    percent = round((score / total) * 100) if total else 0
    passed = percent >= quiz.pass_percent

    with transaction.atomic():
        attempt = QuizAttempt.objects.create(
            user=request.user,
            quiz=quiz,
            score=score,
            total=total,
            percent=percent,
            passed=passed,
        )
    awarded = evaluate_quiz_badges(request.user, attempt) if passed else []

    celebrate = None
    extra_awards = []
    if passed and quiz.badge_slug:
        quiz_badge = Badge.objects.filter(slug=quiz.badge_slug, is_active=True).first()
        holds_quiz_badge = bool(
            quiz_badge
            and (
                any(ub.badge_id == quiz_badge.pk for ub in awarded)
                or UserBadge.objects.filter(
                    user=request.user,
                    badge=quiz_badge,
                ).exists()
            )
        )
        if quiz_badge and holds_quiz_badge:
            newly = next((ub for ub in awarded if ub.badge_id == quiz_badge.pk), None)
            profile = getattr(request.user, "profile", None)
            page_url = request.build_absolute_uri(quiz_badge.get_absolute_url())
            share = build_badge_share_links(
                page_url=page_url,
                title=quiz_badge.title,
                description=quiz_badge.description,
                earned=True,
            )
            show_holder = bool(profile is not None and profile.is_public and profile.handle)
            if show_holder:
                preview_svg_url = reverse(
                    "quizzes:badge_holder_svg",
                    kwargs={"slug": quiz_badge.slug, "handle": profile.handle},
                )
            else:
                preview_svg_url = reverse(
                    "quizzes:badge_svg",
                    kwargs={"slug": quiz_badge.slug},
                )
            celebrate = {
                "badge": quiz_badge,
                "award": newly,
                "is_new": newly is not None,
                "share": share,
                "preview_svg_url": preview_svg_url,
                "show_holder": show_holder,
                "holder_handle": profile.handle if show_holder else None,
            }
            extra_awards = [ub for ub in awarded if ub.badge_id != quiz_badge.pk]
        else:
            extra_awards = list(awarded)
    elif awarded:
        extra_awards = list(awarded)

    share_extras = []
    for ub in extra_awards:
        share_extras.append(
            {
                "award": ub,
                "share": build_badge_share_links(
                    page_url=request.build_absolute_uri(ub.badge.get_absolute_url()),
                    title=ub.badge.title,
                    description=ub.badge.description,
                    earned=True,
                ),
            },
        )

    if passed:
        if celebrate and celebrate["is_new"]:
            messages.success(
                request,
                f"Passed at {percent}% — badge unlocked. Share it.",
            )
        else:
            messages.success(
                request,
                f"Passed at {percent}% — nice work.",
            )
    else:
        messages.info(
            request,
            f"Scored {percent}%. Need {quiz.pass_percent}% to pass — try again.",
        )

    return render(
        request,
        "quizzes/quiz_result.html",
        {
            "quiz": quiz,
            "attempt": attempt,
            "review": review,
            "awarded": awarded,
            "celebrate": celebrate,
            "share_extras": share_extras,
        },
    )


class BadgeCabinetView(ListView):
    """Public badge catalog; shows earned set when authenticated."""

    template_name = "quizzes/badge_cabinet.html"
    context_object_name = "catalog"
    queryset = Badge.objects.filter(is_active=True)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        earned_map: dict[int, UserBadge] = {}
        if self.request.user.is_authenticated:
            for ub in (
                UserBadge.objects.filter(user=self.request.user)
                .select_related("badge")
                .order_by("-earned_at")
            ):
                earned_map[ub.badge_id] = ub
        rows = []
        for badge in ctx["catalog"]:
            rows.append({"badge": badge, "award": earned_map.get(badge.pk)})
        ctx["rows"] = rows
        ctx["earned_count"] = len(earned_map)
        return ctx


class BadgeDetailView(DetailView):
    """Public, linkable badge page with recent holders + embed URLs."""

    model = Badge
    template_name = "quizzes/badge_detail.html"
    context_object_name = "badge"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return Badge.objects.filter(is_active=True)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        badge = self.object
        awards = (
            UserBadge.objects.filter(badge=badge, user__profile__is_public=True)
            .select_related("user__profile")
            .order_by("-earned_at")[:24]
        )
        ctx["holders"] = awards
        ctx["holder_count"] = UserBadge.objects.filter(badge=badge).count()
        ctx["viewer_award"] = None
        if self.request.user.is_authenticated:
            ctx["viewer_award"] = UserBadge.objects.filter(
                user=self.request.user,
                badge=badge,
            ).first()
        related_quiz = None
        if badge.slug.startswith("quiz_"):
            related_quiz = Quiz.objects.filter(
                badge_slug=badge.slug,
                is_published=True,
            ).first()
        ctx["related_quiz"] = related_quiz
        profile = getattr(self.request.user, "profile", None) if self.request.user.is_authenticated else None
        ctx["show_holder_svg"] = bool(
            ctx["viewer_award"] and profile is not None and profile.is_public,
        )
        ctx["holder_handle"] = profile.handle if ctx["show_holder_svg"] else None
        # Social share + embed tooling only after the viewer has earned the badge.
        if ctx["viewer_award"]:
            ctx["share"] = build_badge_share_links(
                page_url=self.request.build_absolute_uri(badge.get_absolute_url()),
                title=badge.title,
                description=badge.description,
                earned=True,
            )
            if ctx["show_holder_svg"] and ctx["holder_handle"]:
                ctx["preview_svg_url"] = reverse(
                    "quizzes:badge_holder_svg",
                    kwargs={"slug": badge.slug, "handle": ctx["holder_handle"]},
                )
            else:
                ctx["preview_svg_url"] = reverse(
                    "quizzes:badge_svg",
                    kwargs={"slug": badge.slug},
                )
            ctx["preview_locked"] = False
        else:
            ctx["share"] = None
            ctx["preview_svg_url"] = reverse(
                "quizzes:badge_locked_svg",
                kwargs={"slug": badge.slug},
            )
            ctx["preview_locked"] = True
        return ctx


def badge_svg_view(request: HttpRequest, slug: str) -> HttpResponse:
    """Public catalog SVG — the shareable earned look for embeds."""
    badge = get_object_or_404(Badge, slug=slug, is_active=True)
    svg = render_achievement_badge_svg(badge)
    response = HttpResponse(svg, content_type="image/svg+xml; charset=utf-8")
    response["Cache-Control"] = "public, max-age=60, must-revalidate"
    return response


def badge_locked_svg_view(request: HttpRequest, slug: str) -> HttpResponse:
    """Muted preview for viewers who have not earned the badge yet."""
    badge = get_object_or_404(Badge, slug=slug, is_active=True)
    svg = render_achievement_badge_svg(badge, locked=True)
    response = HttpResponse(svg, content_type="image/svg+xml; charset=utf-8")
    response["Cache-Control"] = "public, max-age=60, must-revalidate"
    return response


def badge_holder_svg_view(request: HttpRequest, slug: str, handle: str) -> HttpResponse:
    """SVG proving a public profile earned this badge."""
    from devresurge.profiles.models import Profile

    badge = get_object_or_404(Badge, slug=slug, is_active=True)
    profile = get_object_or_404(Profile, handle=handle, is_public=True)
    if not UserBadge.objects.filter(user=profile.user, badge=badge).exists():
        # Unearned claim — never emit a personalized badge SVG.
        return HttpResponse(status=404)
    svg = render_achievement_badge_svg(badge, holder_handle=profile.handle)
    response = HttpResponse(svg, content_type="image/svg+xml; charset=utf-8")
    response["Cache-Control"] = "public, max-age=60, must-revalidate"
    return response


quiz_list_view = QuizListView.as_view()
quiz_detail_view = QuizDetailView.as_view()
badge_cabinet_view = BadgeCabinetView.as_view()
badge_detail_view = BadgeDetailView.as_view()
