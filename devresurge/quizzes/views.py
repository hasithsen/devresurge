from __future__ import annotations

from typing import Any

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
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


class BadgeCabinetView(LoginRequiredMixin, ListView):
    """Owner view of earned + available badges."""

    template_name = "quizzes/badge_cabinet.html"
    context_object_name = "earned"

    def get_queryset(self):
        return (
            UserBadge.objects.filter(user=self.request.user)
            .select_related("badge")
            .order_by("-earned_at")
        )

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        from .models import Badge

        ctx = super().get_context_data(**kwargs)
        earned_ids = {ub.badge_id for ub in ctx["earned"]}
        ctx["available"] = Badge.objects.filter(is_active=True).exclude(pk__in=earned_ids)
        return ctx


quiz_list_view = QuizListView.as_view()
quiz_detail_view = QuizDetailView.as_view()
badge_cabinet_view = BadgeCabinetView.as_view()
