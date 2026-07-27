from django.urls import path

from . import views

app_name = "quizzes"

urlpatterns = [
    path("", views.quiz_list_view, name="list"),
    path("badges/", views.badge_cabinet_view, name="badges"),
    path("badges/<slug:slug>/", views.badge_detail_view, name="badge_detail"),
    path("badges/<slug:slug>.svg", views.badge_svg_view, name="badge_svg"),
    path(
        "badges/<slug:slug>/@<slug:handle>.svg",
        views.badge_holder_svg_view,
        name="badge_holder_svg",
    ),
    path("<slug:slug>/", views.quiz_detail_view, name="detail"),
    path("<slug:slug>/take/", views.quiz_take_view, name="take"),
]
