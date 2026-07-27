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
from django.views.generic import DetailView
from django.views.generic import ListView

from .awards import evaluate_quiz_badges
from .badge_svg import render_achievement_badge_svg
from .models import Badge
from .models import Choice
from .models import Quiz
from .models import QuizAttempt
from .models import UserBadge


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

    if passed:
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
        return ctx


def badge_svg_view(request: HttpRequest, slug: str) -> HttpResponse:
    badge = get_object_or_404(Badge, slug=slug, is_active=True)
    svg = render_achievement_badge_svg(badge)
    response = HttpResponse(svg, content_type="image/svg+xml; charset=utf-8")
    response["Cache-Control"] = "public, max-age=3600"
    return response


def badge_holder_svg_view(request: HttpRequest, slug: str, handle: str) -> HttpResponse:
    """SVG proving a public profile earned this badge."""
    from devresurge.profiles.models import Profile

    badge = get_object_or_404(Badge, slug=slug, is_active=True)
    profile = get_object_or_404(Profile, handle=handle, is_public=True)
    if not UserBadge.objects.filter(user=profile.user, badge=badge).exists():
        return HttpResponse(status=404)
    svg = render_achievement_badge_svg(badge, holder_handle=profile.handle)
    response = HttpResponse(svg, content_type="image/svg+xml; charset=utf-8")
    response["Cache-Control"] = "public, max-age=3600"
    return response


quiz_list_view = QuizListView.as_view()
quiz_detail_view = QuizDetailView.as_view()
badge_cabinet_view = BadgeCabinetView.as_view()
badge_detail_view = BadgeDetailView.as_view()
