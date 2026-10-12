from django.urls import path

from devresurge.search import views as course_views

from . import views

app_name = "learning"

urlpatterns = [
    path("", views.roadmap_list_view, name="list"),
    # Book-length courses (filesystem markdown) — before roadmap slug catch-all
    path("courses/", course_views.course_list, name="course_list"),
    path("courses/<slug:course_slug>/", course_views.course_detail, name="course_detail"),
    path(
        "courses/<slug:course_slug>/<slug:chapter_slug>/",
        course_views.course_chapter,
        name="course_chapter",
    ),
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
