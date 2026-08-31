from django.urls import path

from devresurge.connections import views as connection_views

from . import views

app_name = "profiles"

urlpatterns = [
    path("u/", views.profile_browse_view, name="browse"),
    path("map/", connection_views.explore_map_view, name="explore_map"),
    path("map/data.json", connection_views.explore_map_data_view, name="explore_map_data"),
    path("u/<slug:handle>/badge.svg", views.profile_badge_view, name="badge"),
    path(
        "u/<slug:handle>/map/",
        connection_views.public_network_map_view,
        name="network_map",
    ),
    path(
        "u/<slug:handle>/map/data.json",
        connection_views.public_network_map_data_view,
        name="network_map_data",
    ),
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
    path("me/tools/", views.tool_list_view, name="tool_list"),
    path("me/tools/new/", views.tool_create_view, name="tool_create"),
    path("me/tools/reorder/", views.tool_reorder_view, name="tool_reorder"),
    path("me/tools/<int:pk>/edit/", views.tool_update_view, name="tool_update"),
    path("me/tools/<int:pk>/delete/", views.tool_delete_view, name="tool_delete"),
    path("me/showcases/", views.showcase_list_view, name="showcase_list"),
    path("me/showcases/new/", views.showcase_create_view, name="showcase_create"),
    path("me/showcases/reorder/", views.showcase_reorder_view, name="showcase_reorder"),
    path("me/showcases/<int:pk>/edit/", views.showcase_update_view, name="showcase_update"),
    path("me/showcases/<int:pk>/delete/", views.showcase_delete_view, name="showcase_delete"),
    path("me/showcases/<int:pk>/sync/", views.showcase_sync_view, name="showcase_sync"),
    path(
        "u/<slug:handle>/lab/<slug:slug>/",
        views.showcase_detail_view,
        name="showcase_detail",
    ),
    path("me/links/", views.link_list_view, name="link_list"),
    path("me/links/new/", views.link_create_view, name="link_create"),
    path("me/links/reorder/", views.link_reorder_view, name="link_reorder"),
    path("me/links/<int:pk>/edit/", views.link_update_view, name="link_update"),
    path("me/links/<int:pk>/delete/", views.link_delete_view, name="link_delete"),
]
