from django.urls import path

from . import views

app_name = "profiles"

urlpatterns = [
    path("u/", views.profile_browse_view, name="browse"),
    path("u/<slug:handle>/", views.profile_public_view, name="public"),
    path("me/", views.profile_dashboard_view, name="dashboard"),
    path("me/edit/", views.profile_edit_view, name="edit"),
    path("me/projects/", views.project_list_view, name="project_list"),
    path("me/projects/new/", views.project_create_view, name="project_create"),
    path("me/projects/<int:pk>/edit/", views.project_update_view, name="project_update"),
    path("me/projects/<int:pk>/delete/", views.project_delete_view, name="project_delete"),
    path("me/links/", views.link_list_view, name="link_list"),
    path("me/links/new/", views.link_create_view, name="link_create"),
    path("me/links/<int:pk>/edit/", views.link_update_view, name="link_update"),
    path("me/links/<int:pk>/delete/", views.link_delete_view, name="link_delete"),
]
