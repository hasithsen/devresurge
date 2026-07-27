from django.urls import path

from . import views

app_name = "connections"

urlpatterns = [
    path("", views.connection_list_view, name="list"),
    path("notifications/", views.notification_list_view, name="notifications"),
    path("request/<int:user_id>/", views.connection_request_view, name="request"),
    path("<int:pk>/accept/", views.connection_accept_view, name="accept"),
    path("<int:pk>/decline/", views.connection_decline_view, name="decline"),
    path("<int:pk>/cancel/", views.connection_cancel_view, name="cancel"),
    path("<int:pk>/remove/", views.connection_remove_view, name="remove"),
    path("<int:pk>/relation/", views.connection_relation_view, name="relation"),
    path("block/<int:user_id>/", views.connection_block_view, name="block"),
    path("<int:pk>/unblock/", views.connection_unblock_view, name="unblock"),
]
