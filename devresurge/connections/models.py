from __future__ import annotations

from django.conf import settings
from django.db import models
from django.db.models import F
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class ConnectionStatus(models.TextChoices):
    PENDING = "pending", _("Pending")
    ACCEPTED = "accepted", _("Accepted")
    DECLINED = "declined", _("Declined")
    BLOCKED = "blocked", _("Blocked")


class ConnectionRelation(models.TextChoices):
    """How two people relate once connected (or when requesting)."""

    PEER = "peer", _("Peer")
    COLLABORATOR = "collaborator", _("Collaborator")
    MENTOR = "mentor", _("Mentor")
    MENTEE = "mentee", _("Mentee")
    RECRUITER = "recruiter", _("Recruiter")
    HIRING = "hiring", _("Hiring")
    FRIEND = "friend", _("Friend")
    OTHER = "other", _("Other")


class ConnectionQuerySet(models.QuerySet):
    def involving(self, user) -> ConnectionQuerySet:
        return self.filter(Q(requester=user) | Q(addressee=user))

    def pending(self) -> ConnectionQuerySet:
        return self.filter(status=ConnectionStatus.PENDING)

    def accepted(self) -> ConnectionQuerySet:
        return self.filter(status=ConnectionStatus.ACCEPTED)

    def blocked(self) -> ConnectionQuerySet:
        return self.filter(status=ConnectionStatus.BLOCKED)

    def incoming(self, user) -> ConnectionQuerySet:
        return self.filter(addressee=user, status=ConnectionStatus.PENDING)

    def outgoing(self, user) -> ConnectionQuerySet:
        return self.filter(requester=user, status=ConnectionStatus.PENDING)

    def visible_network(self, user) -> ConnectionQuerySet:
        """Accepted links for a user, excluding rows they blocked."""
        return self.involving(user).accepted()


class Connection(models.Model):
    """A directed connection request that becomes a mutual link once accepted.

    The pair is stored as an ordered (requester, addressee) tuple, but treated
    as undirected once accepted — use `Connection.between()` to look up the
    relationship regardless of who initiated it.

    ``relation`` labels *why* you're connected; ``message`` is an optional note
    attached to the request. ``BLOCKED`` is set by the blocker (always stored
    as requester=blocker) so the other party cannot re-request.
    """

    requester = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="connections_initiated",
    )
    addressee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="connections_received",
    )
    status = models.CharField(
        _("status"),
        max_length=12,
        choices=ConnectionStatus.choices,
        default=ConnectionStatus.PENDING,
        db_index=True,
    )
    relation = models.CharField(
        _("relation"),
        max_length=20,
        choices=ConnectionRelation.choices,
        default=ConnectionRelation.PEER,
        help_text=_("How you know each other."),
    )
    message = models.CharField(
        _("message"),
        max_length=280,
        blank=True,
        help_text=_("Optional note sent with the request."),
    )
    created_at = models.DateTimeField(auto_now_add=True)
    responded_at = models.DateTimeField(_("responded at"), null=True, blank=True)

    objects = ConnectionQuerySet.as_manager()

    class Meta:
        ordering = ("-created_at",)
        verbose_name = _("connection")
        verbose_name_plural = _("connections")
        constraints = [
            models.UniqueConstraint(
                fields=("requester", "addressee"),
                name="connections_unique_pair",
            ),
            models.CheckConstraint(
                condition=~Q(requester=F("addressee")),
                name="connections_no_self_link",
            ),
        ]
        indexes = [
            models.Index(fields=["addressee", "status"], name="conn_addressee_status_idx"),
            models.Index(fields=["requester", "status"], name="conn_requester_status_idx"),
            models.Index(fields=["status", "relation"], name="conn_status_relation_idx"),
        ]

    def __str__(self) -> str:
        return f"{self.requester_id} → {self.addressee_id} ({self.status})"

    @staticmethod
    def between(user_a, user_b) -> Connection | None:
        """Return the connection linking two users in either direction, if any."""
        return (
            Connection.objects.filter(
                Q(requester=user_a, addressee=user_b)
                | Q(requester=user_b, addressee=user_a),
            )
            .order_by("-created_at")
            .first()
        )

    def other_user(self, user):
        """The participant who is *not* `user`."""
        return self.addressee if self.requester_id == user.pk else self.requester

    @property
    def is_pending(self) -> bool:
        return self.status == ConnectionStatus.PENDING

    @property
    def is_accepted(self) -> bool:
        return self.status == ConnectionStatus.ACCEPTED

    @property
    def is_blocked(self) -> bool:
        return self.status == ConnectionStatus.BLOCKED

    @property
    def status_label(self) -> str:
        return self.get_status_display()

    @property
    def relation_label(self) -> str:
        return self.get_relation_display()

    def accept(self) -> None:
        self.status = ConnectionStatus.ACCEPTED
        self.responded_at = timezone.now()
        self.save(update_fields=["status", "responded_at"])

    def decline(self) -> None:
        self.status = ConnectionStatus.DECLINED
        self.responded_at = timezone.now()
        self.save(update_fields=["status", "responded_at"])

    def block(self, blocker) -> None:
        """Mark this pair blocked, with ``blocker`` as the requester."""
        other = self.other_user(blocker)
        self.requester = blocker
        self.addressee = other
        self.status = ConnectionStatus.BLOCKED
        self.responded_at = timezone.now()
        self.save(
            update_fields=["requester", "addressee", "status", "responded_at"],
        )


class NotificationKind(models.TextChoices):
    CONNECTION_REQUEST = "connection_request", _("Connection request")
    CONNECTION_ACCEPTED = "connection_accepted", _("Connection accepted")
    BADGE_EARNED = "badge_earned", _("Badge earned")
    QUIZ_PASSED = "quiz_passed", _("Quiz passed")
    SKILL_ENDORSED = "skill_endorsed", _("Skill endorsed")
    RECOMMENDATION = "recommendation", _("Recommendation")


class NotificationQuerySet(models.QuerySet):
    def for_user(self, user) -> NotificationQuerySet:
        return self.filter(recipient=user)

    def unread(self) -> NotificationQuerySet:
        return self.filter(read_at__isnull=True)


class Notification(models.Model):
    """An in-app notification shown in the recipient's inbox."""

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
    )
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="+",
        null=True,
        blank=True,
        help_text=_("The user whose action triggered this notification."),
    )
    kind = models.CharField(_("kind"), max_length=32, choices=NotificationKind.choices)
    connection = models.ForeignKey(
        Connection,
        on_delete=models.CASCADE,
        related_name="notifications",
        null=True,
        blank=True,
    )
    # Free-form payload for badge/quiz notices (slug or title snapshot).
    payload = models.CharField(_("payload"), max_length=120, blank=True)
    read_at = models.DateTimeField(_("read at"), null=True, blank=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    objects = NotificationQuerySet.as_manager()

    class Meta:
        ordering = ("-created_at",)
        verbose_name = _("notification")
        verbose_name_plural = _("notifications")
        indexes = [
            models.Index(fields=["recipient", "read_at"], name="notif_recipient_read_idx"),
            models.Index(fields=["recipient", "created_at"], name="notif_recipient_created_idx"),
        ]

    def __str__(self) -> str:
        return f"{self.kind} → {self.recipient_id}"

    @property
    def is_read(self) -> bool:
        return self.read_at is not None

    def mark_read(self) -> None:
        if self.read_at is None:
            self.read_at = timezone.now()
            self.save(update_fields=["read_at"])
