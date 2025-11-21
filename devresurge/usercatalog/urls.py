from django.urls import path

from . import views

app_name = "usercatalog"

urlpatterns = [
    path("create/", views.UserProfileCreateView.as_view(), name="userprofile_create"),
    path("<int:pk>/", views.UserProfileDetailView.as_view(), name="userprofile_detail"),
    path(
        "edit/<int:pk>/",
        views.UserProfileUpdateView.as_view(),
        name="userprofile_update",
    ),
    path("", views.UserProfileListView.as_view(), name="userprofile_list"),
]
