"""Public course viewer at /courses/."""

from django.urls import path

from . import views

app_name = "courses"

urlpatterns = [
    path("", views.course_list, name="list"),
    path("<slug:course_slug>/", views.course_detail, name="detail"),
    path(
        "<slug:course_slug>/<slug:chapter_slug>/",
        views.course_chapter,
        name="chapter",
    ),
]
