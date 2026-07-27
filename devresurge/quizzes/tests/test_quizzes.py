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


def test_badge_cabinet_is_public(client, seeded_quizzes):
    response = client.get(reverse("quizzes:badges"))
    assert response.status_code == HTTPStatus.OK
    assert b"Python Pulse" in response.content


def test_badge_detail_and_svg(client, seeded_quizzes):
    response = client.get(reverse("quizzes:badge_detail", kwargs={"slug": "quiz_python"}))
    assert response.status_code == HTTPStatus.OK
    assert b"Python Pulse" in response.content
    # Unearned visitors do not get social share controls.
    assert b"LinkedIn" not in response.content
    assert response.context["share"] is None
    assert b"Earn this badge" in response.content or b"Sign in and earn" in response.content

    svg = client.get(reverse("quizzes:badge_svg", kwargs={"slug": "quiz_python"}))
    assert svg.status_code == HTTPStatus.OK
    assert svg["Content-Type"].startswith("image/svg+xml")
    body = svg.content.decode()
    assert "Python Pulse" in body
    for word in "Passed the Python fundamentals quiz.".split():
        assert word in body
    assert "…" not in body


def test_badge_detail_share_only_when_earned(client, seeded_quizzes):
    user = UserFactory()
    award_badge(user, "quiz_python")
    client.force_login(user)

    response = client.get(reverse("quizzes:badge_detail", kwargs={"slug": "quiz_python"}))
    assert response.status_code == HTTPStatus.OK
    assert b"LinkedIn" in response.content
    share = response.context["share"]
    assert share is not None
    assert "linkedin.com/sharing/share-offsite" in share["linkedin"]
    assert "twitter.com/intent/tweet" in share["x"]
    assert "reddit.com/submit" in share["reddit"]
    assert share["email"].startswith("mailto:")
    assert "I earned" in share["caption"]
    assert "quiz_python" in share["page_url"]

    # A different unearned badge stays locked for sharing.
    locked = client.get(reverse("quizzes:badge_detail", kwargs={"slug": "quiz_git"}))
    assert locked.status_code == HTTPStatus.OK
    assert locked.context["share"] is None
    assert b"LinkedIn" not in locked.content


def test_achievement_badge_svg_fits_long_copy(seeded_quizzes):
    from devresurge.quizzes.badge_svg import render_achievement_badge_svg
    from devresurge.quizzes.models import Badge

    badge = Badge.objects.get(slug="profile_ready")
    svg = render_achievement_badge_svg(badge)
    for word in "Completed every item on the setup.sh checklist.".split():
        assert word in svg
    assert "…" not in svg


def test_python_pulse_badge_shows_full_description(seeded_quizzes):
    from devresurge.quizzes.badge_svg import render_achievement_badge_svg
    from devresurge.quizzes.models import Badge

    badge = Badge.objects.get(slug="quiz_python")
    svg = render_achievement_badge_svg(badge)
    assert "Python Pulse" in svg
    # May wrap across <text> lines — every word must still be present.
    for word in "Passed the Python fundamentals quiz.".split():
        assert word in svg
    assert "…" not in svg
    width = int(svg.split('width="', 1)[1].split('"', 1)[0])
    assert width <= 380


def test_all_catalog_badge_svgs_have_full_descriptions(seeded_quizzes):
    from devresurge.quizzes.badge_svg import render_achievement_badge_svg
    from devresurge.quizzes.models import Badge
    from devresurge.svg_text import text_width

    for badge in Badge.objects.filter(is_active=True):
        svg = render_achievement_badge_svg(badge)
        for word in badge.description.split():
            assert word in svg, f"{badge.slug} missing {word!r}"
        assert "…" not in svg, f"{badge.slug} still ellipsizes"
        width = int(svg.split('width="', 1)[1].split('"', 1)[0])
        assert width <= 380
        # Every body <text> line must fit the content box (pad 56+18).
        content_w = width - 56 - 18
        for chunk in svg.split("<text ")[1:]:
            if 'fill="#7a8a85"' not in chunk and 'fill="#7cf0a8"' not in chunk:
                continue
            text = chunk.split(">", 1)[1].split("</text>", 1)[0]
            # Skip icon circle text (centered at x=34).
            if 'x="34"' in chunk:
                continue
            assert text_width(text, 12) <= content_w + 1, (
                f"{badge.slug} overflows: {text!r}"
            )


def test_badge_holder_svg(client, seeded_quizzes):
    user = UserFactory()
    user.profile.is_public = True
    user.profile.save(update_fields=["is_public"])
    award_badge(user, "quiz_python")
    response = client.get(
        reverse(
            "quizzes:badge_holder_svg",
            kwargs={"slug": "quiz_python", "handle": user.profile.handle},
        ),
    )
    assert response.status_code == HTTPStatus.OK
    assert f"@{user.profile.handle}".encode() in response.content


def test_quiz_polyglot_badge(seeded_quizzes):
    user = UserFactory()
    for slug in (
        "python-fundamentals",
        "git-collaboration",
        "django-basics",
        "sql-fundamentals",
        "javascript-essentials",
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

    assert UserBadge.objects.filter(user=user, badge__slug="quiz_polyglot").exists()


def test_public_profile_shows_earned_badges(client, seeded_quizzes):
    user = UserFactory()
    award_badge(user, "quiz_python")
    response = client.get(
        reverse("profiles:public", kwargs={"handle": user.profile.handle}),
    )
    assert response.status_code == HTTPStatus.OK
    assert b"Python Pulse" in response.content
    assert reverse("quizzes:badge_detail", kwargs={"slug": "quiz_python"}).encode() in response.content
