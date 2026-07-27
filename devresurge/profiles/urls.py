from django.urls import path

from . import views

app_name = "profiles"

urlpatterns = [
    path("u/", views.profile_browse_view, name="browse"),
    path("u/<slug:handle>/badge.svg", views.profile_badge_view, name="badge"),
    path("u/<slug:handle>/endorse/", views.skill_endorse_view, name="endorse"),
    path("u/<slug:handle>/unendorse/", views.skill_unendorse_view, name="unendorse"),
    path("u/<slug:handle>/recommend/", views.recommendation_create_view, name="recommend"),
    path("u/<slug:handle>/", views.profile_public_view, name="public"),
    path("c/", views.link_click_view, name="link_click"),
    path("me/", views.profile_dashboard_view, name="dashboard"),
    path("me/edit/", views.profile_edit_view, name="edit"),
    path("me/analytics/", views.profile_analytics_view, name="analytics"),
    path("me/export/readme.md", views.profile_export_readme_view, name="export_readme"),
    path("me/experience/", views.experience_list_view, name="experience_list"),
    path("me/experience/new/", views.experience_create_view, name="experience_create"),
    path("me/experience/<int:pk>/edit/", views.experience_update_view, name="experience_update"),
    path("me/experience/<int:pk>/delete/", views.experience_delete_view, name="experience_delete"),
    path("me/education/", views.education_list_view, name="education_list"),
    path("me/education/new/", views.education_create_view, name="education_create"),
    path("me/education/<int:pk>/edit/", views.education_update_view, name="education_update"),
    path("me/education/<int:pk>/delete/", views.education_delete_view, name="education_delete"),
    path("me/projects/", views.project_list_view, name="project_list"),
    path("me/projects/new/", views.project_create_view, name="project_create"),
    path("me/projects/reorder/", views.project_reorder_view, name="project_reorder"),
    path("me/projects/<int:pk>/edit/", views.project_update_view, name="project_update"),
    path("me/projects/<int:pk>/delete/", views.project_delete_view, name="project_delete"),
    path("me/links/", views.link_list_view, name="link_list"),
    path("me/links/new/", views.link_create_view, name="link_create"),
    path("me/links/reorder/", views.link_reorder_view, name="link_reorder"),
    path("me/links/<int:pk>/edit/", views.link_update_view, name="link_update"),
    path("me/links/<int:pk>/delete/", views.link_delete_view, name="link_delete"),
]
