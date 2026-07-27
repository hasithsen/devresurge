from django.contrib import admin

from .models import Connection
from .models import Notification


@admin.register(Connection)
class ConnectionAdmin(admin.ModelAdmin):
    list_display = (
        "requester",
        "addressee",
        "status",
        "relation",
        "created_at",
        "responded_at",
    )
    list_filter = ("status", "relation", "created_at")
    search_fields = (
        "requester__email",
        "requester__name",
        "addressee__email",
        "addressee__name",
        "message",
    )
    raw_id_fields = ("requester", "addressee")
    date_hierarchy = "created_at"


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("recipient", "kind", "actor", "payload", "is_read", "created_at")
    list_filter = ("kind", "created_at")
    search_fields = ("recipient__email", "actor__email", "payload")
    raw_id_fields = ("recipient", "actor", "connection")
    readonly_fields = (
        "recipient",
        "actor",
        "kind",
        "connection",
        "payload",
        "read_at",
        "created_at",
    )
    date_hierarchy = "created_at"

    def has_add_permission(self, request) -> bool:  # noqa: ARG002
        return False
