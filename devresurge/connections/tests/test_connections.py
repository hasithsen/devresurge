from __future__ import annotations

from http import HTTPStatus

import pytest
from django.core import mail
from django.db import IntegrityError
from django.db import transaction
from django.urls import reverse

from devresurge.connections.models import Connection
from devresurge.connections.models import ConnectionStatus
from devresurge.connections.models import Notification
from devresurge.connections.models import NotificationKind
from devresurge.connections.tests.factories import ConnectionFactory
from devresurge.connections.tests.factories import NotificationFactory
from devresurge.users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


# ---------------------------------------------------------------------------
# Model
# ---------------------------------------------------------------------------


def test_between_finds_connection_in_either_direction():
    a = UserFactory()
    b = UserFactory()
    conn = ConnectionFactory(requester=a, addressee=b)
    assert Connection.between(a, b) == conn
    assert Connection.between(b, a) == conn


def test_self_connection_is_rejected_by_db():
    user = UserFactory()
    with pytest.raises(IntegrityError), transaction.atomic():
        Connection.objects.create(requester=user, addressee=user)


def test_duplicate_pair_is_rejected_by_db():
    a = UserFactory()
    b = UserFactory()
    ConnectionFactory(requester=a, addressee=b)
    with pytest.raises(IntegrityError), transaction.atomic():
        Connection.objects.create(requester=a, addressee=b)


# ---------------------------------------------------------------------------
# Request flow
# ---------------------------------------------------------------------------


def test_request_creates_pending_connection_notification_and_email(client):
    me = UserFactory()
    target = UserFactory()
    client.force_login(me)

    response = client.post(reverse("connections:request", args=[target.pk]))
    assert response.status_code == HTTPStatus.FOUND

    conn = Connection.objects.get(requester=me, addressee=target)
    assert conn.status == ConnectionStatus.PENDING

    notification = Notification.objects.get(recipient=target)
    assert notification.kind == NotificationKind.CONNECTION_REQUEST
    assert notification.actor == me
    assert notification.connection == conn

    assert len(mail.outbox) == 1
    assert mail.outbox[0].to == [target.email]


def test_request_respects_recipient_email_opt_out(client):
    me = UserFactory()
    target = UserFactory(email_notifications=False)
    client.force_login(me)

    client.post(reverse("connections:request", args=[target.pk]))

    assert Notification.objects.filter(recipient=target).count() == 1
    assert len(mail.outbox) == 0


def test_cannot_connect_with_self(client):
    me = UserFactory()
    client.force_login(me)
    client.post(reverse("connections:request", args=[me.pk]))
    assert Connection.objects.count() == 0


def test_duplicate_request_does_not_create_second_connection(client):
    me = UserFactory()
    target = UserFactory()
    client.force_login(me)
    client.post(reverse("connections:request", args=[target.pk]))
    client.post(reverse("connections:request", args=[target.pk]))
    assert Connection.objects.filter(requester=me, addressee=target).count() == 1
    assert Notification.objects.filter(recipient=target).count() == 1


def test_request_requires_login(client):
    target = UserFactory()
    response = client.post(reverse("connections:request", args=[target.pk]))
    assert response.status_code == HTTPStatus.FOUND
    assert "/accounts/login/" in response.url


def test_request_after_decline_revives(client):
    me = UserFactory()
    target = UserFactory()
    ConnectionFactory(requester=me, addressee=target, status=ConnectionStatus.DECLINED)
    client.force_login(me)

    client.post(reverse("connections:request", args=[target.pk]))
    conn = Connection.objects.get(requester=me, addressee=target)
    assert conn.status == ConnectionStatus.PENDING
    assert Notification.objects.filter(recipient=target).count() == 1


# ---------------------------------------------------------------------------
# Accept / decline / cancel / remove
# ---------------------------------------------------------------------------


def test_accept_marks_connected_and_notifies_requester(client):
    requester = UserFactory()
    me = UserFactory()
    conn = ConnectionFactory(requester=requester, addressee=me)
    NotificationFactory(
        recipient=me,
        actor=requester,
        kind=NotificationKind.CONNECTION_REQUEST,
        connection=conn,
    )
    client.force_login(me)

    response = client.post(reverse("connections:accept", args=[conn.pk]))
    assert response.status_code == HTTPStatus.FOUND

    conn.refresh_from_db()
    assert conn.status == ConnectionStatus.ACCEPTED
    assert conn.responded_at is not None

    # Requester is notified + emailed.
    accepted_notif = Notification.objects.get(
        recipient=requester,
        kind=NotificationKind.CONNECTION_ACCEPTED,
    )
    assert accepted_notif.actor == me
    assert len(mail.outbox) == 1
    assert mail.outbox[0].to == [requester.email]

    # The original request notification is marked read.
    request_notif = Notification.objects.get(
        recipient=me,
        kind=NotificationKind.CONNECTION_REQUEST,
    )
    assert request_notif.read_at is not None


def test_cannot_accept_someone_elses_request(client):
    requester = UserFactory()
    addressee = UserFactory()
    intruder = UserFactory()
    conn = ConnectionFactory(requester=requester, addressee=addressee)
    client.force_login(intruder)

    response = client.post(reverse("connections:accept", args=[conn.pk]))
    assert response.status_code == HTTPStatus.NOT_FOUND
    conn.refresh_from_db()
    assert conn.status == ConnectionStatus.PENDING


def test_decline_sets_status_without_notifying_requester(client):
    requester = UserFactory()
    me = UserFactory()
    conn = ConnectionFactory(requester=requester, addressee=me)
    client.force_login(me)

    client.post(reverse("connections:decline", args=[conn.pk]))
    conn.refresh_from_db()
    assert conn.status == ConnectionStatus.DECLINED
    assert not Notification.objects.filter(
        recipient=requester,
        kind=NotificationKind.CONNECTION_ACCEPTED,
    ).exists()


def test_cancel_withdraws_pending_request(client):
    me = UserFactory()
    target = UserFactory()
    conn = ConnectionFactory(requester=me, addressee=target)
    client.force_login(me)

    client.post(reverse("connections:cancel", args=[conn.pk]))
    assert not Connection.objects.filter(pk=conn.pk).exists()


def test_remove_deletes_accepted_connection(client):
    me = UserFactory()
    other = UserFactory()
    conn = ConnectionFactory(
        requester=me,
        addressee=other,
        status=ConnectionStatus.ACCEPTED,
    )
    client.force_login(me)

    client.post(reverse("connections:remove", args=[conn.pk]))
    assert not Connection.objects.filter(pk=conn.pk).exists()


# ---------------------------------------------------------------------------
# Notifications inbox + badge
# ---------------------------------------------------------------------------


def test_unread_badge_count_in_context(client):
    me = UserFactory()
    NotificationFactory(recipient=me)
    NotificationFactory(recipient=me)
    client.force_login(me)

    response = client.get(reverse("connections:list"))
    assert response.context["unread_notification_count"] == 2


def test_inbox_marks_notifications_read(client):
    me = UserFactory()
    NotificationFactory(recipient=me)
    client.force_login(me)

    response = client.get(reverse("connections:notifications"))
    assert response.status_code == HTTPStatus.OK
    assert Notification.objects.for_user(me).unread().count() == 0


def test_inbox_requires_login(client):
    response = client.get(reverse("connections:notifications"))
    assert response.status_code == HTTPStatus.FOUND
    assert "/accounts/login/" in response.url


# ---------------------------------------------------------------------------
# Notification settings
# ---------------------------------------------------------------------------


def test_settings_page_toggles_email_preference(client):
    me = UserFactory(email_notifications=True)
    client.force_login(me)

    # Unchecked checkbox => field omitted => False.
    response = client.post(reverse("users:settings"), data={})
    assert response.status_code == HTTPStatus.FOUND
    me.refresh_from_db()
    assert me.email_notifications is False

    response = client.post(
        reverse("users:settings"),
        data={"email_notifications": "on"},
    )
    me.refresh_from_db()
    assert me.email_notifications is True


# ---------------------------------------------------------------------------
# Profile page connect button
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# Privacy: never expose emails in connection features
# ---------------------------------------------------------------------------


def test_notification_email_uses_public_name_not_email(client):
    me = UserFactory()
    me.profile.display_name = "Ada Lovelace"
    me.profile.save()
    target = UserFactory()
    client.force_login(me)

    client.post(reverse("connections:request", args=[target.pk]))

    msg = mail.outbox[0]
    rendered = msg.subject + msg.body + "".join(alt[0] for alt in msg.alternatives)
    assert "Ada Lovelace" in rendered
    # Neither party's email address may appear in the message body/subject.
    assert me.email not in rendered
    assert target.email not in rendered


def test_inbox_does_not_expose_actor_email(client):
    requester = UserFactory()
    requester.profile.display_name = "Grace Hopper"
    requester.profile.save()
    me = UserFactory()
    conn = ConnectionFactory(requester=requester, addressee=me)
    NotificationFactory(
        recipient=me,
        actor=requester,
        kind=NotificationKind.CONNECTION_REQUEST,
        connection=conn,
    )
    client.force_login(me)

    content = client.get(reverse("connections:notifications")).content.decode()
    assert "Grace Hopper" in content
    assert requester.email not in content


def test_network_page_does_not_expose_email(client):
    me = UserFactory()
    other = UserFactory()
    other.profile.display_name = "Linus T"
    other.profile.save()
    ConnectionFactory(requester=me, addressee=other, status=ConnectionStatus.ACCEPTED)
    client.force_login(me)

    content = client.get(reverse("connections:list")).content.decode()
    assert "Linus T" in content
    assert other.email not in content


def test_request_message_falls_back_to_handle(client):
    me = UserFactory()
    target = UserFactory()
    target.profile.display_name = ""
    target.profile.save()
    client.force_login(me)

    response = client.post(
        reverse("connections:request", args=[target.pk]),
        follow=True,
    )
    content = response.content.decode()
    assert f"@{target.profile.handle}" in content
    assert target.email not in content


def test_profile_shows_connect_state(client):
    me = UserFactory()
    other = UserFactory()
    client.force_login(me)

    url = reverse("profiles:public", kwargs={"handle": other.profile.handle})
    response = client.get(url)
    assert response.context["can_connect"] is True
    assert response.context["connect_state"] == "none"

    ConnectionFactory(
        requester=me,
        addressee=other,
        status=ConnectionStatus.ACCEPTED,
    )
    response = client.get(url)
    assert response.context["connect_state"] == "connected"


# ---------------------------------------------------------------------------
# Relation labels, notes, block
# ---------------------------------------------------------------------------


def test_request_stores_relation_and_message(client):
    me = UserFactory()
    target = UserFactory()
    client.force_login(me)

    client.post(
        reverse("connections:request", args=[target.pk]),
        data={"relation": "collaborator", "message": "Loved your Django talk."},
    )
    conn = Connection.objects.get(requester=me, addressee=target)
    assert conn.relation == "collaborator"
    assert conn.message == "Loved your Django talk."


def test_update_relation_on_accepted_connection(client):
    me = UserFactory()
    other = UserFactory()
    conn = ConnectionFactory(
        requester=me,
        addressee=other,
        status=ConnectionStatus.ACCEPTED,
        relation="peer",
    )
    client.force_login(me)
    client.post(
        reverse("connections:relation", args=[conn.pk]),
        data={"relation": "mentor"},
    )
    conn.refresh_from_db()
    assert conn.relation == "mentor"


def test_block_prevents_new_requests(client):
    me = UserFactory()
    other = UserFactory()
    client.force_login(me)
    client.post(reverse("connections:block", args=[other.pk]))

    blocked = Connection.objects.get(requester=me, addressee=other)
    assert blocked.status == ConnectionStatus.BLOCKED

    client.force_login(other)
    client.post(reverse("connections:request", args=[me.pk]))
    assert (
        Connection.objects.filter(requester=other, addressee=me).count() == 0
    )
    blocked.refresh_from_db()
    assert blocked.status == ConnectionStatus.BLOCKED


def test_unblock_removes_block_row(client):
    me = UserFactory()
    other = UserFactory()
    conn = ConnectionFactory(
        requester=me,
        addressee=other,
        status=ConnectionStatus.BLOCKED,
    )
    client.force_login(me)
    client.post(reverse("connections:unblock", args=[conn.pk]))
    assert not Connection.objects.filter(pk=conn.pk).exists()
