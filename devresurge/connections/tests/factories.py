from __future__ import annotations

from factory import SubFactory
from factory.django import DjangoModelFactory

from devresurge.connections.models import Connection
from devresurge.connections.models import ConnectionStatus
from devresurge.connections.models import Notification
from devresurge.connections.models import NotificationKind
from devresurge.users.tests.factories import UserFactory


class ConnectionFactory(DjangoModelFactory[Connection]):
    requester = SubFactory(UserFactory)
    addressee = SubFactory(UserFactory)
    status = ConnectionStatus.PENDING

    class Meta:
        model = Connection


class NotificationFactory(DjangoModelFactory[Notification]):
    recipient = SubFactory(UserFactory)
    actor = SubFactory(UserFactory)
    kind = NotificationKind.CONNECTION_REQUEST

    class Meta:
        model = Notification
