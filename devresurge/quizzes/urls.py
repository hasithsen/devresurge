from django.urls import path

from . import views

app_name = "quizzes"

urlpatterns = [
    path("", views.quiz_list_view, name="list"),
    path("badges/", views.badge_cabinet_view, name="badges"),
    path("<slug:slug>/", views.quiz_detail_view, name="detail"),
    path("<slug:slug>/take/", views.quiz_take_view, name="take"),
]
