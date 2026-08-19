from django.urls import path

from . import views

app_name = "learning"

urlpatterns = [
    path("", views.roadmap_list_view, name="list"),
    path("<slug:roadmap_slug>/", views.roadmap_detail_view, name="roadmap"),
    path(
        "<slug:roadmap_slug>/<slug:lesson_slug>/",
        views.lesson_detail_view,
        name="lesson",
    ),
    path(
        "<slug:roadmap_slug>/<slug:lesson_slug>/clear/",
        views.lesson_complete_view,
        name="complete",
    ),
]
