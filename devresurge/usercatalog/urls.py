from django.urls import path

from . import views

app_name = "usercatalog"

urlpatterns = [
    path("create/", views.UserProfileCreateView.as_view(), name="userprofile_create"),
    path("<int:pk>/", views.UserProfileDetailView.as_view(), name="userprofile_detail"),
    path("<int:pk>/", views.UserProfileDetailView.as_view(), name="userprofile_update"),
    path("<int:pk>/", views.UserProfileDetailView.as_view(), name="userprofile_list"),
]
