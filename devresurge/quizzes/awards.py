"""Award achievement badges based on profile / network / quiz activity."""

from __future__ import annotations

import logging

from django.db import IntegrityError
from django.db import transaction

from devresurge.connections.context_processors import invalidate_unread_count
from devresurge.connections.models import Connection
from devresurge.connections.models import Notification
from devresurge.connections.models import NotificationKind

from .models import Badge
from .models import QuizAttempt
from .models import UserBadge

logger = logging.getLogger(__name__)


def award_badge(user, slug: str, *, quiz_attempt: QuizAttempt | None = None) -> UserBadge | None:
    """Grant ``slug`` to ``user`` if not already held. Returns the award or None."""
    badge = Badge.objects.filter(slug=slug, is_active=True).first()
    if badge is None:
        return None
    if UserBadge.objects.filter(user=user, badge=badge).exists():
        return None
    try:
        with transaction.atomic():
            award = UserBadge.objects.create(
                user=user,
                badge=badge,
                quiz_attempt=quiz_attempt,
            )
            Notification.objects.create(
                recipient=user,
                actor=None,
                kind=NotificationKind.BADGE_EARNED,
                payload=badge.title,
            )
    except IntegrityError:
        return None
    except Exception:
        logger.exception("Failed awarding badge %s to user %s", slug, user.pk)
        return None
    invalidate_unread_count(user.pk)
    return award


def evaluate_connection_badges(user) -> list[UserBadge]:
    """Award network milestones after an accept."""
    awarded: list[UserBadge] = []
    count = Connection.objects.involving(user).accepted().count()
    if count >= 1:
        got = award_badge(user, "first_link")
        if got:
            awarded.append(got)
    if count >= 5:
        got = award_badge(user, "networker")
        if got:
            awarded.append(got)
    return awarded


def evaluate_profile_badges(user) -> list[UserBadge]:
    """Award profile-oriented badges from current profile state."""
    awarded: list[UserBadge] = []
    profile = getattr(user, "profile", None)
    if profile is None:
        return awarded

    readiness = profile.readiness()
    if readiness.get("complete"):
        got = award_badge(user, "profile_ready")
        if got:
            awarded.append(got)

    if profile.available_for_hire and profile.is_public:
        got = award_badge(user, "open_to_work")
        if got:
            awarded.append(got)

    if profile.projects.count() >= 3:
        got = award_badge(user, "shipper")
        if got:
            awarded.append(got)

    return awarded


def evaluate_quiz_badges(user, attempt: QuizAttempt) -> list[UserBadge]:
    """Award quiz + streak badges after a passing attempt."""
    awarded: list[UserBadge] = []
    if not attempt.passed:
        return awarded

    quiz = attempt.quiz
    if quiz.badge_slug:
        got = award_badge(user, quiz.badge_slug, quiz_attempt=attempt)
        if got:
            awarded.append(got)

    # Core streak: Python + Git + Django.
    needed = {"quiz_python", "quiz_git", "quiz_django"}
    held = set(
        UserBadge.objects.filter(user=user, badge__slug__in=needed).values_list(
            "badge__slug",
            flat=True,
        ),
    )
    if quiz.badge_slug:
        held.add(quiz.badge_slug)
    if needed.issubset(held):
        got = award_badge(user, "quiz_streak")
        if got:
            awarded.append(got)

    # Frontend track: JS + CSS + TypeScript.
    frontend = {"quiz_js", "quiz_css", "quiz_typescript"}
    held_fe = set(
        UserBadge.objects.filter(user=user, badge__slug__in=frontend).values_list(
            "badge__slug",
            flat=True,
        ),
    )
    if quiz.badge_slug:
        held_fe.add(quiz.badge_slug)
    if frontend.issubset(held_fe):
        got = award_badge(user, "quiz_frontend")
        if got:
            awarded.append(got)

    # Ops track: Linux + Docker + testing.
    ops = {"quiz_linux", "quiz_docker", "quiz_testing"}
    held_ops = set(
        UserBadge.objects.filter(user=user, badge__slug__in=ops).values_list(
            "badge__slug",
            flat=True,
        ),
    )
    if quiz.badge_slug:
        held_ops.add(quiz.badge_slug)
    if ops.issubset(held_ops):
        got = award_badge(user, "quiz_ops")
        if got:
            awarded.append(got)

    # Systems track: DSA + system design + distributed.
    systems = {"quiz_dsa", "quiz_system_design", "quiz_distributed"}
    held_sys = set(
        UserBadge.objects.filter(user=user, badge__slug__in=systems).values_list(
            "badge__slug",
            flat=True,
        ),
    )
    if quiz.badge_slug:
        held_sys.add(quiz.badge_slug)
    if systems.issubset(held_sys):
        got = award_badge(user, "quiz_systems")
        if got:
            awarded.append(got)

    # Infra track: networking + CI/CD + observability.
    infra = {"quiz_networking", "quiz_cicd", "quiz_observability"}
    held_infra = set(
        UserBadge.objects.filter(user=user, badge__slug__in=infra).values_list(
            "badge__slug",
            flat=True,
        ),
    )
    if quiz.badge_slug:
        held_infra.add(quiz.badge_slug)
    if infra.issubset(held_infra):
        got = award_badge(user, "quiz_infra")
        if got:
            awarded.append(got)

    # Polyglot: five or more quiz-category badges.
    quiz_slugs = set(
        UserBadge.objects.filter(user=user, badge__category="quiz").values_list(
            "badge__slug",
            flat=True,
        ),
    )
    if quiz.badge_slug:
        quiz_slugs.add(quiz.badge_slug)
    if len(quiz_slugs) >= 5:
        got = award_badge(user, "quiz_polyglot")
        if got:
            awarded.append(got)

    return awarded
