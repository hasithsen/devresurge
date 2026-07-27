from __future__ import annotations

from http import HTTPStatus

import pytest
from django.urls import reverse

from devresurge.quizzes.awards import award_badge
from devresurge.quizzes.awards import evaluate_connection_badges
from devresurge.quizzes.awards import evaluate_quiz_badges
from devresurge.quizzes.catalog import seed_catalog
from devresurge.quizzes.models import Quiz
from devresurge.quizzes.models import QuizAttempt
from devresurge.quizzes.models import UserBadge
from devresurge.users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


@pytest.fixture
def seeded_quizzes():
    seed_catalog(refresh_questions=True)
    return Quiz.objects.filter(is_published=True)


def test_quiz_list_renders(client, seeded_quizzes):
    response = client.get(reverse("quizzes:list"))
    assert response.status_code == HTTPStatus.OK
    body = response.content.decode()
    assert "Python fundamentals" in body


def test_quiz_take_requires_login(client, seeded_quizzes):
    quiz = Quiz.objects.get(slug="python-fundamentals")
    response = client.get(reverse("quizzes:take", kwargs={"slug": quiz.slug}))
    assert response.status_code == HTTPStatus.FOUND
    assert "/accounts/login/" in response.url


def test_quiz_pass_awards_badge(client, seeded_quizzes):
    user = UserFactory()
    client.force_login(user)
    quiz = Quiz.objects.get(slug="python-fundamentals")
    payload = {}
    for question in quiz.questions.prefetch_related("choices"):
        correct = question.choices.get(is_correct=True)
        payload[f"q_{question.pk}"] = str(correct.pk)

    response = client.post(reverse("quizzes:take", kwargs={"slug": quiz.slug}), data=payload)
    assert response.status_code == HTTPStatus.OK
    attempt = QuizAttempt.objects.get(user=user, quiz=quiz)
    assert attempt.passed is True
    assert UserBadge.objects.filter(user=user, badge__slug="quiz_python").exists()


def test_quiz_fail_does_not_award_badge(client, seeded_quizzes):
    user = UserFactory()
    client.force_login(user)
    quiz = Quiz.objects.get(slug="python-fundamentals")
    payload = {}
    for question in quiz.questions.prefetch_related("choices"):
        wrong = question.choices.filter(is_correct=False).first()
        payload[f"q_{question.pk}"] = str(wrong.pk)

    client.post(reverse("quizzes:take", kwargs={"slug": quiz.slug}), data=payload)
    attempt = QuizAttempt.objects.get(user=user, quiz=quiz)
    assert attempt.passed is False
    assert not UserBadge.objects.filter(user=user, badge__slug="quiz_python").exists()


def test_award_badge_is_idempotent(seeded_quizzes):
    user = UserFactory()
    first = award_badge(user, "first_link")
    second = award_badge(user, "first_link")
    assert first is not None
    assert second is None
    assert UserBadge.objects.filter(user=user, badge__slug="first_link").count() == 1


def test_connection_badges_scale(seeded_quizzes):
    from devresurge.connections.models import Connection
    from devresurge.connections.models import ConnectionStatus

    me = UserFactory()
    for _ in range(5):
        other = UserFactory()
        Connection.objects.create(
            requester=me,
            addressee=other,
            status=ConnectionStatus.ACCEPTED,
        )
    evaluate_connection_badges(me)
    slugs = set(UserBadge.objects.filter(user=me).values_list("badge__slug", flat=True))
    assert "first_link" in slugs
    assert "networker" in slugs


def test_quiz_streak_badge(seeded_quizzes):
    user = UserFactory()
    for slug, badge in (
        ("python-fundamentals", "quiz_python"),
        ("git-collaboration", "quiz_git"),
        ("django-basics", "quiz_django"),
    ):
        quiz = Quiz.objects.get(slug=slug)
        attempt = QuizAttempt.objects.create(
            user=user,
            quiz=quiz,
            score=5,
            total=5,
            percent=100,
            passed=True,
        )
        evaluate_quiz_badges(user, attempt)
        assert UserBadge.objects.filter(user=user, badge__slug=badge).exists()

    assert UserBadge.objects.filter(user=user, badge__slug="quiz_streak").exists()


def test_badge_cabinet_requires_login(client):
    response = client.get(reverse("quizzes:badges"))
    assert response.status_code == HTTPStatus.FOUND


def test_public_profile_shows_earned_badges(client, seeded_quizzes):
    user = UserFactory()
    award_badge(user, "quiz_python")
    response = client.get(
        reverse("profiles:public", kwargs={"handle": user.profile.handle}),
    )
    assert response.status_code == HTTPStatus.OK
    assert b"Python Pulse" in response.content
